# Deployment Guide
# RF Shield - Privacy Protection Platform

**Version:** 1.0  
**Date:** December 14, 2024  
**Author:** DevOps Team  
**Status:** Draft

---

## Table of Contents

1. [Deployment Overview](#1-deployment-overview)
2. [Infrastructure Setup](#2-infrastructure-setup)
3. [Mobile App Deployment](#3-mobile-app-deployment)
4. [Backend Deployment](#4-backend-deployment)
5. [Database Migration](#5-database-migration)
6. [Hardware Firmware Deployment](#6-hardware-firmware-deployment)
7. [Monitoring & Logging](#7-monitoring--logging)
8. [Rollback Procedures](#8-rollback-procedures)
9. [Disaster Recovery](#9-disaster-recovery)

---

## 1. Deployment Overview

### 1.1 Deployment Environments

```
┌─────────────────────────────────────────────────────────┐
│                    Development                           │
│  - Local machines                                        │
│  - Docker Compose                                        │
│  - Firebase Emulator                                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                      Staging                             │
│  - GCP Cloud Run (staging)                               │
│  - Cloud SQL (staging instance)                          │
│  - Firebase Staging Project                              │
│  - TestFlight / Play Beta                                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Production                            │
│  - GCP Cloud Run (multi-region)                          │
│  - Cloud SQL (HA config)                                 │
│  - Firebase Production Project                           │
│  - App Store / Play Store                                │
│  - Cloudflare CDN                                        │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Release Schedule

**Mobile App:**
- Beta releases: Weekly (Fridays)
- Production releases: Bi-weekly (every 2 weeks)
- Hotfixes: As needed (within 24h for P0 bugs)

**Backend:**
- Staging deploys: On every merge to `main`
- Production deploys: Weekly (Tuesdays 10 AM PST)
- Hotfixes: As needed

**Firmware:**
- Beta releases: Monthly
- Production releases: Quarterly
- Security patches: As needed

### 1.3 Deployment Checklist

**Pre-Deployment:**
- [ ] All tests passing (unit, integration, E2E)
- [ ] Code review approved
- [ ] Security scan completed (no critical issues)
- [ ] Performance benchmarks met
- [ ] Database migrations tested
- [ ] Release notes prepared
- [ ] Stakeholders notified

**Deployment:**
- [ ] Deploy to staging
- [ ] Smoke tests on staging
- [ ] Deploy to production (blue-green)
- [ ] Verify health checks
- [ ] Monitor error rates (15 minutes)
- [ ] Gradual rollout (10% → 50% → 100%)

**Post-Deployment:**
- [ ] Monitor dashboards (1 hour)
- [ ] Check error tracking (Sentry)
- [ ] Verify user metrics (analytics)
- [ ] Update documentation
- [ ] Close deployment ticket

---

## 2. Infrastructure Setup

### 2.1 Google Cloud Platform (GCP)

#### Initial Setup

**1. Create GCP Project:**
```bash
# Set variables
PROJECT_ID="rf-shield-prod"
REGION="us-central1"

# Create project
gcloud projects create $PROJECT_ID --name="RF Shield Production"

# Set default project
gcloud config set project $PROJECT_ID

# Enable billing
gcloud billing projects link $PROJECT_ID --billing-account=BILLING_ACCOUNT_ID
```

**2. Enable Required APIs:**
```bash
# Enable APIs
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  cloudbuild.googleapis.com \
  containerregistry.googleapis.com \
  firebase.googleapis.com \
  cloudscheduler.googleapis.com \
  cloudtasks.googleapis.com
```

**3. Set Up VPC Network:**
```bash
# Create VPC
gcloud compute networks create rf-shield-vpc \
  --subnet-mode=custom \
  --bgp-routing-mode=regional

# Create subnet
gcloud compute networks subnets create rf-shield-subnet \
  --network=rf-shield-vpc \
  --region=$REGION \
  --range=10.0.0.0/24

# Create firewall rules
gcloud compute firewall-rules create allow-internal \
  --network=rf-shield-vpc \
  --allow=tcp,udp,icmp \
  --source-ranges=10.0.0.0/24
```

#### Terraform Configuration

**File:** `infrastructure/terraform/main.tf`

```hcl
terraform {
  required_version = ">= 1.0"
  
  backend "gcs" {
    bucket = "rf-shield-terraform-state"
    prefix = "prod"
  }
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Cloud SQL (PostgreSQL)
resource "google_sql_database_instance" "oui_database" {
  name             = "rf-shield-oui-db-${var.environment}"
  database_version = "POSTGRES_14"
  region           = var.region
  
  settings {
    tier              = var.db_tier
    availability_type = var.environment == "prod" ? "REGIONAL" : "ZONAL"
    
    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7
      backup_retention_settings {
        retained_backups = 30
      }
    }
    
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
    }
    
    database_flags {
      name  = "max_connections"
      value = "100"
    }
  }
  
  deletion_protection = var.environment == "prod"
}

# Cloud SQL Database
resource "google_sql_database" "oui_db" {
  name     = "oui_database"
  instance = google_sql_database_instance.oui_database.name
}

# Cloud SQL User
resource "google_sql_user" "oui_user" {
  name     = "oui_admin"
  instance = google_sql_database_instance.oui_database.name
  password = var.db_password
}

# Cloud Storage (Firmware Binaries)
resource "google_storage_bucket" "firmware" {
  name          = "rf-shield-firmware-${var.environment}"
  location      = "US"
  storage_class = "STANDARD"
  
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 90
    }
  }
  
  versioning {
    enabled = true
  }
  
  cors {
    origin          = ["https://cdn.rfshield.io"]
    method          = ["GET", "HEAD"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

# Cloud Run Service
resource "google_cloud_run_service" "api" {
  name     = "rf-shield-api-${var.environment}"
  location = var.region
  
  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/api:${var.api_version}"
        
        resources {
          limits = {
            cpu    = "2000m"
            memory = "1Gi"
          }
        }
        
        env {
          name  = "DATABASE_URL"
          value = "postgresql://${google_sql_user.oui_user.name}:${var.db_password}@${google_sql_database_instance.oui_database.private_ip_address}:5432/${google_sql_database.oui_db.name}"
        }
        
        env {
          name  = "FIREBASE_PROJECT_ID"
          value = var.firebase_project_id
        }
        
        env {
          name  = "STRIPE_SECRET_KEY"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.stripe_key.secret_id
              key  = "latest"
            }
          }
        }
      }
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = var.environment == "prod" ? "2" : "1"
        "autoscaling.knative.dev/maxScale" = "100"
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.oui_database.connection_name
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Cloud Run IAM
resource "google_cloud_run_service_iam_member" "public_access" {
  count = var.environment == "prod" ? 1 : 0
  
  service  = google_cloud_run_service.api.name
  location = google_cloud_run_service.api.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Secret Manager
resource "google_secret_manager_secret" "stripe_key" {
  secret_id = "stripe-secret-key-${var.environment}"
  
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "stripe_key_v1" {
  secret      = google_secret_manager_secret.stripe_key.id
  secret_data = var.stripe_secret_key
}

# Outputs
output "api_url" {
  value = google_cloud_run_service.api.status[0].url
}

output "database_connection" {
  value     = google_sql_database_instance.oui_database.connection_name
  sensitive = true
}
```

**Deploy Infrastructure:**
```bash
cd infrastructure/terraform

# Initialize
terraform init

# Plan
terraform plan -var-file="environments/prod.tfvars"

# Apply
terraform apply -var-file="environments/prod.tfvars"
```

### 2.2 Firebase Setup

**1. Create Firebase Project:**
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Create project (via console: https://console.firebase.google.com)
# Project ID: rf-shield-prod
```

**2. Initialize Firebase:**
```bash
# In project root
firebase init

# Select:
# - Firestore
# - Authentication
# - Storage
# - Functions
# - Hosting (for web dashboard, optional)
```

**3. Configure Firestore Security Rules:**

**File:** `firestore.rules`
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Helper functions
    function isAuthenticated() {
      return request.auth != null;
    }
    
    function isOwner(userId) {
      return request.auth.uid == userId;
    }
    
    function isPremium() {
      return get(/databases/$(database)/documents/users/$(request.auth.uid)).data.premium.active == true;
    }
    
    // User documents
    match /users/{userId} {
      allow read: if isAuthenticated() && isOwner(userId);
      allow write: if isAuthenticated() && isOwner(userId);
    }
    
    // Scan history (subcollection)
    match /users/{userId}/scan_history/{scanId} {
      allow read: if isAuthenticated() && isOwner(userId) && isPremium();
      allow write: if isAuthenticated() && isOwner(userId) && isPremium();
    }
    
    // OUI updates (public read)
    match /oui_updates/{version} {
      allow read: if true;
      allow write: if false; // Only via backend
    }
    
    // Threat intelligence (community)
    match /threat_intelligence/{reportId} {
      allow read: if isAuthenticated();
      allow create: if isAuthenticated();
      allow update: if isAuthenticated() && isOwner(resource.data.user_id);
    }
  }
}
```

**Deploy Firestore Rules:**
```bash
firebase deploy --only firestore:rules
```

**4. Configure Authentication:**
```bash
# Enable email/password auth
firebase auth:enable email

# Enable OAuth providers (via console)
# - Google Sign-In
# - Apple Sign-In
```

### 2.3 Cloudflare CDN

**1. Add Domain:**
```bash
# Via Cloudflare dashboard: https://dash.cloudflare.com
# Add domain: rfshield.io
# Update nameservers at registrar
```

**2. Configure CDN for Firmware:**

**DNS Records:**
```
Type: CNAME
Name: cdn
Target: c.storage.googleapis.com
Proxy: Enabled (orange cloud)
```

**Page Rules:**
```
URL: cdn.rfshield.io/firmware/*
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 year
  - Browser Cache TTL: 1 year
```

**3. SSL/TLS Configuration:**
```
SSL/TLS Mode: Full (strict)
Always Use HTTPS: On
Minimum TLS Version: 1.3
```

---

## 3. Mobile App Deployment

### 3.1 Android Deployment

#### Build Configuration

**File:** `android/app/build.gradle`
```gradle
android {
    defaultConfig {
        applicationId "com.rfshield.app"
        versionCode 1
        versionName "1.0.0"
        
        buildConfigField "String", "API_URL", "\"https://api.rfshield.io/v1\""
    }
    
    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
            
            signingConfig signingConfigs.release
        }
    }
    
    signingConfigs {
        release {
            storeFile file(RELEASE_KEYSTORE_PATH)
            storePassword RELEASE_KEYSTORE_PASSWORD
            keyAlias RELEASE_KEY_ALIAS
            keyPassword RELEASE_KEY_PASSWORD
        }
    }
}
```

#### CI/CD Pipeline (GitHub Actions)

**File:** `.github/workflows/android-deploy.yml`
```yaml
name: Android Production Deploy

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Decode keystore
        run: |
          echo "${{ secrets.RELEASE_KEYSTORE_BASE64 }}" | base64 -d > release.keystore
      
      - name: Build release APK/AAB
        run: |
          cd android
          ./gradlew bundleRelease
        env:
          RELEASE_KEYSTORE_PATH: ../release.keystore
          RELEASE_KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          RELEASE_KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          RELEASE_KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
      
      - name: Upload to Play Console
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.PLAY_SERVICE_ACCOUNT }}
          packageName: com.rfshield.app
          releaseFiles: android/app/build/outputs/bundle/release/app-release.aab
          track: production
          status: completed
          inAppUpdatePriority: 2
          whatsNewDirectory: metadata/whatsnew
      
      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body_path: CHANGELOG.md
```

#### Manual Deployment Steps

**1. Prepare Release:**
```bash
cd android

# Update version
# Edit app/build.gradle:
# versionCode 2
# versionName "1.0.1"

# Clean build
./gradlew clean

# Build release AAB
./gradlew bundleRelease

# Output: app/build/outputs/bundle/release/app-release.aab
```

**2. Upload to Play Console:**
```
1. Go to: https://play.google.com/console
2. Select "RF Shield" app
3. Release → Production → Create new release
4. Upload AAB: app-release.aab
5. Release notes:
   - What's new in this version
   - Bug fixes
6. Review and roll out:
   - Staged rollout: 10% → 50% → 100% (over 7 days)
   - Or full rollout immediately
```

**3. Monitor Rollout:**
```
- Check crash rate (target: <1%)
- Check ANR rate (target: <0.1%)
- Monitor user reviews
- Watch for spike in support tickets
```

### 3.2 iOS Deployment

#### Build Configuration

**File:** `ios/RFShield/Info.plist`
```xml
<key>CFBundleShortVersionString</key>
<string>1.0.0</string>
<key>CFBundleVersion</key>
<string>1</string>

<key>API_URL</key>
<string>https://api.rfshield.io/v1</string>
```

#### CI/CD Pipeline (GitHub Actions)

**File:** `.github/workflows/ios-deploy.yml`
```yaml
name: iOS Production Deploy

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  deploy:
    runs-on: macos-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Xcode
        uses: maxim-lobanov/setup-xcode@v1
        with:
          xcode-version: '15.0'
      
      - name: Install dependencies
        run: |
          cd ios
          pod install
      
      - name: Import signing certificate
        run: |
          echo "${{ secrets.IOS_CERTIFICATE_BASE64 }}" | base64 -d > certificate.p12
          security create-keychain -p "" build.keychain
          security import certificate.p12 -k build.keychain -P "${{ secrets.CERTIFICATE_PASSWORD }}" -T /usr/bin/codesign
          security set-keychain-settings -t 3600 -u build.keychain
          security default-keychain -s build.keychain
          security unlock-keychain -p "" build.keychain
      
      - name: Install provisioning profile
        run: |
          mkdir -p ~/Library/MobileDevice/Provisioning\ Profiles
          echo "${{ secrets.PROVISIONING_PROFILE_BASE64 }}" | base64 -d > ~/Library/MobileDevice/Provisioning\ Profiles/profile.mobileprovision
      
      - name: Build archive
        run: |
          cd ios
          xcodebuild -workspace RFShield.xcworkspace \
                     -scheme RFShield \
                     -configuration Release \
                     -archivePath $PWD/build/RFShield.xcarchive \
                     archive
      
      - name: Export IPA
        run: |
          cd ios
          xcodebuild -exportArchive \
                     -archivePath $PWD/build/RFShield.xcarchive \
                     -exportOptionsPlist ExportOptions.plist \
                     -exportPath $PWD/build
      
      - name: Upload to App Store Connect
        run: |
          xcrun altool --upload-app \
                       --type ios \
                       --file ios/build/RFShield.ipa \
                       --username "${{ secrets.APPLE_ID }}" \
                       --password "${{ secrets.APPLE_APP_PASSWORD }}"
      
      - name: Submit for review
        run: |
          # Use App Store Connect API or manual submission
          echo "IPA uploaded. Submit for review in App Store Connect."
```

#### Manual Deployment Steps

**1. Prepare Release:**
```bash
# Update version
# Xcode → Target → General → Version: 1.0.1, Build: 2

# Archive
# Xcode → Product → Archive

# Wait for archive to complete
```

**2. Upload to App Store Connect:**
```
1. Xcode → Window → Organizer
2. Select archive
3. Distribute App → App Store Connect
4. Upload
```

**3. Submit for Review:**
```
1. Go to: https://appstoreconnect.apple.com
2. My Apps → RF Shield
3. + Version or Platform → iOS
4. Version: 1.0.1
5. What's New:
   - Release notes
6. Build: Select uploaded build
7. Submit for Review
```

**4. Phased Release:**
```
App Store → Pricing and Availability → Phased Release
- Day 1: 1% of users
- Day 2: 2%
- Day 3: 5%
- Day 4: 10%
- Day 5: 20%
- Day 6: 50%
- Day 7: 100%
```

---

## 4. Backend Deployment

### 4.1 Docker Build

**File:** `backend/Dockerfile`
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source
COPY . .

# Build TypeScript
RUN npm run build

# Production image
FROM node:20-alpine

WORKDIR /app

# Copy dependencies
COPY --from=builder /app/node_modules ./node_modules

# Copy built files
COPY --from=builder /app/dist ./dist

# Set environment
ENV NODE_ENV=production
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node dist/healthcheck.js

# Run
EXPOSE 8080
CMD ["node", "dist/index.js"]
```

### 4.2 CI/CD Pipeline

**File:** `.github/workflows/backend-deploy.yml`
```yaml
name: Backend Production Deploy

on:
  push:
    branches:
      - main
    paths:
      - 'backend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: rf-shield-prod
      
      - name: Configure Docker
        run: gcloud auth configure-docker
      
      - name: Build Docker image
        run: |
          cd backend
          docker build -t gcr.io/rf-shield-prod/api:${{ github.sha }} .
          docker tag gcr.io/rf-shield-prod/api:${{ github.sha }} gcr.io/rf-shield-prod/api:latest
      
      - name: Push Docker image
        run: |
          docker push gcr.io/rf-shield-prod/api:${{ github.sha }}
          docker push gcr.io/rf-shield-prod/api:latest
      
      - name: Deploy to Cloud Run (Staging)
        run: |
          gcloud run deploy rf-shield-api-staging \
            --image gcr.io/rf-shield-prod/api:${{ github.sha }} \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated \
            --set-env-vars NODE_ENV=staging
      
      - name: Run smoke tests
        run: |
          curl -f https://rf-shield-api-staging-xxx.run.app/health || exit 1
      
      - name: Deploy to Cloud Run (Production)
        run: |
          gcloud run deploy rf-shield-api-prod \
            --image gcr.io/rf-shield-prod/api:${{ github.sha }} \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated \
            --set-env-vars NODE_ENV=production \
            --min-instances 2 \
            --max-instances 100 \
            --traffic-split latest=100
      
      - name: Monitor deployment
        run: |
          # Wait 5 minutes and check error rate
          sleep 300
          # If error rate > 1%, rollback (custom script)
          ./scripts/check-error-rate.sh || gcloud run services update-traffic rf-shield-api-prod --to-revisions PREVIOUS=100
```

### 4.3 Manual Deployment

**1. Build and Push Image:**
```bash
cd backend

# Build
docker build -t gcr.io/rf-shield-prod/api:v1.0.1 .

# Test locally
docker run -p 8080:8080 -e NODE_ENV=development gcr.io/rf-shield-prod/api:v1.0.1

# Push
docker push gcr.io/rf-shield-prod/api:v1.0.1
```

**2. Deploy to Staging:**
```bash
gcloud run deploy rf-shield-api-staging \
  --image gcr.io/rf-shield-prod/api:v1.0.1 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**3. Test Staging:**
```bash
# Health check
curl https://rf-shield-api-staging-xxx.run.app/health

# API test
curl -H "Authorization: Bearer $TEST_TOKEN" \
     https://rf-shield-api-staging-xxx.run.app/v1/user/profile
```

**4. Deploy to Production:**
```bash
gcloud run deploy rf-shield-api-prod \
  --image gcr.io/rf-shield-prod/api:v1.0.1 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --min-instances 2 \
  --max-instances 100
```

**5. Monitor:**
```bash
# Watch logs
gcloud run logs tail rf-shield-api-prod --format=json

# Check metrics
gcloud run services describe rf-shield-api-prod --region us-central1
```

---

## 5. Database Migration

### 5.1 Migration Strategy

**Tool:** Sequelize Migrations (Node.js) or Alembic (Python)

**Migration Naming:**
```
YYYYMMDDHHMMSS-description.js

Example:
20241214120000-add-oui-confidence-column.js
```

### 5.2 Creating Migrations

**File:** `backend/migrations/20241214120000-add-oui-confidence-column.js`
```javascript
'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('oui_master', 'confidence', {
      type: Sequelize.DECIMAL(3, 2),
      allowNull: true,
      defaultValue: 0.5
    });
    
    await queryInterface.addIndex('oui_master', ['confidence']);
  },
  
  down: async (queryInterface, Sequelize) => {
    await queryInterface.removeIndex('oui_master', ['confidence']);
    await queryInterface.removeColumn('oui_master', 'confidence');
  }
};
```

### 5.3 Running Migrations

**Development:**
```bash
cd backend
npm run migrate
```

**Staging:**
```bash
# Connect to Cloud SQL via proxy
cloud_sql_proxy -instances=rf-shield-staging:us-central1:oui-db=tcp:5432 &

# Run migrations
DATABASE_URL=postgresql://user:pass@localhost:5432/oui_database npm run migrate
```

**Production:**
```bash
# CRITICAL: Always backup before migrations
gcloud sql backups create --instance=oui-db-prod

# Connect via proxy
cloud_sql_proxy -instances=rf-shield-prod:us-central1:oui-db=tcp:5432 &

# Run migrations
DATABASE_URL=postgresql://user:pass@localhost:5432/oui_database npm run migrate

# Verify
psql postgresql://user:pass@localhost:5432/oui_database -c "\d oui_master"
```

### 5.4 Rollback Procedure

**If migration fails:**
```bash
# Rollback last migration
npm run migrate:undo

# Or rollback to specific migration
npm run migrate:undo:all --to 20241214120000-previous-migration.js

# Restore from backup if needed
gcloud sql backups restore BACKUP_ID --backup-instance=oui-db-prod
```

---

## 6. Hardware Firmware Deployment

### 6.1 Build Firmware

**File:** `firmware/platformio.ini`
```ini
[env:esp32s3]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino

build_flags =
  -DVERSION=\"1.3.0\"
  -DCORE_DEBUG_LEVEL=0

lib_deps =
  bblanchon/ArduinoJson @ ^6.21.0
  h2zero/NimBLE-Arduino @ ^1.4.1
```

**Build:**
```bash
cd firmware

# Build
pio run

# Output: .pio/build/esp32s3/firmware.bin
```

### 6.2 Sign Firmware

**Script:** `firmware/scripts/sign-firmware.sh`
```bash
#!/bin/bash

FIRMWARE_FILE=$1
VERSION=$2

# Generate SHA-256 hash
SHA256=$(sha256sum $FIRMWARE_FILE | awk '{print $1}')

# Sign with RSA private key
openssl dgst -sha256 -sign private_key.pem -out ${FIRMWARE_FILE}.sig $FIRMWARE_FILE

# Create manifest
cat > manifest.json <<EOF
{
  "version": "$VERSION",
  "file": "$(basename $FIRMWARE_FILE)",
  "sha256": "$SHA256",
  "size": $(stat -f%z $FIRMWARE_FILE),
  "signature": "$(base64 ${FIRMWARE_FILE}.sig)"
}
EOF

echo "Firmware signed: $SHA256"
```

**Usage:**
```bash
./scripts/sign-firmware.sh .pio/build/esp32s3/firmware.bin 1.3.0
```

### 6.3 Upload to CDN

```bash
# Upload firmware
gsutil cp .pio/build/esp32s3/firmware.bin gs://rf-shield-firmware-prod/esp32/1.3.0/

# Upload manifest
gsutil cp manifest.json gs://rf-shield-firmware-prod/esp32/1.3.0/

# Make public
gsutil acl ch -u AllUsers:R gs://rf-shield-firmware-prod/esp32/1.3.0/firmware.bin
```

### 6.4 Update API Endpoint

**Update latest version:**
```bash
# Update database or config
psql $DATABASE_URL <<EOF
UPDATE firmware_versions
SET latest_version = '1.3.0',
    download_url = 'https://cdn.rfshield.io/firmware/esp32/1.3.0/firmware.bin',
    sha256 = '$SHA256'
WHERE module_type = 'esp32';
EOF
```

### 6.5 Staged Rollout

**Day 1: 10% of devices**
```sql
UPDATE firmware_versions
SET rollout_percentage = 10
WHERE module_type = 'esp32' AND version = '1.3.0';
```

**Day 3: 50% (if no issues)**
```sql
UPDATE firmware_versions
SET rollout_percentage = 50
WHERE module_type = 'esp32' AND version = '1.3.0';
```

**Day 7: 100%**
```sql
UPDATE firmware_versions
SET rollout_percentage = 100
WHERE module_type = 'esp32' AND version = '1.3.0';
```

---

## 7. Monitoring & Logging

### 7.1 Application Monitoring

**Firebase Performance Monitoring:**
```typescript
import { getPerformance, trace } from 'firebase/performance';

const perf = getPerformance();

// Trace scan performance
const scanTrace = trace(perf, 'wifi_scan');
scanTrace.start();

// ... perform scan ...

scanTrace.stop();
```

**Custom Metrics:**
```typescript
import { logEvent } from 'firebase/analytics';

logEvent('threat_detected', {
  device_type: 'wifi_camera',
  manufacturer: 'Wyze Labs',
  threat_level: 'high'
});
```

### 7.2 Error Tracking

**Sentry Setup:**

**File:** `mobile/src/sentry.ts`
```typescript
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'https://xxx@sentry.io/xxx',
  environment: 'production',
  tracesSampleRate: 0.1,
  beforeSend(event, hint) {
    // Don't send errors from beta builds
    if (__DEV__) return null;
    return event;
  }
});
```

### 7.3 Logging

**Backend Logging (Winston):**
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

logger.info('User authenticated', { userId: 'user-123' });
logger.error('Database connection failed', { error: err.message });
```

### 7.4 Dashboards

**GCP Monitoring Dashboard:**
```yaml
dashboardFilters: []
displayName: RF Shield Production
mosaicLayout:
  columns: 12
  tiles:
  - width: 6
    height: 4
    widget:
      title: API Request Rate
      xyChart:
        dataSets:
        - timeSeriesQuery:
            timeSeriesFilter:
              filter: resource.type="cloud_run_revision"
          plotType: LINE
  
  - width: 6
    height: 4
    widget:
      title: Error Rate
      xyChart:
        dataSets:
        - timeSeriesQuery:
            timeSeriesFilter:
              filter: resource.type="cloud_run_revision" AND metric.type="run.googleapis.com/request_count" AND metric.label.response_code_class="5xx"
          plotType: LINE
  
  - width: 6
    height: 4
    widget:
      title: Database Connections
      xyChart:
        dataSets:
        - timeSeriesQuery:
            timeSeriesFilter:
              filter: resource.type="cloudsql_database" AND metric.type="cloudsql.googleapis.com/database/postgresql/num_backends"
          plotType: LINE
```

---

## 8. Rollback Procedures

### 8.1 Mobile App Rollback

**Android:**
```
1. Go to Play Console
2. Release Management → App releases → Production
3. Create new release
4. Re-upload previous version AAB
5. Release notes: "Reverting to v1.0.0 due to critical bug"
6. Review and roll out
```

**iOS:**
```
Note: Cannot rollback app versions on App Store
Workaround:
1. Upload previous version as new version (increment build number)
2. Submit for expedited review (if critical bug)
3. Or: Server-side feature flags to disable broken features
```

### 8.2 Backend Rollback

**Automatic Rollback (if error rate >1%):**
```bash
#!/bin/bash
# scripts/check-error-rate.sh

ERROR_RATE=$(gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" \
  --limit 100 --format json | jq '. | length')

if [ $ERROR_RATE -gt 1 ]; then
  echo "Error rate too high ($ERROR_RATE%), rolling back..."
  gcloud run services update-traffic rf-shield-api-prod --to-revisions PREVIOUS=100
  exit 1
fi
```

**Manual Rollback:**
```bash
# List revisions
gcloud run revisions list --service rf-shield-api-prod

# Rollback to previous
gcloud run services update-traffic rf-shield-api-prod \
  --to-revisions rf-shield-api-prod-00002-xyz=100
```

### 8.3 Database Rollback

**Restore from backup:**
```bash
# List backups
gcloud sql backups list --instance=oui-db-prod

# Restore
gcloud sql backups restore BACKUP_ID \
  --backup-instance=oui-db-prod \
  --backup-project=rf-shield-prod
```

**Rollback migration:**
```bash
npm run migrate:undo
```

---

## 9. Disaster Recovery

### 9.1 Backup Strategy

**Database Backups:**
- Automated daily backups (retained 30 days)
- Point-in-time recovery (7 days)
- Manual backup before major deployments

**Code Backups:**
- GitHub (primary)
- GitLab mirror (secondary)

**Secrets Backups:**
- GCP Secret Manager (encrypted)
- Offline encrypted backup (1Password)

### 9.2 Recovery Procedures

**Scenario 1: Complete Cloud Run Failure**
```bash
# Deploy to different region
gcloud run deploy rf-shield-api-prod \
  --image gcr.io/rf-shield-prod/api:latest \
  --region europe-west1

# Update DNS
# Point api.rfshield.io to new region URL
```

**Scenario 2: Database Corruption**
```bash
# Restore from backup
gcloud sql backups restore LATEST_BACKUP_ID \
  --backup-instance=oui-db-prod

# Verify data integrity
psql $DATABASE_URL -c "SELECT COUNT(*) FROM oui_master;"
```

**Scenario 3: Complete GCP Project Loss**
```bash
# Provision new GCP project
gcloud projects create rf-shield-recovery

# Deploy infrastructure (Terraform)
cd infrastructure/terraform
terraform apply -var="project_id=rf-shield-recovery"

# Restore database from backup
# (requires off-site backup, e.g., AWS S3)

# Deploy backend from Docker image
docker pull gcr.io/rf-shield-prod/api:latest
docker tag gcr.io/rf-shield-prod/api:latest gcr.io/rf-shield-recovery/api:latest
docker push gcr.io/rf-shield-recovery/api:latest

# Update DNS to new project
```

### 9.3 RTO/RPO Targets

**Recovery Time Objective (RTO):**
- Mobile app: 24 hours (submit for review)
- Backend API: 1 hour (redeploy to new region)
- Database: 2 hours (restore from backup)

**Recovery Point Objective (RPO):**
- Database: 24 hours (daily backups)
- Code: 0 (Git commit history)
- User data: 1 hour (Firestore auto-backup)

---

**END OF DEPLOYMENT GUIDE**
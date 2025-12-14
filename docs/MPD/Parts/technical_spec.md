# Technical Specification
# RF Shield - Privacy Protection Platform

**Version:** 1.0  
**Date:** December 14, 2024  
**Author:** Engineering Team  
**Status:** Draft

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Layer                            │
├─────────────────────────────────────────────────────────────┤
│  Mobile App (Android/iOS)                                    │
│  ├── UI Layer (React Native / Native)                        │
│  ├── Business Logic (Kotlin/Swift)                           │
│  ├── Detection Engine                                        │
│  └── Local Database (SQLite)                                 │
└────────────┬────────────────────────────────────────────────┘
             │
             ├─── Bluetooth LE ───┐
             │                     │
             ├─── USB OTG ─────────┤
             │                     │
             └─── REST API ────────┤
                                   │
┌────────────────────────────────┴─────────────────────────────┐
│                    Hardware Layer                             │
├──────────────────────────────────────────────────────────────┤
│  ESP32 Module          RTL-SDR Module      Camera Module      │
│  ├── WiFi Scanner      ├── Wideband SDR   ├── Lens Detector  │
│  ├── BLE Scanner       ├── Demodulator    └── IR Detector    │
│  ├── Sub-GHz (CC1101)  └── FFT Engine                        │
│  ├── GPS Module                                              │
│  └── Data Logger                                             │
│                                                              │
│  Countermeasure Modules                                      │
│  ├── Ultrasonic Jammer                                       │
│  └── IR Flood Light                                          │
└──────────────────────────────────────────────────────────────┘
                                   │
                                   │ HTTPS
                                   │
┌────────────────────────────────┴─────────────────────────────┐
│                     Cloud Layer                               │
├──────────────────────────────────────────────────────────────┤
│  Backend Services (Firebase + Custom)                        │
│  ├── Authentication (Firebase Auth)                          │
│  ├── Database (Firestore + PostgreSQL)                       │
│  ├── Storage (Cloud Storage)                                 │
│  ├── Functions (Cloud Functions)                             │
│  └── Analytics (Firebase Analytics)                          │
│                                                              │
│  APIs & Services                                             │
│  ├── OUI Database Sync                                       │
│  ├── Threat Intelligence Feed                                │
│  ├── Firmware OTA Updates                                    │
│  └── Payment Processing (Stripe)                             │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Component Interactions

**Scan Flow:**
```
1. User initiates scan
   ↓
2. App sends scan command to ESP32 via BLE
   ↓
3. ESP32 performs WiFi/BLE/Sub-GHz scan
   ↓
4. ESP32 sends results back to app
   ↓
5. App queries local OUI database
   ↓
6. App classifies threats (ML model)
   ↓
7. App displays results to user
   ↓
8. (Optional) App syncs to cloud (premium users)
```

**Hardware Module Communication:**
```
App ←─ BLE GATT ─→ ESP32 Module
    {
      "cmd": "scan",
      "type": "wifi",
      "channels": [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    }
    ←─ Response ─
    {
      "devices": [
        {
          "mac": "AA:BB:CC:DD:EE:FF",
          "ssid": "Wyze_Cam_v3",
          "rssi": -45,
          "channel": 6,
          "encryption": "WPA2"
        }
      ]
    }

App ─ USB OTG ─→ RTL-SDR Module
    (librtlsdr commands)
    
App ←─ Camera API ─→ Phone Camera + ML Model
    (TensorFlow Lite inference)
```

### 1.3 Technology Stack

**Mobile App:**
- **Android:** Kotlin, Jetpack Compose, Room DB, Retrofit
- **iOS:** Swift, SwiftUI, Core Data, Alamofire
- **Cross-platform consideration:** React Native (evaluated, rejected due to BLE/USB limitations)

**Backend:**
- **Primary:** Firebase (Auth, Firestore, Storage, Functions)
- **Database:** PostgreSQL (OUI database, analytics)
- **API:** Node.js + Express (custom endpoints)
- **Hosting:** Google Cloud Platform (GCP)
- **CDN:** Cloudflare (firmware binaries, assets)

**Hardware:**
- **ESP32:** Arduino/PlatformIO, C++
- **Protocols:** BLE GATT, UART, SPI, I2C
- **OTA:** ESP32 OTA library

**ML/AI:**
- **Framework:** TensorFlow Lite
- **Models:** MobileNetV3 (lens classifier), LSTM (signal classifier)
- **Training:** Python + TensorFlow, Google Colab

---

## 2. Data Models

### 2.1 Mobile App Database (SQLite)

**Schema Version:** 1.0

#### Table: `scans`
```sql
CREATE TABLE scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,           -- Unix timestamp
    location_lat REAL,                    -- GPS latitude (optional)
    location_lon REAL,                    -- GPS longitude (optional)
    location_name TEXT,                   -- User-provided name (e.g., "Hotel Room 302")
    scan_type TEXT NOT NULL,              -- 'quick', 'full', 'continuous'
    duration INTEGER NOT NULL,            -- Scan duration in seconds
    threats_found INTEGER NOT NULL,       -- Count of threats
    synced_to_cloud INTEGER DEFAULT 0,    -- 0 = not synced, 1 = synced
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

CREATE INDEX idx_scans_timestamp ON scans(timestamp);
CREATE INDEX idx_scans_synced ON scans(synced_to_cloud);
```

#### Table: `detected_devices`
```sql
CREATE TABLE detected_devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id INTEGER NOT NULL,             -- Foreign key to scans
    device_type TEXT NOT NULL,            -- 'wifi', 'ble', 'subghz', 'cellular'
    mac_address TEXT,                     -- MAC address (if applicable)
    uuid TEXT,                            -- UUID (for BLE)
    name TEXT,                            -- Device name (SSID, BLE name, etc.)
    manufacturer TEXT,                    -- From OUI lookup
    model TEXT,                           -- Device model (if identified)
    rssi INTEGER,                         -- Signal strength in dBm
    frequency INTEGER,                    -- Frequency in Hz (for RF devices)
    channel INTEGER,                      -- WiFi channel or BLE advertising channel
    threat_level TEXT NOT NULL,           -- 'safe', 'investigate', 'threat'
    threat_reason TEXT,                   -- Why it's flagged (e.g., "Camera OUI detected")
    first_seen INTEGER NOT NULL,          -- Unix timestamp
    last_seen INTEGER NOT NULL,           -- Unix timestamp
    metadata TEXT,                        -- JSON blob for additional data
    created_at INTEGER NOT NULL,
    
    FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE
);

CREATE INDEX idx_devices_scan ON detected_devices(scan_id);
CREATE INDEX idx_devices_mac ON detected_devices(mac_address);
CREATE INDEX idx_devices_threat ON detected_devices(threat_level);
```

#### Table: `oui_database`
```sql
CREATE TABLE oui_database (
    oui TEXT PRIMARY KEY,                 -- First 6 chars of MAC (AA:BB:CC)
    manufacturer TEXT NOT NULL,           -- Company name
    device_type TEXT,                     -- 'camera', 'tracker', 'router', 'phone', etc.
    threat_category TEXT,                 -- 'surveillance', 'tracking', 'benign'
    confidence REAL,                      -- 0.0 - 1.0 confidence score
    last_updated INTEGER NOT NULL         -- Unix timestamp
);

CREATE INDEX idx_oui_manufacturer ON oui_database(manufacturer);
CREATE INDEX idx_oui_type ON oui_database(device_type);
```

#### Table: `threat_evidence`
```sql
CREATE TABLE threat_evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER NOT NULL,           -- Foreign key to detected_devices
    evidence_type TEXT NOT NULL,          -- 'photo', 'video', 'audio', 'note'
    file_path TEXT,                       -- Local file path (if photo/video)
    content TEXT,                         -- Text content (if note)
    created_at INTEGER NOT NULL,
    
    FOREIGN KEY (device_id) REFERENCES detected_devices(id) ON DELETE CASCADE
);
```

#### Table: `user_settings`
```sql
CREATE TABLE user_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at INTEGER NOT NULL
);

-- Example settings:
-- key: 'premium_status', value: '1' (boolean as integer)
-- key: 'monitoring_enabled', value: '1'
-- key: 'scan_interval', value: '300' (seconds)
-- key: 'threat_notifications', value: '1'
```

### 2.2 Cloud Database (Firestore)

#### Collection: `users`
```javascript
{
  uid: "string",                          // Firebase Auth UID
  email: "string",
  premium: {
    active: boolean,
    tier: "free" | "premium" | "pro",
    expires_at: timestamp,
    stripe_customer_id: "string"
  },
  hardware_modules: [
    {
      module_id: "string",                // Unique device ID (MAC or serial)
      type: "esp32" | "rtl_sdr" | "camera",
      paired_at: timestamp,
      last_seen: timestamp
    }
  ],
  settings: {
    sync_enabled: boolean,
    notification_preferences: object
  },
  created_at: timestamp,
  updated_at: timestamp
}
```

#### Collection: `scan_history` (subcollection under `users/{uid}`)
```javascript
{
  scan_id: "string",                      // UUID
  timestamp: timestamp,
  location: geopoint,                     // Firestore GeoPoint
  location_name: "string",
  scan_type: "quick" | "full" | "continuous",
  threats: [
    {
      device_type: "wifi" | "ble" | "subghz",
      mac: "string",
      name: "string",
      manufacturer: "string",
      threat_level: "safe" | "investigate" | "threat",
      rssi: number
    }
  ],
  encrypted_data: "string"                // E2E encrypted scan details
}
```

#### Collection: `oui_updates`
```javascript
{
  version: number,                        // Incremental version
  entries: [
    {
      oui: "string",
      manufacturer: "string",
      device_type: "string",
      threat_category: "string",
      confidence: number
    }
  ],
  delta_from_version: number,             // For incremental updates
  published_at: timestamp
}
```

#### Collection: `threat_intelligence` (crowdsourced)
```javascript
{
  report_id: "string",
  user_id: "string" (anonymized),
  device: {
    mac_prefix: "string",                 // First 6 chars only (privacy)
    name: "string",
    type: "camera" | "bug" | "tracker" | "benign"
  },
  location: {
    country: "string",                    // Country-level only (privacy)
    city: "string"                        // City-level only
  },
  votes: {
    confirmed: number,                    // Community votes
    rejected: number
  },
  status: "pending" | "verified" | "rejected",
  created_at: timestamp
}
```

### 2.3 PostgreSQL (Analytics & OUI Master Database)

#### Table: `oui_master`
```sql
CREATE TABLE oui_master (
    oui CHAR(8) PRIMARY KEY,              -- AA:BB:CC format
    manufacturer VARCHAR(255) NOT NULL,
    device_type VARCHAR(50),
    threat_category VARCHAR(50),
    confidence DECIMAL(3,2),              -- 0.00 - 1.00
    source VARCHAR(50),                   -- 'ieee', 'crowdsourced', 'manual'
    last_updated TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_manufacturer (manufacturer),
    INDEX idx_device_type (device_type),
    INDEX idx_threat (threat_category)
);
```

#### Table: `analytics_events`
```sql
CREATE TABLE analytics_events (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID,                         -- Anonymized user ID
    event_type VARCHAR(50) NOT NULL,      -- 'scan_started', 'threat_found', etc.
    event_data JSONB,                     -- Flexible event metadata
    platform VARCHAR(20),                 -- 'android', 'ios'
    app_version VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_event_type (event_type),
    INDEX idx_created_at (created_at),
    INDEX idx_user_id (user_id)
);
```

#### Table: `hardware_telemetry`
```sql
CREATE TABLE hardware_telemetry (
    id BIGSERIAL PRIMARY KEY,
    module_id VARCHAR(50) NOT NULL,       -- Unique device ID
    module_type VARCHAR(20),              -- 'esp32', 'rtl_sdr', etc.
    firmware_version VARCHAR(20),
    battery_level INTEGER,                -- Percentage
    temperature INTEGER,                  -- Celsius
    uptime INTEGER,                       -- Seconds
    error_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_module_id (module_id),
    INDEX idx_created_at (created_at)
);
```

---

## 3. API Specifications

### 3.1 REST API (Backend)

**Base URL:** `https://api.rfshield.io/v1`

**Authentication:** Bearer token (Firebase JWT)

#### Endpoint: `POST /scans/sync`
**Description:** Sync scan history to cloud (premium users only)

**Request:**
```json
{
  "scans": [
    {
      "scan_id": "uuid-v4",
      "timestamp": 1702587600,
      "location": {
        "lat": 29.7604,
        "lon": -95.3698
      },
      "location_name": "Hotel Room 302",
      "threats": [
        {
          "device_type": "wifi",
          "mac": "AA:BB:CC:DD:EE:FF",
          "name": "Wyze_Cam_v3",
          "manufacturer": "Wyze Labs",
          "threat_level": "threat",
          "rssi": -45
        }
      ],
      "encrypted_data": "base64-encrypted-blob"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "synced_count": 1,
  "failed": []
}
```

**Errors:**
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User is not premium
- `429 Too Many Requests`: Rate limit exceeded

---

#### Endpoint: `GET /oui/updates`
**Description:** Get OUI database updates

**Query Parameters:**
- `since_version`: (integer) Last known version, returns delta
- `full`: (boolean) If true, returns full database

**Response:**
```json
{
  "version": 1234,
  "delta_from": 1233,
  "entries": [
    {
      "oui": "AA:BB:CC",
      "manufacturer": "Wyze Labs",
      "device_type": "camera",
      "threat_category": "surveillance",
      "confidence": 0.95
    }
  ],
  "next_update_at": 1702674000
}
```

---

#### Endpoint: `POST /threats/report`
**Description:** Submit crowdsourced threat intelligence

**Request:**
```json
{
  "device": {
    "mac_prefix": "AA:BB:CC",
    "name": "Unknown Device",
    "type": "camera"
  },
  "location": {
    "country": "US",
    "city": "Houston"
  },
  "evidence": {
    "confidence": 0.8,
    "detection_method": "lens_finder",
    "notes": "Found hidden in smoke detector"
  }
}
```

**Response:**
```json
{
  "success": true,
  "report_id": "uuid-v4",
  "status": "pending",
  "message": "Report submitted for community verification"
}
```

---

#### Endpoint: `GET /firmware/latest`
**Description:** Check for firmware updates

**Query Parameters:**
- `module_type`: 'esp32' | 'ultrasonic' | 'ir_flood'
- `current_version`: Semantic version (e.g., '1.2.3')

**Response:**
```json
{
  "update_available": true,
  "latest_version": "1.3.0",
  "release_notes": "Added 5 GHz WiFi support",
  "download_url": "https://cdn.rfshield.io/firmware/esp32-1.3.0.bin",
  "sha256": "abc123...",
  "size_bytes": 1048576,
  "mandatory": false
}
```

---

#### Endpoint: `POST /tscm/referral`
**Description:** Submit TSCM professional sweep request

**Request:**
```json
{
  "location": {
    "address": "123 Main St, Houston, TX 77002",
    "type": "hotel" | "home" | "office"
  },
  "urgency": "low" | "medium" | "high",
  "scan_report_id": "uuid-v4",
  "contact": {
    "email": "user@example.com",
    "phone": "+1-555-0100"
  }
}
```

**Response:**
```json
{
  "success": true,
  "referral_id": "uuid-v4",
  "matched_firms": [
    {
      "name": "Houston TSCM Services",
      "distance_km": 3.2,
      "rating": 4.8,
      "price_range": "$2000-$5000",
      "availability": "Next available: 2024-12-20"
    }
  ],
  "message": "Request sent to 3 nearby TSCM firms"
}
```

---

### 3.2 Bluetooth LE GATT Protocol (ESP32 Module)

**Service UUID:** `0000fff0-0000-1000-8000-00805f9b34fb`

**Characteristics:**

#### Characteristic: Command (Write)
**UUID:** `0000fff1-0000-1000-8000-00805f9b34fb`  
**Properties:** Write  
**Description:** Send commands to ESP32

**Command Format (JSON):**
```json
{
  "cmd": "scan" | "stop" | "configure" | "status",
  "params": {
    // Command-specific parameters
  }
}
```

**Example: WiFi Scan**
```json
{
  "cmd": "scan",
  "params": {
    "type": "wifi",
    "channels": [1, 6, 11],
    "duration_ms": 5000
  }
}
```

**Example: BLE Scan**
```json
{
  "cmd": "scan",
  "params": {
    "type": "ble",
    "duration_ms": 10000,
    "filter_airtags": true
  }
}
```

**Example: Sub-GHz Scan**
```json
{
  "cmd": "scan",
  "params": {
    "type": "subghz",
    "frequencies": [315000000, 433920000],  // Hz
    "bandwidth": 200000,                      // 200 kHz
    "duration_ms": 30000
  }
}
```

---

#### Characteristic: Response (Notify)
**UUID:** `0000fff2-0000-1000-8000-00805f9b34fb`  
**Properties:** Notify  
**Description:** Receive scan results from ESP32

**Response Format (JSON):**
```json
{
  "status": "success" | "error",
  "data": {
    // Response-specific data
  },
  "timestamp": 1702587600
}
```

**Example: WiFi Scan Response**
```json
{
  "status": "success",
  "data": {
    "type": "wifi",
    "devices": [
      {
        "bssid": "AA:BB:CC:DD:EE:FF",
        "ssid": "Wyze_Cam_v3",
        "rssi": -45,
        "channel": 6,
        "encryption": "WPA2-PSK",
        "hidden": false
      },
      {
        "bssid": "11:22:33:44:55:66",
        "ssid": "",
        "rssi": -67,
        "channel": 11,
        "encryption": "OPEN",
        "hidden": true
      }
    ],
    "scan_duration_ms": 4823
  },
  "timestamp": 1702587605
}
```

**Example: BLE Scan Response**
```json
{
  "status": "success",
  "data": {
    "type": "ble",
    "devices": [
      {
        "mac": "AA:BB:CC:DD:EE:FF",
        "name": "AirTag",
        "rssi": -52,
        "uuid": "0000FD74-0000-1000-8000-00805F9B34FB",
        "manufacturer_data": "4c0012190...",
        "is_airtag": true,
        "separated_from_owner": true
      }
    ],
    "scan_duration_ms": 10124
  },
  "timestamp": 1702587615
}
```

---

#### Characteristic: Status (Read/Notify)
**UUID:** `0000fff3-0000-1000-8000-00805f9b34fb`  
**Properties:** Read, Notify  
**Description:** ESP32 module status

**Status Format:**
```json
{
  "firmware_version": "1.2.3",
  "battery_level": 85,          // Percentage
  "temperature": 42,            // Celsius
  "uptime_seconds": 3600,
  "wifi_connected": true,
  "gps_locked": true,
  "sd_card_free_mb": 28672,
  "errors": []
}
```

---

### 3.3 Tool Communication Protocol (Computer Use)

**Note:** If RF Shield app has MCP/Computer Use access (like via Claude.ai integration), these are the tool definitions.

#### Tool: `rf_shield_scan`
**Description:** Initiate a threat scan

**Parameters:**
```json
{
  "scan_type": "quick" | "full" | "continuous",
  "modules": ["phone", "esp32", "rtl_sdr", "camera"],
  "location_name": "string (optional)"
}
```

**Returns:**
```json
{
  "scan_id": "uuid",
  "threats_found": 2,
  "devices": [
    {
      "name": "Wyze Cam v3",
      "type": "wifi_camera",
      "threat_level": "high",
      "rssi": -45,
      "location_estimate": "bedroom"
    }
  ],
  "duration_seconds": 58
}
```

---

#### Tool: `rf_shield_locate_device`
**Description:** Guide user to physical location of threat

**Parameters:**
```json
{
  "device_id": "string",
  "scan_id": "string"
}
```

**Returns:**
```json
{
  "rssi": -45,
  "distance_estimate_meters": 2.3,
  "direction": "Move closer - signal strengthening",
  "confidence": 0.8
}
```

---

#### Tool: `rf_shield_activate_countermeasure`
**Description:** Activate countermeasure module

**Parameters:**
```json
{
  "countermeasure": "ultrasonic_jammer" | "ir_flood",
  "mode": "continuous" | "pulse",
  "duration_minutes": 120
}
```

**Returns:**
```json
{
  "success": true,
  "active": true,
  "estimated_battery_life_minutes": 90
}
```

---

## 4. Security Architecture

### 4.1 Authentication & Authorization

**User Authentication:**
- Firebase Authentication (email/password, OAuth)
- JWT tokens (1-hour expiry)
- Refresh tokens (30-day expiry, stored securely)
- Biometric authentication (optional, device-level)

**Authorization Tiers:**
```
Free Tier:
  - 3 scans per day
  - Phone sensors only
  - No cloud sync
  - Ads

Premium Tier ($79/year):
  - Unlimited scans
  - Hardware module support
  - Cloud sync
  - PDF export
  - No ads

Pro Tier ($999 one-time):
  - All premium features
  - TSCM referral
  - Remote consultation
  - Priority support
```

### 4.2 Data Encryption

**At Rest:**
- **Mobile:** AES-256 encryption for SQLite database (SQLCipher)
- **Cloud:** Firestore encryption by default (Google-managed keys)
- **E2E Encrypted:** Scan history (user's password-derived key, PBKDF2)

**In Transit:**
- **HTTPS:** TLS 1.3 for all API calls
- **Certificate Pinning:** Prevent MITM attacks
- **BLE:** Encrypted pairing (BLE Secure Connections, AES-128)

**Key Management:**
- User encryption key: Derived from password (PBKDF2, 100k iterations)
- Stored in: Android Keystore / iOS Keychain
- Never transmitted to server

### 4.3 Privacy

**Data Collection (Minimal):**
- **Collected:** Email, scan timestamps, device types (anonymized)
- **Not Collected:** GPS coordinates, photos (unless user exports), personal data

**Anonymization:**
- User IDs: Hashed before analytics
- Location: Country/city level only (never precise GPS)
- MAC addresses: Truncated to OUI (first 6 chars) in reports

**GDPR Compliance:**
- Right to access: API endpoint to download all user data
- Right to deletion: Delete account → purge all data within 30 days
- Data retention: 90 days for free tier, 1 year for premium
- Cookie consent: Required for web dashboard

### 4.4 Firmware Security

**Signed Binaries:**
- ESP32 firmware signed with RSA-4096
- App verifies signature before OTA update
- Prevents: Malicious firmware injection

**Secure Boot (ESP32):**
- Enable ESP32 secure boot (flash encryption)
- Prevents: Physical dumping of firmware

**Update Mechanism:**
- Over-the-Air (OTA) via BLE or WiFi
- Rollback on failure (dual partition scheme)
- Version checking (semantic versioning)

### 4.5 Threat Model

**Threats Mitigated:**
1. **Malicious Firmware:** Signed binaries, secure boot
2. **MITM Attacks:** Certificate pinning, TLS 1.3
3. **Data Theft:** Encryption at rest, E2E for cloud sync
4. **Account Takeover:** 2FA (optional), strong password requirements
5. **Hardware Tampering:** Secure element (future), tamper detection

**Threats Not Mitigated:**
1. **Physical Device Access:** User responsible for device security
2. **Zero-Day Exploits:** Rely on OS security patches
3. **Social Engineering:** User education, phishing warnings

### 4.6 Secure Coding Practices

**Mobile App:**
- Input validation (all user inputs, API responses)
- No hardcoded secrets (use environment variables)
- Obfuscation (ProGuard for Android, obfuscation for iOS)
- Regular dependency updates (automated via Dependabot)

**Backend:**
- SQL injection prevention (parameterized queries)
- XSS prevention (sanitize all inputs)
- Rate limiting (100 req/min per user)
- DDoS protection (Cloudflare)

**Hardware:**
- Bounds checking (prevent buffer overflows)
- Watchdog timer (auto-reset on freeze)
- Fail-safe defaults (secure state on error)

---

## 5. Performance Requirements

### 5.1 Mobile App Performance

**App Launch:**
- Cold start: <2 seconds
- Warm start: <500 ms

**Scan Performance:**
- Quick scan (phone only): <60 seconds
- Full scan (all modules): <5 minutes
- Device locator: Real-time updates (>10 Hz)

**UI Responsiveness:**
- Button tap → action: <100 ms
- Scan results display: <500 ms
- Scroll/animation: 60 FPS

**Memory Usage:**
- Idle: <100 MB RAM
- Active scan: <250 MB RAM
- Background monitoring: <50 MB RAM

**Battery Impact:**
- Quick scan: <3% battery
- 1-hour continuous monitoring: <5% battery
- Background sync: <1% per day

### 5.2 Backend Performance

**API Latency:**
- GET requests: <100 ms (p95)
- POST requests: <200 ms (p95)
- Batch operations: <500 ms (p95)

**Database Queries:**
- Read: <50 ms (p95)
- Write: <100 ms (p95)
- Complex queries (analytics): <1 second

**Throughput:**
- Support 100 requests/second (Year 1)
- Support 1,000 requests/second (Year 3)
- Auto-scaling enabled (GCP)

### 5.3 Hardware Module Performance

**ESP32 Scan Times:**
- WiFi scan (all channels): <3 seconds
- BLE scan: <10 seconds
- Sub-GHz sweep (315/433 MHz): <30 seconds

**RTL-SDR Scan Times:**
- Wideband spectrum (500 kHz - 1.7 GHz): <10 seconds
- Targeted scan (camera bands): <5 seconds

**Camera Module:**
- Lens detection: Real-time (15-30 FPS)
- ML inference: <100 ms per frame

**Battery Life:**
- ESP32 (continuous scanning): 8 hours
- Ultrasonic jammer: 2 hours
- IR flood: 1 hour (with 5000 mAh power bank)

### 5.4 Scalability

**User Growth:**
- Year 1: 100k MAU (monthly active users)
- Year 3: 1M MAU
- Database: Handle 10M scan records

**Cloud Infrastructure:**
- Firebase: Firestore scales automatically
- PostgreSQL: Vertical scaling (32 vCPU, 128 GB RAM)
- CDN: Cloudflare (99.9% uptime, global edge caching)

**Cost Optimization:**
- Firebase: Free tier → $25/month (Year 1) → $500/month (Year 3)
- PostgreSQL: $100/month (Year 1) → $1,000/month (Year 3)
- Total cloud costs: <10% of revenue

---

## 6. Testing Strategy

### 6.1 Unit Testing

**Mobile App:**
- Framework: JUnit (Android), XCTest (iOS)
- Coverage target: 80%+
- Focus: Business logic, detection algorithms, data models

**Backend:**
- Framework: Jest (Node.js)
- Coverage target: 85%+
- Focus: API endpoints, database queries, authentication

**Hardware:**
- Framework: Unity (PlatformIO)
- Coverage target: 70%+
- Focus: Scanning logic, BLE communication, OTA updates

### 6.2 Integration Testing

**Mobile ↔ Hardware:**
- Test BLE pairing, scanning, data transfer
- Automated tests with mock ESP32 (BLE peripheral simulator)

**Mobile ↔ Backend:**
- Test API calls, authentication, data sync
- Automated tests with Firebase emulator

**Hardware ↔ Backend:**
- Test firmware OTA updates
- Test telemetry reporting

### 6.3 End-to-End Testing

**User Flows:**
1. New user signup → scan → detect threat → export report
2. Premium user login → sync history → view on web dashboard
3. Hardware module pairing → full scan → countermeasure activation

**Tools:**
- Appium (mobile UI automation)
- Selenium (web dashboard)
- Custom scripts (hardware testing)

### 6.4 Performance Testing

**Load Testing:**
- Simulate 10,000 concurrent users (Year 1 peak)
- Tool: Apache JMeter, Gatling
- Metrics: API latency, error rate, throughput

**Stress Testing:**
- Push backend to failure point (10x expected load)
- Identify bottlenecks (database, API, network)

**Battery Testing:**
- Continuous scanning for 24 hours (measure battery drain)
- Background monitoring for 1 week (measure impact)

### 6.5 Security Testing

**Penetration Testing:**
- Mobile app: Static analysis (MobSF), dynamic analysis (Frida)
- Backend: OWASP Top 10 vulnerabilities
- Hardware: Firmware reverse engineering attempts

**Vulnerability Scanning:**
- Automated: Snyk (dependency scanning)
- Manual: Annual third-party pentest ($5k-10k)

**Bug Bounty:**
- Launch bug bounty program (HackerOne, Bugcrowd)
- Payouts: $100-5,000 depending on severity

### 6.6 User Acceptance Testing (UAT)

**Beta Program:**
- Recruit 50-100 beta testers (privacy advocates, tech enthusiasts)
- Duration: 4-6 weeks before launch
- Feedback: In-app surveys, focus groups

**Metrics:**
- Task completion rate: >90%
- User satisfaction (CSAT): 4.5+/5
- Critical bugs found: <5 (P0 severity)

---

## 7. Deployment Architecture

### 7.1 Mobile App Deployment

**Android:**
- **Distribution:** Google Play Store
- **Beta:** Google Play Beta track (internal, closed, open)
- **Release Cadence:** Every 2 weeks (sprints)
- **Versioning:** Semantic (e.g., 1.2.3)

**iOS:**
- **Distribution:** Apple App Store
- **Beta:** TestFlight (internal, external)
- **Release Cadence:** Every 2 weeks
- **Versioning:** Semantic (e.g., 1.2.3)

**CI/CD Pipeline:**
```
GitHub Push → GitHub Actions
  ↓
Unit Tests → Integration Tests
  ↓
Build APK/IPA (signed)
  ↓
Upload to Play Store/App Store (beta track)
  ↓
Automated tests on Firebase Test Lab
  ↓
Manual QA approval
  ↓
Promote to production
```

### 7.2 Backend Deployment

**Infrastructure:**
- **Hosting:** Google Cloud Platform (GCP)
- **Regions:** us-central1 (primary), europe-west1 (secondary)
- **Database:** Cloud SQL (PostgreSQL), Firestore
- **Storage:** Cloud Storage (firmware binaries, user exports)
- **Functions:** Cloud Functions (serverless)

**CI/CD Pipeline:**
```
GitHub Push → Cloud Build
  ↓
Unit Tests → Integration Tests
  ↓
Build Docker image
  ↓
Push to Container Registry
  ↓
Deploy to Cloud Run (staging)
  ↓
Smoke tests
  ↓
Manual approval
  ↓
Deploy to Cloud Run (production)
  ↓
Health check monitoring
```

**Blue-Green Deployment:**
- Zero-downtime deployments
- Instant rollback capability

### 7.3 Hardware Firmware Deployment

**OTA Update Process:**
```
Firmware commit → Build binary → Sign with RSA key
  ↓
Upload to CDN (Cloudflare)
  ↓
Update /firmware/latest API endpoint
  ↓
Mobile app checks for updates
  ↓
User approves update
  ↓
App downloads binary, verifies signature
  ↓
App sends binary to ESP32 via BLE
  ↓
ESP32 writes to OTA partition
  ↓
ESP32 reboots into new firmware
  ↓
Rollback if boot fails (watchdog timer)
```

**Staged Rollout:**
- 10% of devices (Day 1)
- 50% of devices (Day 3, if no issues)
- 100% of devices (Day 7)

### 7.4 Monitoring & Observability

**Application Performance Monitoring (APM):**
- Firebase Performance Monitoring (mobile)
- Google Cloud Monitoring (backend)
- Custom dashboards (Grafana)

**Error Tracking:**
- Firebase Crashlytics (mobile crashes)
- Sentry (backend errors)
- Custom alerts (PagerDuty)

**Logging:**
- Centralized logging (Cloud Logging)
- Retention: 30 days (hot), 1 year (cold storage)
- Log levels: DEBUG, INFO, WARN, ERROR, FATAL

**Metrics:**
- API latency (p50, p95, p99)
- Error rate (4xx, 5xx)
- Throughput (requests/second)
- Database query time
- Mobile app crash rate
- Hardware module battery life

**Alerts:**
- Critical: API down, database down, >5% error rate
- Warning: High latency (>500 ms p95), low disk space (<20%)
- Info: New version deployed, unusual traffic spike

---

## 8. Infrastructure as Code (IaC)

### 8.1 Terraform Configuration

**GCP Resources:**
```hcl
# Cloud SQL (PostgreSQL)
resource "google_sql_database_instance" "oui_database" {
  name             = "rf-shield-oui-db"
  database_version = "POSTGRES_14"
  region           = "us-central1"

  settings {
    tier = "db-custom-4-16384"  # 4 vCPU, 16 GB RAM
    
    backup_configuration {
      enabled            = true
      start_time         = "03:00"
      point_in_time_recovery_enabled = true
    }
    
    ip_configuration {
      ipv4_enabled = false
      private_network = google_compute_network.vpc.id
    }
  }
}

# Cloud Storage (Firmware Binaries)
resource "google_storage_bucket" "firmware" {
  name     = "rf-shield-firmware"
  location = "US"
  
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 90  # Delete old firmware after 90 days
    }
  }
  
  versioning {
    enabled = true
  }
}

# Cloud Run (API Backend)
resource "google_cloud_run_service" "api" {
  name     = "rf-shield-api"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/rf-shield/api:latest"
        
        resources {
          limits = {
            cpu    = "2"
            memory = "1Gi"
          }
        }
        
        env {
          name  = "DATABASE_URL"
          value = google_sql_database_instance.oui_database.connection_name
        }
      }
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "100"
      }
    }
  }
}
```

### 8.2 Kubernetes (Optional, for future scale)

**Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rf-shield-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rf-shield-api
  template:
    metadata:
      labels:
        app: rf-shield-api
    spec:
      containers:
      - name: api
        image: gcr.io/rf-shield/api:1.0.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

---

## 9. Development Environment Setup

### 9.1 Mobile App (Android)

**Prerequisites:**
- Android Studio Hedgehog (2023.1.1) or newer
- JDK 17
- Android SDK (API 28+)
- Kotlin 1.9+

**Setup Steps:**
```bash
# Clone repository
git clone https://github.com/rf-shield/mobile-android.git
cd mobile-android

# Install dependencies
./gradlew build

# Run tests
./gradlew test

# Run on emulator
./gradlew installDebug
adb shell am start -n com.rfshield.app/.MainActivity

# Or run from Android Studio
# Open project → Run 'app'
```

**Environment Variables (.env):**
```
FIREBASE_API_KEY=AIza...
FIREBASE_PROJECT_ID=rf-shield-prod
STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### 9.2 Mobile App (iOS)

**Prerequisites:**
- Xcode 15.0+
- Swift 5.9+
- CocoaPods or Swift Package Manager

**Setup Steps:**
```bash
# Clone repository
git clone https://github.com/rf-shield/mobile-ios.git
cd mobile-ios

# Install dependencies
pod install
# Or if using SPM, dependencies auto-resolve in Xcode

# Open workspace
open RFShield.xcworkspace

# Run from Xcode
# Select simulator → Run
```

### 9.3 Backend (Node.js)

**Prerequisites:**
- Node.js 20+
- npm or yarn
- PostgreSQL 14+ (local or Docker)

**Setup Steps:**
```bash
# Clone repository
git clone https://github.com/rf-shield/backend.git
cd backend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run database migrations
npm run migrate

# Start development server
npm run dev

# Runs on http://localhost:3000
```

**Environment Variables (.env):**
```
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost:5432/rfshield
FIREBASE_PROJECT_ID=rf-shield-dev
STRIPE_SECRET_KEY=sk_test_...
JWT_SECRET=your-secret-key
```

### 9.4 Hardware Firmware (ESP32)

**Prerequisites:**
- PlatformIO IDE (VS Code extension) or Arduino IDE 2.0+
- USB-C cable for programming

**Setup Steps:**
```bash
# Clone repository
git clone https://github.com/rf-shield/firmware-esp32.git
cd firmware-esp32

# Install PlatformIO
# (VS Code: Install "PlatformIO IDE" extension)

# Build firmware
pio run

# Upload to ESP32
pio run --target upload

# Monitor serial output
pio device monitor
```

**platformio.ini:**
```ini
[env:esp32s3]
platform = espressif32
board = esp32-s3-devkitc-1
framework = arduino

lib_deps =
    bblanchon/ArduinoJson @ ^6.21.0
    h2zero/NimBLE-Arduino @ ^1.4.1
    smartrc-cc/CC1101 @ ^1.0.0
    
build_flags =
    -DCORE_DEBUG_LEVEL=3
    -DBOARD_HAS_PSRAM
    
monitor_speed = 115200
```

---

## 10. Dependencies & Third-Party Libraries

### 10.1 Mobile App (Android)

**Core:**
- Kotlin 1.9.20
- AndroidX Core 1.12.0
- Jetpack Compose 1.5.4

**Networking:**
- Retrofit 2.9.0 (REST API client)
- OkHttp 4.12.0 (HTTP client)
- Gson 2.10.1 (JSON parsing)

**Database:**
- Room 2.6.0 (SQLite abstraction)
- SQLCipher 4.5.4 (encryption)

**Bluetooth:**
- Android BLE APIs (built-in)
- Nordic BLE Library 2.6.1 (optional, better API)

**USB:**
- usb-serial-for-android 3.6.0 (RTL-SDR)

**ML:**
- TensorFlow Lite 2.14.0
- ML Kit (optional, for on-device models)

**Firebase:**
- Firebase Auth 22.3.0
- Firebase Firestore 24.9.1
- Firebase Storage 20.3.0
- Firebase Analytics 21.5.0
- Firebase Crashlytics 18.6.0

**UI:**
- Material Design 3 (Jetpack Compose)
- Coil 2.5.0 (image loading)

**Utilities:**
- Timber 5.0.1 (logging)
- Hilt 2.48.1 (dependency injection)

### 10.2 Mobile App (iOS)

**Core:**
- Swift 5.9
- SwiftUI
- Combine

**Networking:**
- Alamofire 5.8.0 (HTTP client)
- SwiftyJSON 5.0.1 (JSON parsing)

**Database:**
- Core Data (built-in)
- SQLCipher 4.5.5 (encryption)

**Bluetooth:**
- CoreBluetooth (built-in)

**ML:**
- Core ML (built-in)
- TensorFlow Lite Swift 2.14.0

**Firebase:**
- FirebaseAuth 10.18.0
- FirebaseFirestore 10.18.0
- FirebaseStorage 10.18.0
- FirebaseAnalytics 10.18.0
- FirebaseCrashlytics 10.18.0

**UI:**
- Charts (Swift Charts, built-in iOS 16+)
- Kingfisher 7.10.0 (image loading)

**Utilities:**
- SwiftyBeaver 2.0.0 (logging)

### 10.3 Backend (Node.js)

**Core:**
- Node.js 20.10.0
- Express 4.18.2
- TypeScript 5.3.3

**Database:**
- pg (PostgreSQL client) 8.11.3
- Sequelize 6.35.0 (ORM)
- Firebase Admin SDK 12.0.0

**Authentication:**
- jsonwebtoken 9.0.2
- bcrypt 5.1.1

**Utilities:**
- dotenv 16.3.1 (environment variables)
- helmet 7.1.0 (security headers)
- cors 2.8.5
- compression 1.7.4
- winston 3.11.0 (logging)

**Payment:**
- stripe 14.10.0

**Testing:**
- Jest 29.7.0
- Supertest 6.3.3

### 10.4 Hardware Firmware (ESP32)

**Core:**
- Arduino Core for ESP32 2.0.14
- ESP-IDF 4.4.6 (underlying framework)

**Libraries:**
- ArduinoJson 6.21.4 (JSON parsing)
- NimBLE-Arduino 1.4.1 (Bluetooth Low Energy)
- CC1101 1.0.0 (Sub-GHz radio)
- TinyGPS++ 1.0.3 (GPS parsing)
- SD 2.0.0 (SD card logging)

---

## 11. Code Examples

### 11.1 Mobile App: WiFi Scanner (Android)

```kotlin
class WiFiScanner(private val context: Context) {
    
    private val wifiManager = context.getSystemService(Context.WIFI_SERVICE) as WifiManager
    private val ouiDatabase = OUIDatabase(context)
    
    suspend fun scanWiFiNetworks(): List<DetectedDevice> = withContext(Dispatchers.IO) {
        val devices = mutableListOf<DetectedDevice>()
        
        // Request permission if not granted
        if (!hasLocationPermission()) {
            throw SecurityException("Location permission required for WiFi scanning")
        }
        
        // Start WiFi scan
        val scanStarted = wifiManager.startScan()
        if (!scanStarted) {
            Log.w(TAG, "WiFi scan failed to start")
            return@withContext emptyList()
        }
        
        // Wait for scan to complete
        delay(3000) // WiFi scan takes ~2-3 seconds
        
        // Get scan results
        val scanResults = wifiManager.scanResults
        
        for (result in scanResults) {
            val oui = result.BSSID.substring(0, 8).uppercase()
            val deviceInfo = ouiDatabase.lookup(oui)
            
            val device = DetectedDevice(
                deviceType = DeviceType.WIFI,
                macAddress = result.BSSID,
                name = result.SSID.ifEmpty { "<Hidden Network>" },
                manufacturer = deviceInfo?.manufacturer ?: "Unknown",
                model = deviceInfo?.model,
                rssi = result.level,
                frequency = result.frequency,
                channel = frequencyToChannel(result.frequency),
                threatLevel = assessThreatLevel(deviceInfo),
                threatReason = getThreatReason(deviceInfo),
                firstSeen = System.currentTimeMillis(),
                lastSeen = System.currentTimeMillis(),
                metadata = mapOf(
                    "encryption" to getEncryptionType(result),
                    "hidden" to result.SSID.isEmpty()
                )
            )
            
            devices.add(device)
        }
        
        return@withContext devices
    }
    
    private fun assessThreatLevel(deviceInfo: DeviceInfo?): ThreatLevel {
        return when (deviceInfo?.deviceType) {
            "camera" -> ThreatLevel.THREAT
            "tracker" -> ThreatLevel.THREAT
            "router", "phone", "laptop" -> ThreatLevel.SAFE
            else -> ThreatLevel.INVESTIGATE
        }
    }
    
    private fun getThreatReason(deviceInfo: DeviceInfo?): String? {
        return when (deviceInfo?.deviceType) {
            "camera" -> "WiFi camera detected (${deviceInfo.manufacturer})"
            "tracker" -> "GPS tracker detected"
            else -> null
        }
    }
    
    private fun frequencyToChannel(frequencyMhz: Int): Int {
        return when {
            frequencyMhz in 2412..2484 -> (frequencyMhz - 2407) / 5
            frequencyMhz in 5170..5825 -> (frequencyMhz - 5000) / 5
            else -> 0
        }
    }
    
    private fun getEncryptionType(result: ScanResult): String {
        return when {
            result.capabilities.contains("WPA3") -> "WPA3"
            result.capabilities.contains("WPA2") -> "WPA2"
            result.capabilities.contains("WPA") -> "WPA"
            result.capabilities.contains("WEP") -> "WEP"
            else -> "OPEN"
        }
    }
    
    private fun hasLocationPermission(): Boolean {
        return ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.ACCESS_FINE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED
    }
    
    companion object {
        private const val TAG = "WiFiScanner"
    }
}
```

### 11.2 ESP32 Firmware: BLE Scanner

```cpp
#include <NimBLEDevice.h>
#include <ArduinoJson.h>

class BLEScanner {
private:
    NimBLEScan* scanner;
    std::vector<BLEAdvertisedDevice> devices;
    
    static constexpr uint8_t AIRTAG_MFG_ID[] = {0x4C, 0x00};  // Apple
    static constexpr uint8_t AIRTAG_SERVICE_UUID[] = {0x74, 0xFD};
    
public:
    BLEScanner() {
        NimBLEDevice::init("RF-Shield-ESP32");
        scanner = NimBLEDevice::getScan();
        scanner->setActiveScan(true);  // Active scan uses more power but gets more data
        scanner->setInterval(100);
        scanner->setWindow(99);
    }
    
    String scanBLE(int durationSeconds) {
        devices.clear();
        
        // Start scan
        NimBLEScanResults scanResults = scanner->start(durationSeconds, false);
        
        // Process results
        for (int i = 0; i < scanResults.getCount(); i++) {
            NimBLEAdvertisedDevice device = scanResults.getDevice(i);
            devices.push_back(device);
        }
        
        // Clear scan results to free memory
        scanner->clearResults();
        
        // Build JSON response
        return buildJSONResponse();
    }
    
    String buildJSONResponse() {
        StaticJsonDocument<4096> doc;
        doc["status"] = "success";
        doc["timestamp"] = millis();
        
        JsonObject data = doc.createNestedObject("data");
        data["type"] = "ble";
        
        JsonArray devicesArray = data.createNestedArray("devices");
        
        for (const auto& device : devices) {
            JsonObject deviceObj = devicesArray.createObject();
            
            deviceObj["mac"] = device.getAddress().toString().c_str();
            deviceObj["rssi"] = device.getRSSI();
            
            if (device.haveName()) {
                deviceObj["name"] = device.getName().c_str();
            }
            
            // Check if AirTag
            bool isAirTag = false;
            bool separatedFromOwner = false;
            
            if (device.haveManufacturerData()) {
                std::string mfgData = device.getManufacturerData();
                if (mfgData.size() >= 2) {
                    // Check if Apple (0x004C)
                    if (mfgData[0] == AIRTAG_MFG_ID[0] && mfgData[1] == AIRTAG_MFG_ID[1]) {
                        // Check for Nearby Interaction service (AirTag)
                        if (mfgData.size() >= 4 && mfgData[2] == 0x12 && mfgData[3] == 0x19) {
                            isAirTag = true;
                            
                            // Check status byte (offset 4, bit 4 = separated from owner)
                            if (mfgData.size() > 4) {
                                separatedFromOwner = (mfgData[4] & 0x10) != 0;
                            }
                        }
                    }
                }
                
                // Include manufacturer data as hex string
                char mfgHex[mfgData.size() * 2 + 1];
                for (size_t i = 0; i < mfgData.size(); i++) {
                    sprintf(&mfgHex[i * 2], "%02X", mfgData[i]);
                }
                deviceObj["manufacturer_data"] = mfgHex;
            }
            
            deviceObj["is_airtag"] = isAirTag;
            if (isAirTag) {
                deviceObj["separated_from_owner"] = separatedFromOwner;
            }
            
            // Service UUIDs
            if (device.haveServiceUUID()) {
                JsonArray uuidsArray = deviceObj.createNestedArray("service_uuids");
                for (int j = 0; j < device.getServiceUUIDCount(); j++) {
                    uuidsArray.add(device.getServiceUUID(j).toString().c_str());
                }
            }
        }
        
        data["scan_duration_ms"] = millis();
        
        String output;
        serializeJson(doc, output);
        return output;
    }
};

// Usage in main code
BLEScanner bleScanner;

void setup() {
    Serial.begin(115200);
    // BLEScanner automatically initializes in constructor
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        
        StaticJsonDocument<512> cmdDoc;
        DeserializationError error = deserializeJson(cmdDoc, command);
        
        if (!error && cmdDoc["cmd"] == "scan" && cmdDoc["params"]["type"] == "ble") {
            int duration = cmdDoc["params"]["duration_ms"] | 10000;  // Default 10 seconds
            String result = bleScanner.scanBLE(duration / 1000);
            Serial.println(result);
        }
    }
}
```

### 11.3 Backend: OUI Database Sync Endpoint

```typescript
import { Request, Response } from 'express';
import { Pool } from 'pg';

interface OUIEntry {
    oui: string;
    manufacturer: string;
    device_type: string | null;
    threat_category: string | null;
    confidence: number;
}

class OUIController {
    private pool: Pool;
    
    constructor(pool: Pool) {
        this.pool = pool;
    }
    
    /**
     * GET /api/v1/oui/updates
     * 
     * Returns OUI database updates since a given version.
     * Supports delta updates (only changed entries) or full sync.
     */
    async getUpdates(req: Request, res: Response) {
        try {
            const sinceVersion = parseInt(req.query.since_version as string) || 0;
            const full = req.query.full === 'true';
            
            if (full) {
                // Return full database
                const result = await this.pool.query(
                    'SELECT oui, manufacturer, device_type, threat_category, confidence FROM oui_master ORDER BY oui'
                );
                
                const currentVersion = await this.getCurrentVersion();
                
                return res.json({
                    version: currentVersion,
                    delta_from: null,
                    entries: result.rows,
                    next_update_at: this.getNextUpdateTime()
                });
            } else {
                // Return delta since version
                const result = await this.pool.query(
                    `SELECT oui, manufacturer, device_type, threat_category, confidence 
                     FROM oui_master 
                     WHERE last_updated > (SELECT created_at FROM oui_versions WHERE version = $1)
                     ORDER BY oui`,
                    [sinceVersion]
                );
                
                const currentVersion = await this.getCurrentVersion();
                
                return res.json({
                    version: currentVersion,
                    delta_from: sinceVersion,
                    entries: result.rows,
                    next_update_at: this.getNextUpdateTime()
                });
            }
        } catch (error) {
            console.error('OUI sync error:', error);
            return res.status(500).json({
                error: 'Internal server error',
                message: 'Failed to retrieve OUI updates'
            });
        }
    }
    
    /**
     * POST /api/v1/oui/update
     * 
     * Admin endpoint to update OUI database from IEEE registry.
     * Authenticated with admin API key.
     */
    async updateFromIEEE(req: Request, res: Response) {
        try {
            // Verify admin API key
            const apiKey = req.headers['x-api-key'];
            if (apiKey !== process.env.ADMIN_API_KEY) {
                return res.status(401).json({ error: 'Unauthorized' });
            }
            
            // Fetch IEEE OUI registry (example URL)
            const ieeeData = await this.fetchIEEERegistry();
            
            // Begin transaction
            const client = await this.pool.connect();
            try {
                await client.query('BEGIN');
                
                let insertedCount = 0;
                let updatedCount = 0;
                
                for (const entry of ieeeData) {
                    const result = await client.query(
                        `INSERT INTO oui_master (oui, manufacturer, device_type, threat_category, confidence, source, last_updated)
                         VALUES ($1, $2, $3, $4, $5, 'ieee', NOW())
                         ON CONFLICT (oui) DO UPDATE
                         SET manufacturer = EXCLUDED.manufacturer,
                             last_updated = NOW()
                         RETURNING (xmax = 0) AS inserted`,
                        [entry.oui, entry.manufacturer, null, null, 0.5]
                    );
                    
                    if (result.rows[0].inserted) {
                        insertedCount++;
                    } else {
                        updatedCount++;
                    }
                }
                
                // Increment version
                await client.query(
                    `INSERT INTO oui_versions (version, created_at, entry_count)
                     VALUES ((SELECT COALESCE(MAX(version), 0) + 1 FROM oui_versions), NOW(), $1)`,
                    [ieeeData.length]
                );
                
                await client.query('COMMIT');
                
                return res.json({
                    success: true,
                    inserted: insertedCount,
                    updated: updatedCount,
                    version: await this.getCurrentVersion()
                });
                
            } catch (error) {
                await client.query('ROLLBACK');
                throw error;
            } finally {
                client.release();
            }
        } catch (error) {
            console.error('IEEE sync error:', error);
            return res.status(500).json({
                error: 'Failed to sync from IEEE registry'
            });
        }
    }
    
    private async getCurrentVersion(): Promise<number> {
        const result = await this.pool.query(
            'SELECT MAX(version) as version FROM oui_versions'
        );
        return result.rows[0].version || 0;
    }
    
    private getNextUpdateTime(): number {
        // Weekly updates, next Sunday at 3 AM UTC
        const now = new Date();
        const nextSunday = new Date(now);
        nextSunday.setDate(now.getDate() + (7 - now.getDay()));
        nextSunday.setHours(3, 0, 0, 0);
        return Math.floor(nextSunday.getTime() / 1000);
    }
    
    private async fetchIEEERegistry(): Promise<{oui: string, manufacturer: string}[]> {
        // Placeholder - actual implementation would fetch from:
        // https://standards-oui.ieee.org/oui/oui.txt
        // Parse the file and return array of {oui, manufacturer}
        return [];
    }
}

export default OUIController;
```

---

## 12. Appendices

### Appendix A: Glossary

See PRD Appendix A

### Appendix B: Database Schema Diagrams

```
[Mobile SQLite Database]

┌──────────────┐         ┌────────────────────┐
│    scans     │1      N │ detected_devices   │
│──────────────│◄────────│────────────────────│
│ id (PK)      │         │ id (PK)            │
│ timestamp    │         │ scan_id (FK)       │
│ location_lat │         │ device_type        │
│ location_lon │         │ mac_address        │
│ ...          │         │ threat_level       │
└──────────────┘         │ ...                │
                         └────────────────────┘
                                  │1
                                  │
                                  │N
                         ┌────────────────────┐
                         │ threat_evidence    │
                         │────────────────────│
                         │ id (PK)            │
                         │ device_id (FK)     │
                         │ evidence_type      │
                         │ file_path          │
                         └────────────────────┘

┌──────────────┐
│oui_database  │
│──────────────│
│ oui (PK)     │
│ manufacturer │
│ device_type  │
│ threat_cat.. │
└──────────────┘
```

### Appendix C: Sequence Diagrams

**User Scan Flow:**
```
User → App → ESP32 → App → Cloud
 │      │       │      │      │
 │ Tap "Scan"  │      │      │
 │─────>│      │      │      │
 │      │Send cmd     │      │
 │      │────────>│   │      │
 │      │      │ Scan │      │
 │      │      │(WiFi)│      │
 │      │<─Result──┘  │      │
 │      │Query OUI DB │      │
 │      │─────────────>│      │
 │      │<──Device Info┤      │
 │      │Classify     │      │
 │<─Show results──┘   │      │
 │      │(Optional)   │      │
 │      │──Sync to cloud────>│
 │      │<─────Ack─────────┘│
```

---

**END OF TECHNICAL SPECIFICATION**
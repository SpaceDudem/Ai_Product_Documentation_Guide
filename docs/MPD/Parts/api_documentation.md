# API Documentation
# RF Shield - Privacy Protection Platform

**Version:** 1.0  
**Date:** December 14, 2024  
**Author:** Engineering Team  
**Status:** Draft

---

## Table of Contents

1. [Overview](#1-overview)
2. [Authentication](#2-authentication)
3. [REST API Endpoints](#3-rest-api-endpoints)
4. [Bluetooth LE GATT API](#4-bluetooth-le-gatt-api)
5. [WebSocket API](#5-websocket-api)
6. [Error Codes](#6-error-codes)
7. [Rate Limits](#7-rate-limits)
8. [Code Examples](#8-code-examples)

---

## 1. Overview

### 1.1 Base URLs

**Production:**
```
https://api.rfshield.io/v1
```

**Staging:**
```
https://api-staging.rfshield.io/v1
```

**Development:**
```
http://localhost:3000/v1
```

### 1.2 API Versioning

- Current version: `v1`
- Version specified in URL path: `/v1/endpoint`
- Breaking changes will increment major version: `v2`
- Backward-compatible changes do not change version

### 1.3 Data Formats

**Request:**
- Content-Type: `application/json`
- Character encoding: UTF-8

**Response:**
- Content-Type: `application/json`
- Character encoding: UTF-8

**Timestamps:**
- Format: Unix timestamp (seconds since epoch)
- Example: `1702587600`

**Dates:**
- Format: ISO 8601 (YYYY-MM-DD)
- Example: `2024-12-14`

---

## 2. Authentication

### 2.1 Firebase JWT Authentication

All authenticated endpoints require a Firebase JWT token in the Authorization header.

**Header:**
```
Authorization: Bearer <firebase_jwt_token>
```

**Obtaining a Token:**

```javascript
// Client-side (Firebase SDK)
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';

const auth = getAuth();
const userCredential = await signInWithEmailAndPassword(auth, email, password);
const token = await userCredential.user.getIdToken();

// Use token in API requests
fetch('https://api.rfshield.io/v1/scans/sync', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
});
```

**Token Expiration:**
- Tokens expire after 1 hour
- Refresh tokens automatically via Firebase SDK
- Expired tokens return `401 Unauthorized`

### 2.2 API Key Authentication (Admin Endpoints)

Admin endpoints require an API key in the `X-API-Key` header.

**Header:**
```
X-API-Key: <admin_api_key>
```

**Example:**
```bash
curl -X POST https://api.rfshield.io/v1/admin/oui/update \
  -H "X-API-Key: sk_live_abc123..." \
  -H "Content-Type: application/json"
```

---

## 3. REST API Endpoints

### 3.1 Scan Management

#### POST `/scans/sync`

Sync scan history to cloud (premium users only).

**Authentication:** Required (Firebase JWT)

**Request Body:**
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
      "scan_type": "quick",
      "duration": 58,
      "threats_found": 2,
      "threats": [
        {
          "device_type": "wifi",
          "mac": "AA:BB:CC:DD:EE:FF",
          "name": "Wyze_Cam_v3",
          "manufacturer": "Wyze Labs",
          "model": "v3",
          "rssi": -45,
          "channel": 6,
          "threat_level": "threat",
          "threat_reason": "WiFi camera detected"
        }
      ],
      "encrypted_data": "base64-encoded-encrypted-blob"
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "synced_count": 1,
  "failed": [],
  "sync_timestamp": 1702587620
}
```

**Response (207 Multi-Status - Partial Success):**
```json
{
  "success": false,
  "synced_count": 0,
  "failed": [
    {
      "scan_id": "uuid-v4",
      "error": "Invalid data format",
      "code": "VALIDATION_ERROR"
    }
  ],
  "sync_timestamp": 1702587620
}
```

**Errors:**
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User is not premium
- `413 Payload Too Large`: Request body exceeds 10 MB
- `429 Too Many Requests`: Rate limit exceeded

**Rate Limit:** 100 requests per hour per user

---

#### GET `/scans/history`

Retrieve user's scan history from cloud.

**Authentication:** Required (Firebase JWT)

**Query Parameters:**
- `limit` (integer, optional): Max results to return (1-100, default: 20)
- `offset` (integer, optional): Pagination offset (default: 0)
- `start_date` (integer, optional): Unix timestamp - filter scans after this date
- `end_date` (integer, optional): Unix timestamp - filter scans before this date
- `threat_level` (string, optional): Filter by threat level (`safe`, `investigate`, `threat`)

**Example Request:**
```
GET /scans/history?limit=50&threat_level=threat&start_date=1702400000
```

**Response (200 OK):**
```json
{
  "scans": [
    {
      "scan_id": "uuid-v4",
      "timestamp": 1702587600,
      "location_name": "Hotel Room 302",
      "scan_type": "quick",
      "threats_found": 2,
      "threats": [
        {
          "device_type": "wifi",
          "name": "Wyze_Cam_v3",
          "threat_level": "threat"
        }
      ]
    }
  ],
  "total_count": 143,
  "offset": 0,
  "limit": 50
}
```

**Errors:**
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User is not premium

**Rate Limit:** 1000 requests per hour per user

---

#### DELETE `/scans/:scan_id`

Delete a specific scan from cloud history.

**Authentication:** Required (Firebase JWT)

**Path Parameters:**
- `scan_id` (string): UUID of scan to delete

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Scan deleted successfully"
}
```

**Errors:**
- `401 Unauthorized`: Invalid or expired token
- `404 Not Found`: Scan not found or doesn't belong to user

---

### 3.2 OUI Database

#### GET `/oui/updates`

Get OUI database updates.

**Authentication:** Optional (unauthenticated gets public data only)

**Query Parameters:**
- `since_version` (integer, optional): Last known version, returns delta
- `full` (boolean, optional): If true, returns full database (default: false)

**Example Request:**
```
GET /oui/updates?since_version=1233
```

**Response (200 OK):**
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
    },
    {
      "oui": "11:22:33",
      "manufacturer": "Tile Inc",
      "device_type": "tracker",
      "threat_category": "tracking",
      "confidence": 0.99
    }
  ],
  "next_update_at": 1702674000,
  "download_size_bytes": 45678
}
```

**Response Headers:**
```
ETag: "1234"
Cache-Control: public, max-age=86400
```

**Errors:**
- `400 Bad Request`: Invalid version number

**Rate Limit:** 10 requests per hour per IP (unauthenticated), 100 per hour (authenticated)

---

#### GET `/oui/lookup/:mac`

Lookup device info by MAC address.

**Authentication:** Optional

**Path Parameters:**
- `mac` (string): MAC address (formats accepted: `AA:BB:CC:DD:EE:FF`, `AA-BB-CC-DD-EE-FF`, `AABBCCDDEEFF`)

**Example Request:**
```
GET /oui/lookup/AA:BB:CC:DD:EE:FF
```

**Response (200 OK):**
```json
{
  "oui": "AA:BB:CC",
  "mac": "AA:BB:CC:DD:EE:FF",
  "manufacturer": "Wyze Labs",
  "device_type": "camera",
  "threat_category": "surveillance",
  "confidence": 0.95,
  "last_updated": 1702587600
}
```

**Response (404 Not Found):**
```json
{
  "error": "OUI not found",
  "oui": "AA:BB:CC",
  "message": "No manufacturer data available for this OUI"
}
```

**Rate Limit:** 1000 requests per hour per IP

---

### 3.3 Threat Intelligence

#### POST `/threats/report`

Submit crowdsourced threat intelligence.

**Authentication:** Required (Firebase JWT)

**Request Body:**
```json
{
  "device": {
    "mac_prefix": "AA:BB:CC",
    "name": "Unknown Device",
    "type": "camera",
    "manufacturer": "Unknown"
  },
  "location": {
    "country": "US",
    "city": "Houston"
  },
  "evidence": {
    "confidence": 0.8,
    "detection_method": "lens_finder",
    "notes": "Found hidden in smoke detector",
    "photo_hash": "sha256:abc123..."
  }
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "report_id": "uuid-v4",
  "status": "pending",
  "message": "Report submitted for community verification",
  "estimated_verification_time": "24-48 hours"
}
```

**Errors:**
- `401 Unauthorized`: Invalid or expired token
- `400 Bad Request`: Invalid data format
- `429 Too Many Requests`: Max 10 reports per day per user

**Rate Limit:** 10 requests per day per user

---

#### GET `/threats/reports/:report_id`

Get status of a threat report.

**Authentication:** Required (Firebase JWT, must be report author)

**Path Parameters:**
- `report_id` (string): UUID of report

**Response (200 OK):**
```json
{
  "report_id": "uuid-v4",
  "status": "verified",
  "votes": {
    "confirmed": 15,
    "rejected": 2
  },
  "created_at": 1702587600,
  "verified_at": 1702674000,
  "device": {
    "oui": "AA:BB:CC",
    "manufacturer": "Wyze Labs",
    "device_type": "camera",
    "threat_category": "surveillance"
  }
}
```

**Status Values:**
- `pending`: Under community review
- `verified`: Confirmed by community (will be added to OUI database)
- `rejected`: Rejected by community (false positive)
- `disputed`: Mixed votes, needs admin review

---

### 3.4 Firmware Updates

#### GET `/firmware/latest`

Check for firmware updates.

**Authentication:** Optional (unauthenticated gets stable releases only)

**Query Parameters:**
- `module_type` (string, required): `esp32`, `ultrasonic`, `ir_flood`
- `current_version` (string, required): Semantic version (e.g., `1.2.3`)
- `beta` (boolean, optional): Include beta releases (default: false, requires authentication)

**Example Request:**
```
GET /firmware/latest?module_type=esp32&current_version=1.2.3
```

**Response (200 OK - Update Available):**
```json
{
  "update_available": true,
  "latest_version": "1.3.0",
  "release_notes": "Added 5 GHz WiFi support, improved BLE range",
  "download_url": "https://cdn.rfshield.io/firmware/esp32-1.3.0.bin",
  "sha256": "abc123def456...",
  "size_bytes": 1048576,
  "mandatory": false,
  "released_at": 1702587600
}
```

**Response (200 OK - No Update):**
```json
{
  "update_available": false,
  "latest_version": "1.2.3",
  "message": "You are running the latest version"
}
```

**Errors:**
- `400 Bad Request`: Invalid module type or version format

**Rate Limit:** 100 requests per hour per device

---

#### GET `/firmware/download/:module_type/:version`

Download firmware binary.

**Authentication:** Not required (public CDN link)

**Path Parameters:**
- `module_type` (string): `esp32`, `ultrasonic`, `ir_flood`
- `version` (string): Semantic version (e.g., `1.3.0`)

**Response (200 OK):**
- Content-Type: `application/octet-stream`
- Content-Length: File size in bytes
- Content-Disposition: `attachment; filename="esp32-1.3.0.bin"`
- Binary firmware file

**Response Headers:**
```
X-Firmware-Version: 1.3.0
X-SHA256: abc123def456...
Cache-Control: public, max-age=31536000, immutable
```

**Errors:**
- `404 Not Found`: Firmware version not found

---

### 3.5 TSCM Professional Referrals

#### POST `/tscm/referral`

Submit TSCM professional sweep request.

**Authentication:** Required (Firebase JWT)

**Request Body:**
```json
{
  "location": {
    "address": "123 Main St, Houston, TX 77002",
    "type": "hotel",
    "additional_info": "Room 302"
  },
  "urgency": "high",
  "scan_report_id": "uuid-v4",
  "contact": {
    "email": "user@example.com",
    "phone": "+1-555-0100",
    "preferred_contact_method": "email"
  },
  "notes": "Found hidden camera in smoke detector, need professional verification"
}
```

**Location Types:**
- `hotel`: Hotel room
- `home`: Residence
- `office`: Office/workspace
- `vehicle`: Car/vehicle
- `other`: Other location

**Urgency Levels:**
- `low`: Non-urgent, can wait 1-2 weeks
- `medium`: Important, prefer within a week
- `high`: Urgent, need within 24-48 hours

**Response (201 Created):**
```json
{
  "success": true,
  "referral_id": "uuid-v4",
  "matched_firms": [
    {
      "firm_id": "uuid-firm-1",
      "name": "Houston TSCM Services",
      "distance_km": 3.2,
      "rating": 4.8,
      "price_range": "$2000-$5000",
      "availability": "Next available: 2024-12-20",
      "contact": {
        "phone": "+1-713-555-0200",
        "email": "contact@houstontscm.com",
        "website": "https://houstontscm.com"
      }
    },
    {
      "firm_id": "uuid-firm-2",
      "name": "Texas Security Sweeps",
      "distance_km": 5.8,
      "rating": 4.6,
      "price_range": "$1800-$4500",
      "availability": "Next available: 2024-12-22"
    }
  ],
  "message": "Request sent to 3 nearby TSCM firms. They will contact you within 24 hours.",
  "estimated_response_time": "24 hours"
}
```

**Errors:**
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: Feature not available in user's tier
- `400 Bad Request`: Invalid location or contact info

**Rate Limit:** 5 requests per week per user

---

#### GET `/tscm/referral/:referral_id`

Get status of TSCM referral request.

**Authentication:** Required (Firebase JWT, must be request author)

**Path Parameters:**
- `referral_id` (string): UUID of referral

**Response (200 OK):**
```json
{
  "referral_id": "uuid-v4",
  "status": "firms_responded",
  "created_at": 1702587600,
  "responses": [
    {
      "firm_id": "uuid-firm-1",
      "firm_name": "Houston TSCM Services",
      "responded_at": 1702591200,
      "message": "We can schedule a sweep for December 20th at 2 PM. Our rate is $2,500 for a standard hotel room sweep.",
      "quote": {
        "amount": 2500,
        "currency": "USD",
        "valid_until": 1703192400
      }
    }
  ]
}
```

**Status Values:**
- `pending`: Sent to firms, awaiting responses
- `firms_responded`: At least one firm responded
- `booked`: User scheduled with a firm
- `completed`: Sweep completed
- `cancelled`: User cancelled request

---

### 3.6 User Management

#### GET `/user/profile`

Get user profile and subscription info.

**Authentication:** Required (Firebase JWT)

**Response (200 OK):**
```json
{
  "uid": "firebase-user-id",
  "email": "user@example.com",
  "premium": {
    "active": true,
    "tier": "premium",
    "expires_at": 1734123600,
    "stripe_customer_id": "cus_abc123",
    "subscription_id": "sub_def456"
  },
  "hardware_modules": [
    {
      "module_id": "ESP32-AABBCCDDEEFF",
      "type": "esp32",
      "firmware_version": "1.2.3",
      "paired_at": 1702587600,
      "last_seen": 1702674000
    }
  ],
  "settings": {
    "sync_enabled": true,
    "notification_preferences": {
      "new_threats": true,
      "firmware_updates": true,
      "marketing": false
    }
  },
  "stats": {
    "total_scans": 143,
    "threats_found": 8,
    "last_scan": 1702674000
  },
  "created_at": 1670000000
}
```

---

#### PATCH `/user/settings`

Update user settings.

**Authentication:** Required (Firebase JWT)

**Request Body:**
```json
{
  "sync_enabled": true,
  "notification_preferences": {
    "new_threats": true,
    "firmware_updates": true,
    "marketing": false
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "settings": {
    "sync_enabled": true,
    "notification_preferences": {
      "new_threats": true,
      "firmware_updates": true,
      "marketing": false
    }
  }
}
```

---

#### POST `/user/pair-hardware`

Pair a hardware module to user account.

**Authentication:** Required (Firebase JWT)

**Request Body:**
```json
{
  "module_id": "ESP32-AABBCCDDEEFF",
  "type": "esp32",
  "pairing_code": "123456"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "module": {
    "module_id": "ESP32-AABBCCDDEEFF",
    "type": "esp32",
    "firmware_version": "1.2.3",
    "paired_at": 1702674000
  }
}
```

**Errors:**
- `400 Bad Request`: Invalid pairing code
- `409 Conflict`: Module already paired to another account

---

#### DELETE `/user/account`

Delete user account (GDPR compliance).

**Authentication:** Required (Firebase JWT)

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Account deletion initiated. All data will be permanently deleted within 30 days.",
  "deletion_date": 1705266000
}
```

**Note:** This is irreversible. All scan history, hardware pairings, and subscription data will be deleted.

---

### 3.7 Payment & Subscription

#### POST `/subscription/create`

Create a premium subscription.

**Authentication:** Required (Firebase JWT)

**Request Body:**
```json
{
  "tier": "premium",
  "billing_cycle": "annual",
  "payment_method_id": "pm_abc123"
}
```

**Tier Options:**
- `premium`: $79/year or $9.99/month
- `pro`: $999 one-time

**Billing Cycle:**
- `monthly`: Billed monthly
- `annual`: Billed annually (20% discount)

**Response (200 OK):**
```json
{
  "success": true,
  "subscription": {
    "subscription_id": "sub_def456",
    "status": "active",
    "tier": "premium",
    "current_period_start": 1702587600,
    "current_period_end": 1734123600,
    "amount": 7900,
    "currency": "USD"
  }
}
```

**Errors:**
- `400 Bad Request`: Invalid payment method
- `402 Payment Required`: Payment failed
- `409 Conflict`: User already has active subscription

---

#### POST `/subscription/cancel`

Cancel subscription (end of billing period).

**Authentication:** Required (Firebase JWT)

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Subscription will be cancelled at end of billing period",
  "cancellation_date": 1734123600
}
```

---

#### GET `/subscription/status`

Get current subscription status.

**Authentication:** Required (Firebase JWT)

**Response (200 OK):**
```json
{
  "active": true,
  "tier": "premium",
  "status": "active",
  "current_period_end": 1734123600,
  "cancel_at_period_end": false,
  "renewal_date": 1734123600
}
```

**Status Values:**
- `active`: Subscription is active
- `past_due`: Payment failed, grace period
- `cancelled`: Subscription cancelled
- `expired`: Subscription expired

---

## 4. Bluetooth LE GATT API

### 4.1 Service Overview

**Service UUID:** `0000fff0-0000-1000-8000-00805f9b34fb`

**Characteristics:**
1. **Command (Write):** `0000fff1-0000-1000-8000-00805f9b34fb`
2. **Response (Notify):** `0000fff2-0000-1000-8000-00805f9b34fb`
3. **Status (Read/Notify):** `0000fff3-0000-1000-8000-00805f9b34fb`

### 4.2 Connection Flow

```
1. Mobile app scans for BLE devices
2. Finds device with name "RF-Shield-ESP32-XXXXXX"
3. Connects to device
4. Discovers services (0000fff0-...)
5. Subscribes to Response characteristic (Notify)
6. Subscribes to Status characteristic (Notify)
7. Writes commands to Command characteristic
8. Receives responses via notifications
```

### 4.3 Command Characteristic (Write)

**UUID:** `0000fff1-0000-1000-8000-00805f9b34fb`

**Format:** JSON string (UTF-8 encoded)

**Max Length:** 512 bytes per write

#### Command: WiFi Scan

```json
{
  "cmd": "scan",
  "params": {
    "type": "wifi",
    "channels": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    "duration_ms": 5000
  }
}
```

**Parameters:**
- `channels` (array, optional): WiFi channels to scan (default: all)
- `duration_ms` (integer, optional): Scan duration in milliseconds (default: 5000)

#### Command: BLE Scan

```json
{
  "cmd": "scan",
  "params": {
    "type": "ble",
    "duration_ms": 10000,
    "filter_airtags": true,
    "active_scan": true
  }
}
```

**Parameters:**
- `duration_ms` (integer, optional): Scan duration (default: 10000)
- `filter_airtags` (boolean, optional): Only return AirTags (default: false)
- `active_scan` (boolean, optional): Active scan (more data, more power) (default: true)

#### Command: Sub-GHz Scan

```json
{
  "cmd": "scan",
  "params": {
    "type": "subghz",
    "frequencies": [315000000, 433920000, 868000000, 915000000],
    "bandwidth": 200000,
    "duration_ms": 30000
  }
}
```

**Parameters:**
- `frequencies` (array): Frequencies to scan in Hz
- `bandwidth` (integer): Receiver bandwidth in Hz (default: 200000)
- `duration_ms` (integer): Scan duration (default: 30000)

#### Command: Stop Scan

```json
{
  "cmd": "stop"
}
```

#### Command: Get Status

```json
{
  "cmd": "status"
}
```

#### Command: Configure Module

```json
{
  "cmd": "configure",
  "params": {
    "gps_enabled": true,
    "sd_logging": true,
    "led_brightness": 50
  }
}
```

### 4.4 Response Characteristic (Notify)

**UUID:** `0000fff2-0000-1000-8000-00805f9b34fb`

**Format:** JSON string (UTF-8 encoded)

**Max Length:** 512 bytes per notification (chunked if larger)

#### Response: WiFi Scan Results

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
      }
    ],
    "scan_duration_ms": 4823
  },
  "timestamp": 1702587605
}
```

#### Response: BLE Scan Results

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

#### Response: Sub-GHz Scan Results

```json
{
  "status": "success",
  "data": {
    "type": "subghz",
    "signals": [
      {
        "frequency": 433920000,
        "rssi": -65,
        "bandwidth": 200000,
        "modulation": "ASK",
        "duration_ms": 1500,
        "data": "base64-encoded-capture"
      }
    ],
    "scan_duration_ms": 30120
  },
  "timestamp": 1702587645
}
```

#### Response: Error

```json
{
  "status": "error",
  "error": {
    "code": "SCAN_FAILED",
    "message": "WiFi initialization failed",
    "details": "ESP32 WiFi module not responding"
  },
  "timestamp": 1702587650
}
```

**Error Codes:**
- `SCAN_FAILED`: Scan could not be initiated
- `TIMEOUT`: Scan timed out
- `INVALID_PARAMS`: Invalid command parameters
- `HARDWARE_ERROR`: Hardware module error
- `LOW_BATTERY`: Battery too low to perform scan

### 4.5 Status Characteristic (Read/Notify)

**UUID:** `0000fff3-0000-1000-8000-00805f9b34fb`

**Format:** JSON string (UTF-8 encoded)

```json
{
  "firmware_version": "1.2.3",
  "battery_level": 85,
  "temperature": 42,
  "uptime_seconds": 3600,
  "wifi_connected": true,
  "gps_locked": true,
  "gps_coords": {
    "lat": 29.7604,
    "lon": -95.3698,
    "altitude": 10.5
  },
  "sd_card_free_mb": 28672,
  "errors": []
}
```

**Status Updates:**
- Automatically sent every 30 seconds when connected
- Can be requested via "status" command

---

## 5. WebSocket API

### 5.1 Connection

**URL:** `wss://api.rfshield.io/v1/ws`

**Authentication:** JWT token in query parameter or header

```javascript
const ws = new WebSocket('wss://api.rfshield.io/v1/ws?token=<firebase_jwt>');

// Or via header (if supported by client)
const ws = new WebSocket('wss://api.rfshield.io/v1/ws', {
  headers: {
    'Authorization': 'Bearer <firebase_jwt>'
  }
});
```

### 5.2 Message Format

**Client → Server:**
```json
{
  "type": "subscribe",
  "channel": "scans",
  "filters": {
    "threat_level": "threat"
  }
}
```

**Server → Client:**
```json
{
  "type": "scan_update",
  "data": {
    "scan_id": "uuid-v4",
    "threats_found": 1,
    "threat": {
      "device_type": "wifi",
      "name": "New Camera Detected"
    }
  },
  "timestamp": 1702587700
}
```

### 5.3 Channels

#### Channel: `scans`

Real-time scan updates from all user's devices.

**Subscribe:**
```json
{
  "type": "subscribe",
  "channel": "scans"
}
```

**Events:**
- `scan_started`: Scan initiated
- `scan_progress`: Scan in progress (% complete)
- `scan_completed`: Scan finished
- `threat_detected`: New threat found

#### Channel: `firmware`

Firmware update notifications.

**Subscribe:**
```json
{
  "type": "subscribe",
  "channel": "firmware",
  "filters": {
    "module_type": "esp32"
  }
}
```

**Events:**
- `update_available`: New firmware version released

#### Channel: `tscm`

TSCM referral status updates.

**Subscribe:**
```json
{
  "type": "subscribe",
  "channel": "tscm",
  "filters": {
    "referral_id": "uuid-v4"
  }
}
```

**Events:**
- `firm_responded`: TSCM firm responded to request
- `quote_received`: Price quote received

---

## 6. Error Codes

### 6.1 HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request succeeded, no body returned |
| 400 | Bad Request | Invalid request format or parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Request conflicts with current state |
| 413 | Payload Too Large | Request body exceeds size limit |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

### 6.2 Application Error Codes

**Format:**
```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": "Additional context (optional)"
}
```

**Common Codes:**

| Code | HTTP | Description |
|------|------|-------------|
| `INVALID_TOKEN` | 401 | JWT token invalid or expired |
| `PREMIUM_REQUIRED` | 403 | Feature requires premium subscription |
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `SCAN_NOT_FOUND` | 404 | Scan ID not found |
| `OUI_NOT_FOUND` | 404 | OUI not in database |
| `FIRMWARE_NOT_FOUND` | 404 | Firmware version not available |
| `PAYMENT_FAILED` | 402 | Payment processing failed |
| `DUPLICATE_REPORT` | 409 | Threat already reported |
| `MODULE_ALREADY_PAIRED` | 409 | Hardware module already paired |

---

## 7. Rate Limits

### 7.1 Global Rate Limits

**Per IP Address (Unauthenticated):**
- 100 requests per hour
- Burst: 10 requests per minute

**Per User (Authenticated):**
- Free tier: 100 requests per hour
- Premium tier: 1,000 requests per hour
- Pro tier: 10,000 requests per hour

### 7.2 Endpoint-Specific Limits

| Endpoint | Free | Premium | Pro |
|----------|------|---------|-----|
| `/scans/sync` | N/A | 100/hour | 1000/hour |
| `/oui/updates` | 10/hour | 100/hour | 1000/hour |
| `/threats/report` | 10/day | 50/day | Unlimited |
| `/firmware/latest` | 100/hour | 1000/hour | Unlimited |
| `/tscm/referral` | N/A | 5/week | 50/week |

### 7.3 Rate Limit Headers

**Response Headers:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1702591200
Retry-After: 3600
```

**When Rate Limited (429):**
```json
{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded",
  "retry_after": 3600,
  "limit": 1000,
  "reset_at": 1702591200
}
```

---

## 8. Code Examples

### 8.1 JavaScript/TypeScript (Node.js)

#### Sync Scans to Cloud

```typescript
import axios from 'axios';
import { getAuth } from 'firebase/auth';

async function syncScans(scans: Scan[]): Promise<void> {
  const auth = getAuth();
  const user = auth.currentUser;
  
  if (!user) {
    throw new Error('User not authenticated');
  }
  
  const token = await user.getIdToken();
  
  try {
    const response = await axios.post(
      'https://api.rfshield.io/v1/scans/sync',
      { scans },
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    console.log(`Synced ${response.data.synced_count} scans`);
    
    if (response.data.failed.length > 0) {
      console.error('Failed scans:', response.data.failed);
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Sync failed:', error.response?.data);
    }
    throw error;
  }
}

interface Scan {
  scan_id: string;
  timestamp: number;
  location?: {
    lat: number;
    lon: number;
  };
  location_name?: string;
  threats: Threat[];
}

interface Threat {
  device_type: string;
  mac: string;
  name: string;
  threat_level: string;
  rssi: number;
}
```

#### Check for Firmware Updates

```typescript
async function checkFirmwareUpdate(
  moduleType: string,
  currentVersion: string
): Promise<FirmwareUpdate | null> {
  try {
    const response = await axios.get(
      'https://api.rfshield.io/v1/firmware/latest',
      {
        params: {
          module_type: moduleType,
          current_version: currentVersion
        }
      }
    );
    
    if (response.data.update_available) {
      return {
        version: response.data.latest_version,
        downloadUrl: response.data.download_url,
        sha256: response.data.sha256,
        sizeBytes: response.data.size_bytes,
        releaseNotes: response.data.release_notes,
        mandatory: response.data.mandatory
      };
    }
    
    return null;
  } catch (error) {
    console.error('Failed to check for updates:', error);
    return null;
  }
}

interface FirmwareUpdate {
  version: string;
  downloadUrl: string;
  sha256: string;
  sizeBytes: number;
  releaseNotes: string;
  mandatory: boolean;
}
```

### 8.2 Kotlin (Android)

#### BLE Communication

```kotlin
import android.bluetooth.*
import java.util.UUID

class ESP32Module(private val device: BluetoothDevice) {
    
    companion object {
        val SERVICE_UUID: UUID = UUID.fromString("0000fff0-0000-1000-8000-00805f9b34fb")
        val COMMAND_UUID: UUID = UUID.fromString("0000fff1-0000-1000-8000-00805f9b34fb")
        val RESPONSE_UUID: UUID = UUID.fromString("0000fff2-0000-1000-8000-00805f9b34fb")
        val STATUS_UUID: UUID = UUID.fromString("0000fff3-0000-1000-8000-00805f9b34fb")
    }
    
    private var gatt: BluetoothGatt? = null
    private var commandCharacteristic: BluetoothGattCharacteristic? = null
    private var responseCharacteristic: BluetoothGattCharacteristic? = null
    
    suspend fun connect(): Boolean = suspendCancellableCoroutine { continuation ->
        val callback = object : BluetoothGattCallback() {
            override fun onConnectionStateChange(
                gatt: BluetoothGatt,
                status: Int,
                newState: Int
            ) {
                if (newState == BluetoothProfile.STATE_CONNECTED) {
                    gatt.discoverServices()
                } else {
                    continuation.resumeWith(Result.success(false))
                }
            }
            
            override fun onServicesDiscovered(gatt: BluetoothGatt, status: Int) {
                if (status == BluetoothGatt.GATT_SUCCESS) {
                    val service = gatt.getService(SERVICE_UUID)
                    commandCharacteristic = service.getCharacteristic(COMMAND_UUID)
                    responseCharacteristic = service.getCharacteristic(RESPONSE_UUID)
                    
                    // Enable notifications
                    gatt.setCharacteristicNotification(responseCharacteristic, true)
                    val descriptor = responseCharacteristic?.getDescriptor(
                        UUID.fromString("00002902-0000-1000-8000-00805f9b34fb")
                    )
                    descriptor?.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
                    gatt.writeDescriptor(descriptor)
                    
                    continuation.resumeWith(Result.success(true))
                } else {
                    continuation.resumeWith(Result.success(false))
                }
            }
            
            override fun onCharacteristicChanged(
                gatt: BluetoothGatt,
                characteristic: BluetoothGattCharacteristic
            ) {
                if (characteristic.uuid == RESPONSE_UUID) {
                    val response = characteristic.getStringValue(0)
                    handleResponse(response)
                }
            }
        }
        
        gatt = device.connectGatt(context, false, callback)
    }
    
    fun sendCommand(command: String) {
        commandCharacteristic?.let {
            it.setValue(command)
            gatt?.writeCharacteristic(it)
        }
    }
    
    fun scanWiFi(channels: List<Int> = (1..14).toList(), durationMs: Int = 5000) {
        val command = JSONObject().apply {
            put("cmd", "scan")
            put("params", JSONObject().apply {
                put("type", "wifi")
                put("channels", JSONArray(channels))
                put("duration_ms", durationMs)
            })
        }.toString()
        
        sendCommand(command)
    }
    
    private fun handleResponse(json: String) {
        val response = JSONObject(json)
        val status = response.getString("status")
        
        if (status == "success") {
            val data = response.getJSONObject("data")
            val type = data.getString("type")
            
            when (type) {
                "wifi" -> handleWiFiResults(data)
                "ble" -> handleBLEResults(data)
                "subghz" -> handleSubGHzResults(data)
            }
        } else {
            val error = response.getJSONObject("error")
            Log.e("ESP32", "Scan error: ${error.getString("message")}")
        }
    }
    
    fun disconnect() {
        gatt?.disconnect()
        gatt?.close()
        gatt = null
    }
}
```

### 8.3 Swift (iOS)

#### API Client

```swift
import Foundation

class RFShieldAPI {
    static let shared = RFShieldAPI()
    private let baseURL = "https://api.rfshield.io/v1"
    
    private init() {}
    
    func syncScans(scans: [Scan]) async throws {
        guard let token = try await getAuthToken() else {
            throw APIError.notAuthenticated
        }
        
        let url = URL(string: "\(baseURL)/scans/sync")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["scans": scans.map { $0.toDictionary() }]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            throw APIError.httpError(statusCode: httpResponse.statusCode)
        }
        
        let result = try JSONDecoder().decode(SyncResponse.self, from: data)
        print("Synced \(result.synced_count) scans")
    }
    
    private func getAuthToken() async throws -> String? {
        // Firebase Auth token retrieval
        return try await Auth.auth().currentUser?.getIDToken()
    }
}

struct SyncResponse: Codable {
    let success: Bool
    let synced_count: Int
    let failed: [FailedScan]
}

struct FailedScan: Codable {
    let scan_id: String
    let error: String
    let code: String
}

enum APIError: Error {
    case notAuthenticated
    case invalidResponse
    case httpError(statusCode: Int)
}
```

### 8.4 Python

#### OUI Database Sync

```python
import requests
import sqlite3
from typing import List, Dict

class OUIDatabase:
    def __init__(self, db_path: str, api_url: str = "https://api.rfshield.io/v1"):
        self.db_path = db_path
        self.api_url = api_url
        self.conn = sqlite3.connect(db_path)
        self.create_table()
    
    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS oui_database (
                oui TEXT PRIMARY KEY,
                manufacturer TEXT NOT NULL,
                device_type TEXT,
                threat_category TEXT,
                confidence REAL,
                last_updated INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
    
    def get_current_version(self) -> int:
        cursor = self.conn.execute(
            'SELECT MAX(last_updated) FROM oui_database'
        )
        result = cursor.fetchone()[0]
        return result if result else 0
    
    def sync_updates(self) -> Dict:
        current_version = self.get_current_version()
        
        response = requests.get(
            f'{self.api_url}/oui/updates',
            params={'since_version': current_version}
        )
        response.raise_for_status()
        
        data = response.json()
        entries = data['entries']
        
        # Batch insert
        self.conn.executemany('''
            INSERT OR REPLACE INTO oui_database
            (oui, manufacturer, device_type, threat_category, confidence, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', [
            (
                entry['oui'],
                entry['manufacturer'],
                entry.get('device_type'),
                entry.get('threat_category'),
                entry.get('confidence', 0.5),
                data['version']
            )
            for entry in entries
        ])
        self.conn.commit()
        
        return {
            'updated_count': len(entries),
            'new_version': data['version']
        }
    
    def lookup(self, mac: str) -> Dict:
        oui = mac[:8].upper()
        cursor = self.conn.execute(
            'SELECT * FROM oui_database WHERE oui = ?',
            (oui,)
        )
        result = cursor.fetchone()
        
        if result:
            return {
                'oui': result[0],
                'manufacturer': result[1],
                'device_type': result[2],
                'threat_category': result[3],
                'confidence': result[4]
            }
        return None

# Usage
db = OUIDatabase('oui.db')
result = db.sync_updates()
print(f"Updated {result['updated_count']} entries to version {result['new_version']}")

device_info = db.lookup('AA:BB:CC:DD:EE:FF')
if device_info:
    print(f"Manufacturer: {device_info['manufacturer']}")
    print(f"Device Type: {device_info['device_type']}")
```

---

## 9. Appendices

### Appendix A: Postman Collection

A Postman collection with all API endpoints is available at:
```
https://api.rfshield.io/postman/collection.json
```

Import into Postman and set environment variables:
- `base_url`: https://api.rfshield.io/v1
- `firebase_token`: Your Firebase JWT token

### Appendix B: OpenAPI Specification

Full OpenAPI 3.0 specification available at:
```
https://api.rfshield.io/openapi.yaml
```

Use with tools like Swagger UI, Redoc, or API clients that support OpenAPI.

### Appendix C: SDK Availability

**Official SDKs:**
- JavaScript/TypeScript: `npm install @rfshield/sdk`
- Python: `pip install rfshield`
- Java/Kotlin: `implementation 'io.rfshield:sdk:1.0.0'`
- Swift: Swift Package Manager - `https://github.com/rfshield/swift-sdk`

**Community SDKs:**
- Ruby: `gem install rfshield`
- Go: `go get github.com/rfshield/go-sdk`
- Rust: `cargo add rfshield`

---

**END OF API DOCUMENTATION**


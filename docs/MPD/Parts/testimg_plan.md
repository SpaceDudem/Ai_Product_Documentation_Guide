# Testing Plan
# RF Shield - Privacy Protection Platform

**Version:** 1.0  
**Date:** December 14, 2024  
**Author:** QA Team  
**Status:** Draft

---

## Table of Contents

1. [Testing Strategy](#1-testing-strategy)
2. [Unit Testing](#2-unit-testing)
3. [Integration Testing](#3-integration-testing)
4. [System Testing](#4-system-testing)
5. [Performance Testing](#5-performance-testing)
6. [Security Testing](#6-security-testing)
7. [Acceptance Testing](#7-acceptance-testing)
8. [Test Environments](#8-test-environments)
9. [Test Data](#9-test-data)
10. [Defect Management](#10-defect-management)

---

## 1. Testing Strategy

### 1.1 Testing Objectives

**Primary Goals:**
1. Verify all functional requirements from PRD are met
2. Ensure detection accuracy >80% (true positives)
3. Ensure false positive rate <5%
4. Validate security and privacy controls
5. Confirm performance meets NFRs (non-functional requirements)
6. Ensure cross-platform compatibility (Android/iOS)

**Success Criteria:**
- 95%+ test case pass rate before production release
- Zero P0 (critical) bugs in production
- <5 P1 (high) bugs in production within first 30 days
- 4.5+ star rating from beta testers
- <1% crash rate in production

### 1.2 Testing Scope

**In Scope:**
- Mobile applications (Android, iOS)
- Backend APIs (REST, WebSocket)
- Hardware modules (ESP32, RTL-SDR, Camera)
- Bluetooth communication (GATT)
- Cloud services (Firebase, PostgreSQL)
- Payment processing (Stripe)
- OUI database sync
- Firmware OTA updates

**Out of Scope:**
- Third-party libraries (assume tested by vendors)
- Operating system bugs (report to Google/Apple)
- Hardware defects (covered by manufacturer warranty)
- Physical security of hardware modules

### 1.3 Testing Levels

```
┌─────────────────────────────────────────┐
│          Level 1: Unit Testing           │
│  - Individual functions & classes        │
│  - Target: 80%+ code coverage            │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│       Level 2: Integration Testing       │
│  - Module interactions                   │
│  - API contracts                         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Level 3: System Testing          │
│  - End-to-end flows                      │
│  - Cross-platform validation             │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Level 4: Acceptance Testing         │
│  - User scenarios                        │
│  - Beta user validation                  │
└─────────────────────────────────────────┘
```

### 1.4 Testing Types

| Type | Scope | When | Owner |
|------|-------|------|-------|
| **Unit** | Individual functions | Every commit | Engineers |
| **Integration** | Component interactions | Every PR merge | Engineers + QA |
| **Functional** | Feature validation | Sprint end | QA |
| **Regression** | No new bugs introduced | Every release | QA (automated) |
| **Performance** | Speed, battery, memory | Weekly | QA + DevOps |
| **Security** | Vulnerabilities | Sprint end + Pre-release | Security team |
| **Usability** | User experience | Beta phase | Product + UX |
| **Acceptance** | User stories met | Pre-release | Product + QA |

---

## 2. Unit Testing

### 2.1 Mobile App (Android)

**Framework:** JUnit 5 + Mockito

**Coverage Target:** 80%+

**Test Categories:**

#### 2.1.1 Detection Engine Tests

**File:** `DetectionEngineTest.kt`

```kotlin
class DetectionEngineTest {
    
    @Test
    fun `WiFi scan detects camera OUI correctly`() {
        // Arrange
        val mockScanner = mock<WiFiScanner>()
        val ouiDatabase = OUIDatabase(mockContext)
        val detectionEngine = DetectionEngine(mockScanner, ouiDatabase)
        
        val scanResult = ScanResult().apply {
            BSSID = "AA:BB:CC:DD:EE:FF" // Wyze Labs OUI
            SSID = "Wyze_Cam_v3"
            level = -45
        }
        
        whenever(mockScanner.scan()).thenReturn(listOf(scanResult))
        
        // Act
        val results = detectionEngine.scanWiFi()
        
        // Assert
        assertEquals(1, results.size)
        assertEquals("Wyze Labs", results[0].manufacturer)
        assertEquals(ThreatLevel.THREAT, results[0].threatLevel)
        assertEquals("camera", results[0].deviceType)
    }
    
    @Test
    fun `BLE scan identifies AirTag correctly`() {
        // Arrange
        val mockScanner = mock<BLEScanner>()
        val detectionEngine = DetectionEngine(bleScanner = mockScanner)
        
        val airtag = mockBluetoothDevice(
            mac = "AA:BB:CC:DD:EE:FF",
            manufacturerData = byteArrayOf(0x4C, 0x00, 0x12, 0x19, 0x10) // Apple AirTag signature
        )
        
        whenever(mockScanner.scan(10000)).thenReturn(listOf(airtag))
        
        // Act
        val results = detectionEngine.scanBLE()
        
        // Assert
        assertEquals(1, results.size)
        assertTrue(results[0].isAirTag)
        assertTrue(results[0].separatedFromOwner)
    }
    
    @Test
    fun `Threat assessment correctly classifies devices`() {
        val engine = DetectionEngine()
        
        // Camera = THREAT
        val camera = DeviceInfo(deviceType = "camera", manufacturer = "Wyze Labs")
        assertEquals(ThreatLevel.THREAT, engine.assessThreat(camera))
        
        // Router = SAFE
        val router = DeviceInfo(deviceType = "router", manufacturer = "Netgear")
        assertEquals(ThreatLevel.SAFE, engine.assessThreat(router))
        
        // Unknown = INVESTIGATE
        val unknown = DeviceInfo(deviceType = null, manufacturer = "Unknown")
        assertEquals(ThreatLevel.INVESTIGATE, engine.assessThreat(unknown))
    }
    
    @Test
    fun `RSSI to distance estimation is accurate`() {
        val engine = DetectionEngine()
        
        // -30 dBm = very close (< 1m)
        assertTrue(engine.estimateDistance(-30) < 1.0)
        
        // -60 dBm = medium distance (~5m)
        val dist60 = engine.estimateDistance(-60)
        assertTrue(dist60 in 3.0..7.0)
        
        // -90 dBm = far (~30m)
        assertTrue(engine.estimateDistance(-90) > 20.0)
    }
}
```

#### 2.1.2 OUI Database Tests

**File:** `OUIDatabaseTest.kt`

```kotlin
class OUIDatabaseTest {
    
    private lateinit var database: OUIDatabase
    
    @Before
    fun setup() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        database = OUIDatabase(context)
        database.clearAll() // Start with clean state
    }
    
    @Test
    fun `Lookup returns correct manufacturer for known OUI`() {
        // Arrange
        database.insert(OUIEntry(
            oui = "AA:BB:CC",
            manufacturer = "Wyze Labs",
            deviceType = "camera",
            threatCategory = "surveillance",
            confidence = 0.95
        ))
        
        // Act
        val result = database.lookup("AA:BB:CC:DD:EE:FF")
        
        // Assert
        assertNotNull(result)
        assertEquals("Wyze Labs", result?.manufacturer)
        assertEquals("camera", result?.deviceType)
    }
    
    @Test
    fun `Lookup returns null for unknown OUI`() {
        val result = database.lookup("99:99:99:DD:EE:FF")
        assertNull(result)
    }
    
    @Test
    fun `Sync updates database correctly`() {
        // Arrange
        val mockApi = mock<RFShieldAPI>()
        val updates = listOf(
            OUIEntry("11:22:33", "Apple", "tracker", "tracking", 0.99),
            OUIEntry("44:55:66", "Tile", "tracker", "tracking", 0.98)
        )
        whenever(mockApi.getOUIUpdates(any())).thenReturn(updates)
        
        // Act
        database.syncFrom(mockApi)
        
        // Assert
        assertEquals(2, database.count())
        assertNotNull(database.lookup("11:22:33:AA:BB:CC"))
    }
}
```

#### 2.1.3 Report Generation Tests

**File:** `ReportGeneratorTest.kt`

```kotlin
class ReportGeneratorTest {
    
    @Test
    fun `PDF report contains all required sections`() {
        // Arrange
        val scan = Scan(
            id = "scan-123",
            timestamp = 1702587600,
            locationName = "Hotel Room 302",
            threats = listOf(
                DetectedDevice(
                    deviceType = DeviceType.WIFI,
                    name = "Wyze_Cam_v3",
                    manufacturer = "Wyze Labs",
                    threatLevel = ThreatLevel.THREAT
                )
            )
        )
        
        val generator = ReportGenerator()
        
        // Act
        val pdf = generator.generatePDF(scan)
        
        // Assert
        assertNotNull(pdf)
        assertTrue(pdf.size > 1000) // Non-empty PDF
        
        // Parse PDF and verify content
        val text = extractTextFromPDF(pdf)
        assertTrue(text.contains("RF Shield Security Report"))
        assertTrue(text.contains("Hotel Room 302"))
        assertTrue(text.contains("Wyze_Cam_v3"))
        assertTrue(text.contains("2024-12-14")) // Date
    }
    
    @Test
    fun `PDF includes cryptographic signature`() {
        val scan = Scan(id = "scan-123", threats = emptyList())
        val generator = ReportGenerator()
        
        val pdf = generator.generatePDF(scan)
        val metadata = extractPDFMetadata(pdf)
        
        assertNotNull(metadata["SHA256"])
        assertEquals(64, metadata["SHA256"]?.length) // SHA-256 hash is 64 hex chars
    }
}
```

### 2.2 Backend (Node.js)

**Framework:** Jest

**Coverage Target:** 85%+

#### 2.2.1 API Endpoint Tests

**File:** `scan-sync.test.ts`

```typescript
import request from 'supertest';
import app from '../src/app';
import { createMockFirebaseToken } from './helpers';

describe('POST /scans/sync', () => {
  
  it('should sync scans for authenticated user', async () => {
    const token = createMockFirebaseToken({ uid: 'user-123', premium: true });
    
    const response = await request(app)
      .post('/v1/scans/sync')
      .set('Authorization', `Bearer ${token}`)
      .send({
        scans: [
          {
            scan_id: 'uuid-scan-1',
            timestamp: 1702587600,
            threats: []
          }
        ]
      });
    
    expect(response.status).toBe(200);
    expect(response.body.success).toBe(true);
    expect(response.body.synced_count).toBe(1);
  });
  
  it('should reject unauthenticated requests', async () => {
    const response = await request(app)
      .post('/v1/scans/sync')
      .send({ scans: [] });
    
    expect(response.status).toBe(401);
    expect(response.body.error).toBe('INVALID_TOKEN');
  });
  
  it('should reject non-premium users', async () => {
    const token = createMockFirebaseToken({ uid: 'user-123', premium: false });
    
    const response = await request(app)
      .post('/v1/scans/sync')
      .set('Authorization', `Bearer ${token}`)
      .send({ scans: [] });
    
    expect(response.status).toBe(403);
    expect(response.body.error).toBe('PREMIUM_REQUIRED');
  });
  
  it('should enforce rate limits', async () => {
    const token = createMockFirebaseToken({ uid: 'user-123', premium: true });
    
    // Make 101 requests (limit is 100/hour)
    for (let i = 0; i < 101; i++) {
      const response = await request(app)
        .post('/v1/scans/sync')
        .set('Authorization', `Bearer ${token}`)
        .send({ scans: [] });
      
      if (i < 100) {
        expect(response.status).toBe(200);
      } else {
        expect(response.status).toBe(429);
        expect(response.body.error).toBe('RATE_LIMIT_EXCEEDED');
      }
    }
  });
});
```

#### 2.2.2 Database Query Tests

**File:** `oui-database.test.ts`

```typescript
import { Pool } from 'pg';
import { OUIDatabase } from '../src/database/oui';

describe('OUI Database', () => {
  let pool: Pool;
  let db: OUIDatabase;
  
  beforeAll(async () => {
    pool = new Pool({ connectionString: process.env.TEST_DATABASE_URL });
    db = new OUIDatabase(pool);
    await db.migrate(); // Run migrations
  });
  
  afterAll(async () => {
    await pool.end();
  });
  
  beforeEach(async () => {
    await db.clearAll(); // Clean state for each test
  });
  
  it('should insert and retrieve OUI entry', async () => {
    await db.insert({
      oui: 'AA:BB:CC',
      manufacturer: 'Wyze Labs',
      device_type: 'camera',
      threat_category: 'surveillance',
      confidence: 0.95
    });
    
    const result = await db.lookup('AA:BB:CC');
    
    expect(result).toBeDefined();
    expect(result?.manufacturer).toBe('Wyze Labs');
  });
  
  it('should handle bulk inserts efficiently', async () => {
    const entries = Array.from({ length: 1000 }, (_, i) => ({
      oui: `${i.toString(16).padStart(2, '0')}:BB:CC`,
      manufacturer: `Manufacturer ${i}`,
      device_type: 'unknown',
      threat_category: null,
      confidence: 0.5
    }));
    
    const startTime = Date.now();
    await db.bulkInsert(entries);
    const duration = Date.now() - startTime;
    
    expect(duration).toBeLessThan(1000); // < 1 second for 1000 entries
    expect(await db.count()).toBe(1000);
  });
});
```

### 2.3 Hardware Firmware (ESP32)

**Framework:** Unity (PlatformIO)

**Coverage Target:** 70%+

#### 2.3.1 WiFi Scanner Tests

**File:** `test_wifi_scanner.cpp`

```cpp
#include <unity.h>
#include "WiFiScanner.h"

void test_wifi_scan_returns_results() {
    WiFiScanner scanner;
    auto results = scanner.scan();
    
    // Should find at least 1 network (test environment has AP)
    TEST_ASSERT_GREATER_THAN(0, results.size());
}

void test_wifi_scan_includes_required_fields() {
    WiFiScanner scanner;
    auto results = scanner.scan();
    
    if (results.size() > 0) {
        auto device = results[0];
        TEST_ASSERT_NOT_EQUAL("", device.bssid);
        TEST_ASSERT_GREATER_THAN(-100, device.rssi);
        TEST_ASSERT_GREATER_OR_EQUAL(1, device.channel);
        TEST_ASSERT_LESS_OR_EQUAL(14, device.channel);
    }
}

void test_frequency_to_channel_conversion() {
    WiFiScanner scanner;
    
    TEST_ASSERT_EQUAL(1, scanner.frequencyToChannel(2412));
    TEST_ASSERT_EQUAL(6, scanner.frequencyToChannel(2437));
    TEST_ASSERT_EQUAL(11, scanner.frequencyToChannel(2462));
}

void setup() {
    UNITY_BEGIN();
    RUN_TEST(test_wifi_scan_returns_results);
    RUN_TEST(test_wifi_scan_includes_required_fields);
    RUN_TEST(test_frequency_to_channel_conversion);
    UNITY_END();
}

void loop() {
    // Empty - tests run once in setup()
}
```

---

## 3. Integration Testing

### 3.1 Mobile ↔ Backend Integration

**Test Scope:** API calls, authentication, data sync

#### Test Case INT-001: User Authentication Flow

**Preconditions:**
- Backend API running
- Firebase Auth configured
- Test user account exists

**Steps:**
1. Mobile app calls Firebase `signInWithEmailAndPassword()`
2. Firebase returns JWT token
3. App sends token to backend `/user/profile` endpoint
4. Backend validates token with Firebase Admin SDK
5. Backend returns user profile

**Expected Results:**
- JWT token received from Firebase
- Backend validates token successfully
- User profile returned with correct data
- Response time <200ms

**Actual Results:** _[To be filled during test execution]_

**Status:** ☐ Pass ☐ Fail ☐ Blocked

---

#### Test Case INT-002: Scan Sync to Cloud

**Preconditions:**
- User authenticated (premium tier)
- User has completed local scan
- Backend API running

**Steps:**
1. App creates scan object (timestamp, threats, location)
2. App calls `POST /scans/sync` with JWT token
3. Backend validates token
4. Backend validates premium status
5. Backend stores scan in Firestore
6. Backend returns success response

**Expected Results:**
- Scan synced successfully (200 OK)
- Scan visible in Firestore console
- Response includes `synced_count: 1`
- Sync completes <1 second

**Actual Results:** _[To be filled]_

**Status:** ☐ Pass ☐ Fail ☐ Blocked

---

### 3.2 Mobile ↔ Hardware Integration

**Test Scope:** Bluetooth communication, hardware control

#### Test Case INT-010: ESP32 Pairing

**Preconditions:**
- ESP32 module powered on
- Mobile app has Bluetooth permission
- Bluetooth enabled on phone

**Steps:**
1. App scans for BLE devices
2. App discovers "RF-Shield-ESP32-XXXXXX"
3. App connects to ESP32
4. App discovers GATT service (0000fff0-...)
5. App subscribes to response characteristic
6. ESP32 sends status notification

**Expected Results:**
- ESP32 discovered within 5 seconds
- Connection established <5 seconds
- All characteristics discovered
- Status notification received

**Pass Criteria:**
- ✓ Device discovered
- ✓ Connection successful
- ✓ Service/characteristics found
- ✓ Notifications working

**Status:** ☐ Pass ☐ Fail ☐ Blocked

---

#### Test Case INT-011: WiFi Scan via ESP32

**Preconditions:**
- ESP32 connected to app
- Test environment has WiFi networks

**Steps:**
1. App sends WiFi scan command (JSON)
2. ESP32 receives command
3. ESP32 performs WiFi scan
4. ESP32 sends results via BLE notification
5. App parses JSON response
6. App displays results

**Expected Results:**
- Command sent successfully
- Scan completes within 10 seconds
- Results contain ≥1 WiFi network
- Results include: BSSID, SSID, RSSI, channel

**Validation:**
```json
{
  "status": "success",
  "data": {
    "type": "wifi",
    "devices": [
      {
        "bssid": "AA:BB:CC:DD:EE:FF",
        "ssid": "Test_Network",
        "rssi": -45,
        "channel": 6
      }
    ]
  }
}
```

**Status:** ☐ Pass ☐ Fail ☐ Blocked

---

### 3.3 Backend ↔ Database Integration

**Test Scope:** Database queries, transactions, migrations

#### Test Case INT-020: OUI Database Sync

**Preconditions:**
- PostgreSQL database running
- Test data available (IEEE OUI registry sample)

**Steps:**
1. Backend fetches OUI updates from IEEE
2. Backend parses OUI text file
3. Backend starts transaction
4. Backend bulk inserts new OUIs
5. Backend commits transaction
6. Backend increments version number

**Expected Results:**
- 1000+ OUIs inserted
- Transaction completes successfully
- Version incremented
- No duplicate OUIs

**Performance:**
- Insert 10,000 OUIs in <5 seconds

**Status:** ☐ Pass ☐ Fail ☐ Blocked

---

## 4. System Testing

### 4.1 End-to-End User Flows

#### Test Case SYS-001: Complete Hotel Room Scan Flow

**User Story:** US-1.1 - US-1.4 (Quick Room Scan)

**Preconditions:**
- User logged in (free tier)
- User in test environment with WiFi camera (Wyze Cam)

**Test Steps:**

**Step 1: Initiate Scan**
- User taps "Scan This Room"
- ✓ Scan progress shown
- ✓ Scan completes <60 seconds

**Step 2: View Results**
- Results screen displays
- ✓ Shows "1 Threat Detected"
- ✓ Lists Wyze_Cam_v3 as THREAT
- ✓ Shows all other devices as SAFE

**Step 3: Investigate Threat**
- User taps on Wyze_Cam_v3
- ✓ Detail screen shows manufacturer, RSSI, channel
- ✓ Threat reason: "WiFi camera detected"
- ✓ Action buttons visible: [Find It], [Take Photo], [Export Report]

**Step 4: Locate Device**
- User taps [Find It]
- ✓ Hot/cold locator activates
- ✓ RSSI meter updates in real-time
- ✓ Haptic feedback when close
- User moves near camera
- ✓ Meter shows "HOT" (signal >-40 dBm)

**Step 5: Document Evidence**
- User taps [Take Photo]
- ✓ Camera opens
- User takes photo
- ✓ Photo attached to threat

**Step 6: Export Report**
- User taps [Export Report]
- ✓ PDF generated <5 seconds
- ✓ PDF contains: timestamp, location, threat details, photo
- ✓ PDF cryptographically signed
- ✓ Share dialog appears

**Expected Results:**
- All steps complete successfully
- User can identify, locate, document, and report threat
- Total flow time <5 minutes

**Actual Results:** _[To be filled]_

**Status:** ☐ Pass ☐ Fail ☐ Blocked

---

#### Test Case SYS-002: AirTag Detection & Removal

**User Story:** US-2.1 - US-2.4 (AirTag Detection)

**Preconditions:**
- User has free tier app
- AirTag (not owned by user) placed nearby

**Test Steps:**

**Step 1: Open App**
- User opens RF Shield
- ✓ Home screen displays
- ✓ "Find AirTag" button prominent

**Step 2: Scan for AirTags**
- User taps "Find AirTag"
- ✓ Scan runs <15 seconds
- ✓ Results show "Unknown AirTag Detected"
- ✓ Status: "Separated from Owner: Yes"

**Step 3: Locate AirTag**
- User taps [Locate It]
- ✓ RSSI meter activates
- User walks toward AirTag
- ✓ Signal strengthens
- ✓ Haptic feedback increases
- User finds AirTag
- ✓ RSSI <-30 dBm (very close)

**Step 4: Play Sound (optional)**
- User taps [Play Sound]
- ✓ AirTag beeps
- ✓ Confirmation message shown

**Step 5: Document Evidence**
- User removes AirTag
- App detects signal lost
- ✓ Prompt: "Document this as evidence?"
- User taps "Yes"
- ✓ Photo capture opens
- User takes photos
- ✓ Evidence report generated

**Step 6: Access Resources**
- ✓ DV hotline number displayed
- ✓ Local shelter info shown
- ✓ Legal aid resources listed

**Expected Results:**
- AirTag found and removed
- Evidence documented
- User connected to support resources

**Actual Results:** _[To be filled]_

**Status:** ☐ Pass ☐ Fail ☐ Blocked

---

### 4.2 Cross-Platform Testing

**Test Matrix:**

| Device | OS | Scan | BLE | Hardware | Report | Status |
|--------|----|----|-----|----------|---------|---------|
| Pixel 6 | Android 13 | ☐ | ☐ | ☐ | ☐ | ☐ |
| Samsung S23 | Android 14 | ☐ | ☐ | ☐ | ☐ | ☐ |
| OnePlus 9 | Android 13 | ☐ | ☐ | ☐ | ☐ | ☐ |
| iPhone 13 | iOS 17 | ☐ | ☐ | ☐ | ☐ | ☐ |
| iPhone 15 Pro | iOS 18 | ☐ | ☐ | ☐ | ☐ | ☐ |
| iPad Pro | iPadOS 17 | ☐ | ☐ | ☐ | ☐ | ☐ |

**Test Cases per Device:**
- Quick scan (phone sensors only)
- BLE AirTag detection
- ESP32 module pairing
- WiFi scan via ESP32
- PDF report generation
- Cloud sync (premium)

---

## 5. Performance Testing

### 5.1 App Performance Metrics

#### Test Case PERF-001: App Launch Time

**Measurement:**
- **Cold Start:** App not in memory
- **Warm Start:** App in background

**Target Metrics:**
- Cold start: <2 seconds
- Warm start: <500ms

**Test Procedure:**
1. Force close app
2. Start stopwatch
3. Tap app icon
4. Stop when home screen fully rendered

**Results:**

| Device | OS | Cold Start | Warm Start | Pass? |
|--------|----|-----------  |------------|-------|
| Pixel 6 | Android 13 | _____ms | _____ms | ☐ |
| iPhone 13 | iOS 17 | _____ms | _____ms | ☐ |

---

#### Test Case PERF-002: Scan Speed

**Target Metrics:**
- Quick scan (phone only): <60 seconds
- Full scan (all modules): <5 minutes

**Test Procedure:**
1. Initiate scan
2. Measure time from tap to results displayed
3. Repeat 10 times, calculate average

**Results:**

| Scan Type | Trial 1 | Trial 2 | Trial 3 | Avg | Pass? |
|-----------|---------|---------|---------|-----|-------|
| Quick (WiFi+BLE) | ___s | ___s | ___s | ___s | ☐ |
| Full (ESP32+SDR) | ___s | ___s | ___s | ___s | ☐ |

---

#### Test Case PERF-003: Battery Impact

**Target Metrics:**
- Quick scan: <3% battery drain
- 1-hour continuous monitoring: <5% battery drain

**Test Procedure:**
1. Fully charge device to 100%
2. Note battery level
3. Perform operation (scan or monitoring)
4. Note battery level after
5. Calculate drain percentage

**Results:**

| Operation | Start % | End % | Drain % | Pass? |
|-----------|---------|-------|---------|-------|
| Quick Scan | 100% | ___% | ___% | ☐ |
| 1hr Monitor | 100% | ___% | ___% | ☐ |

---

### 5.2 Backend Performance Testing

#### Test Case PERF-010: API Load Testing

**Tool:** Apache JMeter or Artillery

**Scenario:** Simulate 1,000 concurrent users

**Endpoints to Test:**
- `GET /oui/updates` (read-heavy)
- `POST /scans/sync` (write-heavy)
- `GET /scans/history` (read-heavy)

**Target Metrics:**
- Response time p95: <200ms
- Error rate: <0.1%
- Throughput: >100 req/sec

**Test Configuration:**
```yaml
# Artillery config
config:
  target: 'https://api-staging.rfshield.io'
  phases:
    - duration: 60
      arrivalRate: 10
      rampTo: 100
scenarios:
  - name: "Sync Scans"
    flow:
      - post:
          url: "/v1/scans/sync"
          headers:
            Authorization: "Bearer ${token}"
          json:
            scans: [...]
```

**Results:**

| Endpoint | p50 | p95 | p99 | Error % | Pass? |
|----------|-----|-----|-----|---------|-------|
| /oui/updates | ___ms | ___ms | ___ms | ___% | ☐ |
| /scans/sync | ___ms | ___ms | ___ms | ___% | ☐ |

---

### 5.3 Hardware Performance Testing

#### Test Case PERF-020: ESP32 Scan Time

**Target:** WiFi scan (all 14 channels) <3 seconds

**Test Procedure:**
1. Send WiFi scan command to ESP32
2. Measure time until response received
3. Repeat 20 times

**Results:**

| Trial | Time (ms) | Pass? |
|-------|-----------|-------|
| 1-5 avg | _____ms | ☐ |
| 6-10 avg | _____ms | ☐ |
| Overall avg | _____ms | ☐ |

---

## 6. Security Testing

### 6.1 Authentication & Authorization

#### Test Case SEC-001: JWT Token Validation

**Test:**
1. Request API with expired token
2. Request API with invalid signature
3. Request API with tampered payload

**Expected:**
- All requests return 401 Unauthorized
- No data leaked

**Status:** ☐ Pass ☐ Fail

---

#### Test Case SEC-002: Premium Feature Access Control

**Test:**
1. Free tier user attempts `/scans/sync`
2. Free tier user attempts >3 scans/day
3. Expired premium user attempts premium features

**Expected:**
- All requests return 403 Forbidden
- Clear error message

**Status:** ☐ Pass ☐ Fail

---

### 6.2 Data Encryption

#### Test Case SEC-010: Data at Rest Encryption

**Test:**
1. Create scan with sensitive data
2. Access SQLite database file directly
3. Attempt to read without decryption key

**Expected:**
- Database file encrypted (SQLCipher)
- Data unreadable without key

**Validation:**
```bash
# Attempt to open encrypted DB without key
sqlite3 /data/data/com.rfshield.app/databases/scans.db
# Should fail or show garbage data
```

**Status:** ☐ Pass ☐ Fail

---

#### Test Case SEC-011: Data in Transit Encryption

**Test:**
1. Capture network traffic during API call
2. Analyze packets with Wireshark
3. Verify TLS 1.3 used
4. Verify certificate valid

**Expected:**
- All traffic encrypted
- TLS 1.3 or higher
- Certificate matches domain
- No unencrypted data

**Status:** ☐ Pass ☐ Fail

---

### 6.3 Penetration Testing

#### Test Case SEC-020: OWASP Top 10 Scan

**Tool:** OWASP ZAP or Burp Suite

**Tests:**
1. SQL Injection
2. XSS (Cross-Site Scripting)
3. CSRF (Cross-Site Request Forgery)
4. Insecure Deserialization
5. Broken Authentication
6. Sensitive Data Exposure
7. XML External Entities (XXE)
8. Broken Access Control
9. Security Misconfiguration
10. Insufficient Logging

**Results:**

| Vulnerability | Severity | Found? | Fixed? |
|---------------|----------|--------|--------|
| SQL Injection | Critical | ☐ Yes ☐ No | ☐ |
| XSS | High | ☐ Yes ☐ No | ☐ |
| CSRF | Medium | ☐ Yes ☐ No | ☐ |
| ... | ... | ... | ☐ |

---

#### Test Case SEC-021: Mobile App Security Scan

**Tool:** MobSF (Mobile Security Framework)

**Android Tests:**
- Insecure data storage
- Weak cryptography
- Insecure communication
- Code obfuscation
- Root detection bypass

**iOS Tests:**
- Keychain usage
- ATS (App Transport Security)
- Binary protections
- Jailbreak detection

**Results:** _[MobSF report attached]_

**Status:** ☐ Pass ☐ Fail

---

## 7. Acceptance Testing

### 7.1 Beta User Testing

**Participants:** 50-100 beta testers

**Duration:** 4-6 weeks

**Platforms:**
- 50% Android (various devices)
- 50% iOS (various devices)

**Test Scenarios:**
1. Hotel room scan
2. AirTag detection
3. Hardware module usage
4. Report generation
5. Premium subscription

**Feedback Collection:**
- In-app surveys (after each scan)
- Weekly feedback forms
- Focus group sessions (10 users)
- Bug reports (via TestFlight/Play Beta)

**Success Criteria:**
- CSAT (Customer Satisfaction): 4.5+/5
- NPS (Net Promoter Score): 50+
- Critical bugs: <5
- Feature completion rate: >90%

---

### 7.2 User Acceptance Test Cases

#### UAT-001: Sarah's Hotel Room Scan

**Persona:** Privacy-Conscious Traveler

**Scenario:** Sarah checks into hotel, wants to scan room

**Steps:**
1. Sarah opens app
2. Sarah taps "Scan This Room"
3. Scan completes, shows 1 threat (WiFi camera)
4. Sarah investigates threat
5. Sarah uses hot/cold locator
6. Sarah finds camera
7. Sarah exports report
8. Sarah contacts hotel

**Acceptance Criteria:**
- ✓ Easy to use (no instructions needed)
- ✓ Scan completes <2 minutes
- ✓ Results clear and actionable
- ✓ Locator accurate (<2m)
- ✓ Report professional

**User Feedback:** _[To be collected]_

**Status:** ☐ Pass ☐ Fail

---

#### UAT-002: Maria's AirTag Removal

**Persona:** Domestic Violence Survivor

**Scenario:** Maria suspects tracking, uses app to find AirTag

**Steps:**
1. Maria downloads free app
2. Maria taps "Find AirTag"
3. App detects AirTag
4. Maria follows hot/cold guide
5. Maria removes AirTag
6. Maria documents evidence

**Acceptance Criteria:**
- ✓ Free tier sufficient
- ✓ Clear instructions (low tech literacy)
- ✓ Found tracker successfully
- ✓ Evidence report generated
- ✓ Resources provided (DV hotline)

**User Feedback:** _[To be collected]_

**Status:** ☐ Pass ☐ Fail

---

## 8. Test Environments

### 8.1 Development Environment

**Purpose:** Developer testing during development

**Infrastructure:**
- Backend: Local (Docker Compose)
- Database: PostgreSQL (local)
- Firebase: Emulator
- Mobile: Emulators/Simulators

**Data:** Mock/synthetic data

---

### 8.2 Staging Environment

**Purpose:** QA testing before production

**Infrastructure:**
- Backend: GCP Cloud Run (staging)
- Database: Cloud SQL (staging)
- Firebase: Staging project
- Mobile: TestFlight/Play Beta

**Data:** Anonymized production data

**URL:** https://api-staging.rfshield.io

---

### 8.3 Production Environment

**Purpose:** Live user traffic

**Infrastructure:**
- Backend: GCP Cloud Run (production)
- Database: Cloud SQL (production)
- Firebase: Production project
- CDN: Cloudflare

**URL:** https://api.rfshield.io

---

## 9. Test Data

### 9.1 Test Devices (WiFi)

**Mock WiFi Networks:**

| SSID | BSSID | OUI | Type | Expected Result |
|------|-------|-----|------|-----------------|
| Wyze_Cam_v3 | AA:BB:CC:11:22:33 | AA:BB:CC (Wyze) | Camera | THREAT |
| Home_WiFi | 11:22:33:44:55:66 | 11:22:33 (Netgear) | Router | SAFE |
| Hidden_Network | 99:88:77:66:55:44 | 99:88:77 (Unknown) | Unknown | INVESTIGATE |

### 9.2 Test Devices (BLE)

**Mock BLE Devices:**

| Name | MAC | Manufacturer Data | Type | Expected Result |
|------|-----|-------------------|------|-----------------|
| AirTag | AA:BB:CC:DD:EE:01 | 4C 00 12 19 10 | AirTag (separated) | THREAT |
| Tile | 11:22:33:44:55:01 | ... | Tracker | INVESTIGATE |
| AirPods Pro | AA:BB:CC:DD:EE:02 | 4C 00 07 ... | Headphones | SAFE |

### 9.3 Test Users

**Test Accounts:**

| Email | Password | Tier | Premium Expires | Purpose |
|-------|----------|------|-----------------|---------|
| test-free@rfshield.io | Test1234! | Free | N/A | Free tier testing |
| test-premium@rfshield.io | Test1234! | Premium | 2025-12-31 | Premium feature testing |
| test-pro@rfshield.io | Test1234! | Pro | Lifetime | Pro tier testing |
| test-expired@rfshield.io | Test1234! | Free | 2024-01-01 (expired) | Expiry handling |

---

## 10. Defect Management

### 10.1 Bug Severity Levels

**P0 - Critical:**
- App crashes on launch
- Data loss
- Security vulnerabilities
- Payment processing fails

**Fix SLA:** 24 hours

---

**P1 - High:**
- Core feature broken (scanning doesn't work)
- Major UI issues
- Performance degradation >50%

**Fix SLA:** 3 days

---

**P2 - Medium:**
- Minor feature issues
- UI glitches
- Non-critical errors

**Fix SLA:** 1 week

---

**P3 - Low:**
- Cosmetic issues
- Minor inconsistencies
- Nice-to-have features

**Fix SLA:** Next sprint

---

### 10.2 Bug Report Template

```markdown
**Title:** [Brief description]

**Severity:** P0 / P1 / P2 / P3

**Environment:**
- OS: Android 13 / iOS 17
- Device: Pixel 6 / iPhone 13
- App Version: 1.0.0
- Build: 123

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected Result:**
[What should happen]

**Actual Result:**
[What actually happens]

**Screenshots/Logs:**
[Attach if available]

**Frequency:**
Always / Sometimes / Rare

**Workaround:**
[If known]
```

---

### 10.3 Test Metrics

**Tracked Metrics:**

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Test Coverage (Unit) | 80% | ___% | ☐ |
| Test Coverage (Integration) | 70% | ___% | ☐ |
| Pass Rate | 95% | ___% | ☐ |
| Critical Bugs (P0) | 0 | ___ | ☐ |
| High Bugs (P1) | <5 | ___ | ☐ |
| Crash Rate | <1% | ___% | ☐ |
| CSAT (Beta) | 4.5+ | ___ | ☐ |

---

**END OF TESTING PLAN**
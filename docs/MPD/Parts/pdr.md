# Product Requirements Document (PRD)
# RF Shield - Privacy Protection Platform

**Version:** 1.0  
**Date:** December 14, 2024  
**Author:** Product Team  
**Status:** Draft

---

## 1. Executive Summary

### 1.1 Product Vision
RF Shield is a comprehensive privacy protection platform that detects and neutralizes hidden surveillance devices (cameras, microphones, GPS trackers) in hotels, rentals, offices, and vehicles. By combining smartphone sensors with optional hardware modules, RF Shield democratizes professional-grade TSCM (Technical Surveillance Counter-Measures) capabilities at consumer prices.

### 1.2 Problem Statement
**Current Market Pain Points:**
- 67% of travelers worry about hidden cameras in hotels/Airbnbs
- AirTag stalking epidemic: 50+ documented cases in 2023
- Professional bug sweeps cost $2,000-10,000 per session
- Consumer detection tools are either ineffective toys ($30-80) or require expertise
- No integrated solution for detection + neutralization

**Target User Challenges:**
- Privacy-conscious travelers have no affordable protection
- Domestic violence survivors need tracker detection (<$100 budget)
- Business executives face corporate espionage threats
- No way to verify Airbnb/hotel room privacy
- GPS-only trackers are undetectable by consumers

### 1.3 Solution Overview
**RF Shield provides:**

**Detection Capabilities:**
- WiFi cameras (IP cameras, nanny cams) - 90% detection rate
- BLE trackers (AirTags, Tile, SmartTag) - 95% detection rate
- Cellular GPS trackers - 70-85% detection rate
- 433/315 MHz RF bugs - 80% detection rate (with ESP32 module)
- Analog wireless cameras - 85% detection rate (with SDR module)
- Wired cameras via lens detection - 70% detection rate (with camera module)

**Countermeasure Capabilities:**
- Ultrasonic audio jamming (25 kHz, disrupts MEMS microphones)
- IR flooding (blinds night vision cameras)
- Faraday isolation (blocks wireless transmission)
- Physical location guidance (hot/cold proximity tracking)

**Integrated Platform:**
- Mobile app (Android/iOS) - free tier + premium ($79/year)
- ESP32 Marauder module ($79) - WiFi/BLE/Sub-GHz detection
- RTL-SDR module ($79) - Wideband spectrum analysis
- Camera module ($49) - Optical lens detection
- Countermeasure modules ($59-149) - Ultrasonic jammer, IR flood
- Full kit bundle ($299) - All hardware + lifetime premium

### 1.4 Success Metrics

**Year 1 Targets:**
- 100,000 app downloads
- 5,000 premium subscribers ($395k ARR)
- 2,000 hardware units sold ($316k revenue)
- 4.5+ star rating (App Store/Play Store)
- <5% false positive rate
- 80%+ threat detection accuracy

**Year 3 Targets:**
- 2M app downloads
- 200,000 premium subscribers ($15.8M ARR)
- 50,000 hardware units sold ($7.5M revenue)
- Strategic partnerships (2+ hotel chains, 3+ insurance companies)
- TSCM professional network (50+ referral partners)

---

## 2. User Personas & Use Cases

### 2.1 Primary Personas

#### Persona 1: "Privacy-Conscious Traveler" - Sarah
**Demographics:**
- Age: 32
- Occupation: Marketing Manager
- Income: $75k/year
- Tech-savvy: High

**Pain Points:**
- Travels 2-3x/month for work (hotels, Airbnbs)
- Heard horror stories about hidden cameras
- Doesn't trust "smart" hotel rooms (Alexa, cameras everywhere)
- Willing to pay for peace of mind

**Goals:**
- Quick room scan (<5 minutes)
- Confidence that room is private
- Easy-to-use tool (not technical)

**Solution Fit:**
- App-only tier ($79/year) or Privacy Kit ($149)
- One-tap "Scan Room" feature
- Clear "Safe/Unsafe" results
- Countermeasures if threat found

**User Journey:**
1. Checks into hotel
2. Opens RF Shield app
3. Taps "Scan This Room"
4. Walks around room for 60 seconds
5. Reviews results: "2 cameras detected (lobby security - expected), 0 threats"
6. Sleeps soundly

#### Persona 2: "Domestic Violence Survivor" - Maria
**Demographics:**
- Age: 28
- Occupation: Retail worker
- Income: $32k/year
- Tech-savvy: Low

**Pain Points:**
- Ex-partner stalking with GPS tracker
- Limited budget (<$100)
- Needs to find tracker immediately
- Doesn't understand technical jargon

**Goals:**
- Find AirTag/GPS tracker on car
- Simple instructions
- Affordable solution
- Immediate action

**Solution Fit:**
- Free app tier (BLE tracker detection)
- "Find AirTag" feature with hot/cold guidance
- Partnership with domestic violence orgs (free premium codes)
- Clear "What to do next" instructions

**User Journey:**
1. Downloads free app (recommended by shelter advocate)
2. Scans car for trackers
3. Finds AirTag under bumper (hot/cold guidance)
4. Removes tracker
5. Reports to police (app exports evidence report)

#### Persona 3: "Corporate Executive" - James
**Demographics:**
- Age: 48
- Occupation: VP of Engineering at tech startup
- Income: $250k/year
- Tech-savvy: High

**Pain Points:**
- Frequent travel to competitor conferences
- Corporate espionage concerns
- Needs comprehensive protection
- Willing to pay premium

**Goals:**
- Detect all threat types (cameras, bugs, trackers)
- Professional-grade results
- Export reports for security team
- Countermeasures when needed

**Solution Fit:**
- Executive Protection Kit ($299)
- All hardware modules (ESP32 + SDR + camera + countermeasures)
- Lifetime premium app
- Optional TSCM pro referral ($999 tier)

**User Journey:**
1. Arrives at conference hotel
2. Full sweep with all modules (15 minutes)
3. Detects: Evil twin WiFi, 433 MHz bug in lamp
4. Activates countermeasures: Ultrasonic jammer, avoids rogue AP
5. Exports report to company InfoSec team
6. Requests pro TSCM sweep for office (via app referral)

### 2.2 Secondary Personas

#### Persona 4: "Privacy Advocate" - Alex
- Age: 25, Student/Activist
- Use Case: Protests, meetings, public spaces
- Budget: $0-50
- Needs: Free app, open-source hardware

#### Persona 5: "Private Investigator" - Detective Rodriguez
- Age: 42, Licensed PI
- Use Case: Client sweeps, evidence gathering
- Budget: $500-2000
- Needs: Professional reports, court-admissible evidence

#### Persona 6: "Small Business Owner" - Restaurant Owner
- Age: 55
- Use Case: Protect trade secrets, verify employees not recording
- Budget: $200-500
- Needs: 24/7 monitoring, simple setup

### 2.3 Core Use Cases

#### Use Case 1: Hotel Room Privacy Check
**Actor:** Privacy-conscious traveler  
**Precondition:** User checked into hotel room  
**Trigger:** User opens RF Shield app  
**Main Flow:**
1. User taps "Scan This Room"
2. App performs WiFi scan (5 seconds)
3. App performs BLE scan (10 seconds)
4. App analyzes cellular activity (optional, 30 seconds)
5. App displays results:
   - "2 WiFi cameras detected" (map shows locations)
   - "Bedroom camera: Wyze Cam v3 (🚨 UNEXPECTED)"
   - "Lobby camera: Nest Cam (✅ EXPECTED)"
6. User investigates bedroom camera
7. User uses hot/cold locator feature
8. User finds camera in smoke detector
9. User contacts hotel management
10. App exports evidence report (PDF with photos, timestamps)

**Alternate Flows:**
- 5a. No threats detected → "Room is clear" message
- 5b. AirTag detected → Immediate critical alert
- 8a. Camera is legitimate (user's own device) → User marks as "safe"

**Postcondition:** User has confidence in room privacy

**Success Criteria:**
- <60 second scan time
- Clear threat vs. expected device distinction
- Actionable next steps provided

#### Use Case 2: AirTag Stalking Detection
**Actor:** Potential stalking victim  
**Precondition:** User suspects being tracked  
**Trigger:** User downloads app (free tier)  
**Main Flow:**
1. User opens app
2. User taps "Find AirTag"
3. App scans for BLE trackers (15 seconds)
4. App detects: "Unknown AirTag - not yours"
5. User taps "Locate It"
6. App shows RSSI meter (hot/cold game)
7. User walks around car
8. RSSI increases near rear bumper
9. User finds AirTag under bumper
10. App plays sound on AirTag (confirmation)
11. User removes AirTag
12. App offers: "Report to Police" (exports evidence)

**Alternate Flows:**
- 4a. No AirTag found → "No trackers detected, but check physically"
- 4b. User's own AirTag detected → "This AirTag is registered to you"

**Postcondition:** Tracker removed, evidence documented

**Success Criteria:**
- 100% AirTag detection rate (if within BLE range)
- <1 meter location accuracy
- Clear instructions for non-technical users

#### Use Case 3: Corporate Espionage Prevention
**Actor:** Business executive  
**Precondition:** User has Executive Protection Kit  
**Trigger:** User enters conference hotel room  
**Main Flow:**
1. User places ESP32 module in center of room
2. User opens app, taps "Full Scan"
3. ESP32 performs:
   - WiFi scan (all channels)
   - BLE scan (extended range)
   - 433/315 MHz sweep
4. App connects via WiFi Direct to ESP32
5. Results after 2 minutes:
   - "Evil twin AP detected: 'Conference_WiFi_Guest'"
   - "433 MHz transmitter detected (desk lamp)"
   - "2 expected cameras (hallway security)"
6. User investigates lamp with hot/cold feature
7. User finds RF bug in lamp base
8. User activates ultrasonic jammer (audio protection)
9. User avoids evil twin AP (uses VPN on cellular)
10. User exports comprehensive report
11. User emails report to company security team

**Alternate Flows:**
- 5a. No threats → User still activates countermeasures (paranoid mode)
- 7a. Can't physically access bug → User uses Faraday bag isolation

**Postcondition:** User protected from surveillance, evidence collected

**Success Criteria:**
- Detect sophisticated threats (evil twins, RF bugs)
- Export professional report (PDF with technical details)
- Countermeasures effective (audio unintelligible when jammer active)

---

## 3. Functional Requirements

### 3.1 Mobile Application (Android/iOS)

#### 3.1.1 Core Detection Features

**FR-1.1: Quick Scan Mode**
- **Description:** One-tap scan of environment for common threats
- **Priority:** P0 (Must-have for MVP)
- **Acceptance Criteria:**
  - User taps "Scan This Room" button
  - Scan completes in <60 seconds
  - Results show: WiFi cameras, BLE trackers, threat count
  - Color-coded alerts: Green (safe), Yellow (investigate), Red (threat)
- **Technical Notes:**
  - WiFi scan uses Android WifiManager / iOS NEHotspotHelper
  - BLE scan uses Android BluetoothLeScanner / iOS CoreBluetooth
  - Background processing, UI remains responsive

**FR-1.2: Continuous Monitoring Mode**
- **Description:** Background scanning for new devices appearing
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - User enables "Monitor" toggle
  - App scans every 5 minutes (configurable)
  - Push notification if new device detected
  - Battery impact <5% per day
- **Technical Notes:**
  - Android: Use WorkManager for periodic scans
  - iOS: Limited background BLE scanning only
  - Smart scheduling (reduce frequency when stationary)

**FR-1.3: Device Locator (Hot/Cold)**
- **Description:** Guide user to physical location of detected threat
- **Priority:** P0 (Must-have for MVP)
- **Acceptance Criteria:**
  - User selects detected threat from list
  - User taps "Find It" button
  - RSSI meter shows signal strength (visual + haptic feedback)
  - Accuracy: <2 meter location estimate
- **Technical Notes:**
  - Use RSSI triangulation (multiple scan points)
  - Kalman filter for RSSI smoothing
  - Haptic feedback increases as signal strengthens

**FR-1.4: Threat Database Matching**
- **Description:** Identify device type from MAC/UUID signatures
- **Priority:** P0 (Must-have for MVP)
- **Acceptance Criteria:**
  - Device MAC matched against OUI database (100k+ entries)
  - Common devices identified: "Wyze Cam v3", "Apple AirTag", etc.
  - Unknown devices labeled: "Unknown WiFi Device"
  - Database updates weekly (cloud sync)
- **Technical Notes:**
  - Local SQLite database (50 MB, common OUIs)
  - Cloud database (full, 500 MB, optional download)
  - ML classifier for unknown devices (v2.0)

**FR-1.5: Safe Zone Baseline**
- **Description:** Establish expected devices, alert on new additions
- **Priority:** P2 (v2.0 feature)
- **Acceptance Criteria:**
  - User taps "Set as Safe Zone"
  - App records all current devices
  - Future scans compare against baseline
  - Alert: "New device detected since baseline"
- **Technical Notes:**
  - Store baseline per location (geofence)
  - 7-day auto-expiration (devices change)

#### 3.1.2 Hardware Module Integration

**FR-2.1: ESP32 Module Connection**
- **Description:** Pair with ESP32 Marauder module via Bluetooth
- **Priority:** P0 (Must-have for MVP)
- **Acceptance Criteria:**
  - User taps "Connect Hardware"
  - App discovers ESP32 via BLE advertisement
  - Connection established <5 seconds
  - Firmware version check (ensure compatibility)
- **Technical Notes:**
  - BLE GATT protocol (custom service UUID)
  - Automatic reconnection if disconnected
  - OTA firmware updates via app

**FR-2.2: SDR Module Connection**
- **Description:** Connect RTL-SDR via USB OTG (Android only initially)
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - User connects RTL-SDR to USB-C port
  - App detects RTL-SDR device
  - Spectrum scan available in UI
  - Results: "Scanning 1 MHz - 1.7 GHz..."
- **Technical Notes:**
  - Use rtl_sdr Android library (libusb wrapper)
  - iOS: Not supported (no USB OTG access)
  - Power management (RTL-SDR draws 300 mA)

**FR-2.3: Camera Module Integration**
- **Description:** Use phone camera + clip-on lens for optical detection
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - User attaches camera module
  - User taps "Lens Finder" mode
  - Camera feed shows with ML overlay
  - Detected lenses highlighted with bounding boxes
- **Technical Notes:**
  - TensorFlow Lite on-device inference
  - Model: MobileNetV3 (lens classifier)
  - Real-time processing: 15-30 FPS

#### 3.1.3 Countermeasure Controls

**FR-3.1: Ultrasonic Jammer Control**
- **Description:** Activate/deactivate ultrasonic audio jammer module
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - User taps "Activate Audio Protection"
  - App sends Bluetooth command to jammer module
  - Confirmation: "Ultrasonic jammer active (25 kHz)"
  - Auto shut-off after 2 hours (safety)
- **Technical Notes:**
  - BLE command: `{cmd: "jammer", state: "on", freq: 25000}`
  - Battery monitoring (warn if <20%)
  - Manual override (disable auto-shutoff)

**FR-3.2: IR Flood Control**
- **Description:** Activate IR flood light to blind cameras
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - User taps "Blind Cameras"
  - IR flood activates at full power
  - Pulse mode option (conserve battery)
  - Brightness control: 0-100%
- **Technical Notes:**
  - PWM control via BLE
  - Thermal monitoring (auto-shutoff if >80°C)

**FR-3.3: Faraday Bag Verification**
- **Description:** Verify device is in Faraday bag (no RF leakage)
- **Priority:** P2 (v2.0 feature)
- **Acceptance Criteria:**
  - User places suspected tracker in Faraday bag
  - App scans for RF emissions
  - Confirmation: "No RF detected - isolation effective"
- **Technical Notes:**
  - Scan all bands (WiFi, BLE, cellular)
  - Signal threshold: <-90 dBm = isolated

#### 3.1.4 Reporting & Evidence

**FR-4.1: Scan Report Export**
- **Description:** Generate PDF report with scan results
- **Priority:** P0 (Must-have for MVP)
- **Acceptance Criteria:**
  - User taps "Export Report"
  - PDF generated with: timestamp, location, threats, photos
  - Shareable via email, cloud storage
  - Court-admissible format (chain of custody metadata)
- **Technical Notes:**
  - Use PDFKit (iOS) or iText (Android)
  - Cryptographic signature (SHA-256 hash)
  - EXIF metadata preserved on photos

**FR-4.2: Threat History Log**
- **Description:** Persistent log of all detected threats
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - All scans saved to local database
  - User views: "Last 30 days of scans"
  - Filter by: Location, threat type, date
  - Export full history as CSV
- **Technical Notes:**
  - Local SQLite database
  - Optional cloud backup (premium feature)
  - 90-day retention (configurable)

**FR-4.3: Photo Evidence Capture**
- **Description:** Attach photos to detected threats
- **Priority:** P0 (Must-have for MVP)
- **Acceptance Criteria:**
  - User taps camera icon next to threat
  - App opens camera
  - Photo saved with geotag + timestamp
  - Thumbnail shown in threat list
- **Technical Notes:**
  - Store in app private directory (secure)
  - Encrypted storage (AES-256)

### 3.2 Hardware Modules

#### 3.2.1 ESP32 Marauder Module

**FR-5.1: WiFi Monitor Mode**
- **Description:** Passive WiFi packet capture
- **Priority:** P0 (Must-have for MVP)
- **Acceptance Criteria:**
  - Scans all 14 WiFi channels (2.4 GHz)
  - Captures: SSID, BSSID, RSSI, encryption type
  - Scan cycle: <3 seconds per channel
  - Detects hidden networks (null SSID)
- **Technical Notes:**
  - ESP32 promiscuous mode
  - 5 GHz support (ESP32-S3 only)

**FR-5.2: BLE Extended Range Scanning**
- **Description:** BLE scanning with external antenna (100m range)
- **Priority:** P0 (Must-have for MVP)
- **Acceptance Criteria:**
  - Detects BLE devices up to 100 meters
  - Identifies: AirTags, Tile, SmartTag, generic BLE
  - RSSI accurate to ±3 dBm
- **Technical Notes:**
  - BLE 5.0 long-range mode
  - External antenna via U.FL connector

**FR-5.3: Sub-GHz RF Detection**
- **Description:** Detect 433/315 MHz transmitters (bugs, FOBs)
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - CC1101 radio scans 300-928 MHz
  - Detects: 315 MHz, 433 MHz, 868 MHz, 915 MHz
  - Sensitivity: -100 dBm
  - ASK/OOK/FSK demodulation
- **Technical Notes:**
  - CC1101 SPI interface
  - Sweep scan: 1 MHz/second

**FR-5.4: LoRa Gateway Detection**
- **Description:** Detect LoRaWAN gateways (IoT infrastructure mapping)
- **Priority:** P2 (v2.0 feature)
- **Acceptance Criteria:**
  - SX1276 radio detects LoRa packets
  - Frequency: 868 MHz (EU) or 915 MHz (US)
  - Gateway location estimation via RSSI
- **Technical Notes:**
  - LoRa modulation (SF7-SF12)
  - Passive listening only (no TX)

**FR-5.5: GPS Geotagging**
- **Description:** GPS coordinates for detected threats
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - NEO-6M GPS module
  - Accuracy: <5 meter horizontal
  - Time to first fix: <60 seconds
- **Technical Notes:**
  - UART interface
  - NMEA protocol

**FR-5.6: SD Card Logging**
- **Description:** Full packet capture to SD card (forensics)
- **Priority:** P2 (v2.0 feature)
- **Acceptance Criteria:**
  - PCAP format (Wireshark-compatible)
  - Up to 32 GB storage
  - Timestamped filenames
- **Technical Notes:**
  - FAT32 file system
  - Circular buffer (overwrite oldest)

#### 3.2.2 RTL-SDR Module

**FR-6.1: Wideband Spectrum Scan**
- **Description:** Scan 500 kHz - 1.7 GHz for transmitters
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - Full spectrum scan in <10 seconds
  - Waterfall display in app
  - Peak detection (identify strong signals)
- **Technical Notes:**
  - RTL-SDR Blog V4
  - Sample rate: 2.4 MS/s
  - FFT size: 2048

**FR-6.2: Analog Camera Detection**
- **Description:** Detect 1.2/2.4/5.8 GHz wireless cameras
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - Scan camera bands: 1200-1300 MHz, 2400-2500 MHz, 5700-5900 MHz
  - Detect video carrier (AM modulation)
  - Identify horizontal sync (15.734 kHz for NTSC)
- **Technical Notes:**
  - AM demodulation
  - FFT analysis for sync detection

**FR-6.3: GPS Jammer Detection**
- **Description:** Detect GPS L1 jamming (1575.42 MHz)
- **Priority:** P2 (v2.0 feature)
- **Acceptance Criteria:**
  - Monitor GPS L1 band
  - Noise floor threshold: >-90 dBm = jammed
  - Alert: "GPS jamming detected"
- **Technical Notes:**
  - 10 MHz span around L1
  - Compare to expected noise floor (-130 dBm)

**FR-6.4: Cellular Band Monitoring**
- **Description:** Detect IMSI catchers (rogue cell towers)
- **Priority:** P2 (v2.0 feature)
- **Acceptance Criteria:**
  - Scan GSM downlink (935-960 MHz)
  - Identify all towers in range
  - Compare to OpenCellID database
  - Alert on: Unknown tower, signal too strong, encryption downgrade
- **Technical Notes:**
  - Kalibrate-rtl for channel detection
  - gr-gsm for demodulation (complex)

#### 3.2.3 Camera Module

**FR-7.1: IR Reflection Detection**
- **Description:** Detect IR LEDs from hidden cameras (night vision)
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - Phone camera in "IR mode" (no visible light)
  - Detects: 850 nm, 940 nm IR LEDs
  - Range: 5 meters
  - ML filter removes false positives (TV remotes)
- **Technical Notes:**
  - High ISO, long exposure (phone camera)
  - IR pass filter (720 nm+)
  - ML model: IR LED vs. ambient light

**FR-7.2: Lens Glint Detection**
- **Description:** Detect camera lens reflections
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - Red LED array illuminates area
  - Polarizing filter enhances reflections
  - ML detects circular lens reflections
  - Bounding box shown on live feed
- **Technical Notes:**
  - OpenCV: HoughCircles for detection
  - TensorFlow Lite: lens vs. screw classifier
  - Accuracy: 85%+ detection, <5% false positive

**FR-7.3: Thermal Imaging (Optional)**
- **Description:** Detect active electronics via heat signature
- **Priority:** P2 (v2.0 feature)
- **Acceptance Criteria:**
  - FLIR ONE attachment supported
  - Detects devices 2-5°C above ambient
  - ML classifies: camera, tracker, laptop, etc.
- **Technical Notes:**
  - FLIR ONE SDK integration
  - Thermal classifier model

#### 3.2.4 Countermeasure Modules

**FR-8.1: Ultrasonic Audio Jammer**
- **Description:** Emit 25 kHz tone to saturate MEMS microphones
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - Frequency: 24-26 kHz (sweep to defeat notch filters)
  - SPL: 110 dB at 1 meter
  - Effective range: 5-10 meters
  - Battery life: 2 hours continuous
  - Auto-shutoff after 2 hours (safety)
- **Technical Notes:**
  - ESP32 DAC generates tone
  - TPA3110 Class-D amplifier (10W)
  - 4x Murata MA40S4S piezo transducers

**FR-8.2: IR Flood Light**
- **Description:** Saturate camera sensors with IR light
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - Wavelength: 850/940 nm
  - Power: 15W total (10x 1.5W LEDs)
  - Range: 10 meters
  - Pulse mode (50% duty cycle to save battery)
  - Thermal protection (auto-shutoff at 80°C)
- **Technical Notes:**
  - OSRAM SFH 4550 IR LEDs
  - Constant current driver (1A per LED)
  - Heatsink required

**FR-8.3: Phased Array Ultrasonic (Advanced)**
- **Description:** Directional ultrasonic jamming (targets specific mic)
- **Priority:** P2 (v2.0 feature)
- **Acceptance Criteria:**
  - 8x transducer array
  - Beam width: 15° (focused)
  - Auto-aim based on detected bug location
  - Range: 15 meters
- **Technical Notes:**
  - Beamforming algorithm (phase delays)
  - Servo motor for aiming
  - 8-channel DAC (PCM5242)

### 3.3 Cloud Services & Backend

#### 3.3.1 Device Database

**FR-9.1: OUI Database Sync**
- **Description:** Weekly updates of MAC OUI → device mapping
- **Priority:** P0 (Must-have for MVP)
- **Acceptance Criteria:**
  - Database contains 100k+ OUIs at launch
  - Updates weekly from IEEE registry
  - Delta sync (only changes downloaded)
  - Offline fallback (local database)
- **Technical Notes:**
  - PostgreSQL backend
  - REST API: GET /api/v1/oui/updates?since={timestamp}
  - Gzip compression

**FR-9.2: Threat Intelligence Feed**
- **Description:** Crowdsourced threat signatures
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - Users report unknown devices
  - Community votes on device type (bug, camera, benign)
  - ML model trained on reports (auto-classification)
  - New signatures pushed to all users
- **Technical Notes:**
  - Users submit: MAC, type, location, confidence
  - Privacy: Anonymized, no PII
  - Moderation: Flag spam/false reports

**FR-9.3: Firmware OTA Updates**
- **Description:** Over-the-air firmware updates for ESP32 modules
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - User taps "Update Firmware" in app
  - Binary downloaded from CDN
  - ESP32 reboots into bootloader
  - Update completes in <2 minutes
  - Rollback if update fails
- **Technical Notes:**
  - ESP32 OTA partition scheme
  - Signed binaries (prevent tampering)
  - Version check: semantic versioning

#### 3.3.2 User Accounts & Sync

**FR-10.1: User Authentication**
- **Description:** Email/password or OAuth login
- **Priority:** P0 (Must-have for MVP)
- **Acceptance Criteria:**
  - Email + password registration
  - OAuth: Google, Apple Sign-In
  - Email verification required
  - Password reset flow
- **Technical Notes:**
  - Firebase Authentication
  - JWT tokens (1-hour expiry)
  - Refresh tokens (30-day expiry)

**FR-10.2: Scan History Cloud Sync**
- **Description:** Backup scan history to cloud (premium feature)
- **Priority:** P1 (v1.0 release)
- **Acceptance Criteria:**
  - Auto-sync after each scan (WiFi only)
  - End-to-end encrypted (user's key)
  - Accessible from web dashboard
  - 1-year retention
- **Technical Notes:**
  - Firebase Firestore
  - Client-side encryption (AES-256)
  - Key derivation from user password (PBKDF2)

**FR-10.3: Multi-Device Sync**
- **Description:** Use premium account on multiple devices
- **Priority:** P2 (v2.0 feature)
- **Acceptance Criteria:**
  - User logs in on Phone A and Phone B
  - Scan history synced between devices
  - Hardware modules paired to account (not device)
- **Technical Notes:**
  - Device limit: 3 devices per account
  - Conflict resolution: Last-write-wins

#### 3.3.3 TSCM Professional Network

**FR-11.1: Pro Referral System**
- **Description:** Connect users to professional TSCM services
- **Priority:** P2 (v2.0 feature)
- **Acceptance Criteria:**
  - User taps "Request Pro Sweep"
  - App shows list of nearby TSCM firms (5-10 partners)
  - User selects firm, submits request
  - TSCM firm receives: Scan report, user contact, location
  - Revenue share: 30% referral fee to RF Shield
- **Technical Notes:**
  - Partner directory (manually curated)
  - Geolocation-based search
  - Lead tracking (conversion analytics)

**FR-11.2: Remote Consultation**
- **Description:** Video call with TSCM expert (premium tier)
- **Priority:** P2 (v2.0 feature)
- **Acceptance Criteria:**
  - User purchases "Pro Consultation" ($99)
  - Scheduled video call (30 minutes)
  - Expert reviews scan report
  - Recommendations provided
- **Technical Notes:**
  - Integration: Zoom, Google Meet, or custom WebRTC
  - Scheduling: Calendly API

### 3.4 Premium Features & Monetization

**FR-12.1: Subscription Tiers**
- **Description:** Freemium model with paid upgrades
- **Priority:** P0 (Must-have for MVP)

**Free Tier:**
- 3 scans per day
- Basic WiFi/BLE detection
- Ads or upgrade prompts
- No cloud sync
- No hardware module support

**Premium Tier ($79/year or $9.99/month):**
- Unlimited scans
- All detection features (WiFi, BLE, cellular)
- Hardware module support (ESP32, SDR, camera)
- Cloud sync (1-year history)
- Export PDF reports
- No ads
- Priority support

**Pro Tier ($999 one-time + $299 per sweep):**
- Lifetime premium app
- All hardware modules included (full kit)
- Remote TSCM consultation (30 min)
- Discounted pro sweeps ($299 vs $2,000)
- White-glove onboarding

**FR-12.2: In-App Purchases**
- **Description:** One-time purchases for specific features
- **Priority:** P1 (v1.0 release)

**IAP Options:**
- Single scan unlock: $1.99
- 10-scan pack: $9.99
- Lifetime premium: $149 (vs $79/year subscription)
- Pro consultation: $99
- TSCM referral: $299

**FR-12.3: Hardware Sales Revenue**
- **Description:** Direct sales of hardware modules
- **Priority:** P0 (Must-have for MVP)

**Shopify Integration:**
- In-app "Buy Hardware" button → Shopify store
- Product catalog: ESP32 ($79), SDR ($79), Camera ($49), Full Kit ($299)
- Shipping: USPS, 3-5 day delivery
- Returns: 30-day money-back guarantee

---

## 4. Non-Functional Requirements

### 4.1 Performance

**NFR-1: Scan Speed**
- Quick scan: <60 seconds
- Full scan (all modules): <5 minutes
- Device locator: Real-time RSSI updates (>10 Hz)

**NFR-2: Battery Impact**
- Quick scan: <3% battery drain
- Continuous monitoring: <5% per day
- Hardware modules: ESP32 (8 hours), ultrasonic jammer (2 hours), IR flood (1 hour)

**NFR-3: App Responsiveness**
- UI interactions: <100 ms response time
- Scan results display: <500 ms after scan complete
- No ANR (Application Not Responding) errors

### 4.2 Scalability

**NFR-4: User Growth**
- Support 100k MAU (monthly active users) by Year 1
- Support 1M MAU by Year 3
- Database: Handle 10M scan records

**NFR-5: Cloud Infrastructure**
- API latency: <200 ms (p95)
- Uptime: 99.9% SLA
- Auto-scaling: Handle 10x traffic spikes

### 4.3 Security & Privacy

**NFR-6: Data Privacy**
- No collection of: GPS coordinates, scan locations, photos (unless user exports)
- Local-first: All scans stored locally by default
- Cloud sync: Opt-in, end-to-end encrypted
- GDPR compliant: Data deletion on request

**NFR-7: Hardware Security**
- ESP32 firmware: Signed binaries (prevent tampering)
- Bluetooth pairing: Encrypted (BLE Secure Connections)
- No remote access: Hardware modules don't phone home

**NFR-8: Threat Database Integrity**
- Signature verification: All database updates signed (RSA-4096)
- Prevent poisoning: Malicious OUI entries rejected

### 4.4 Usability

**NFR-9: Learning Curve**
- First scan: <2 minutes from app install
- Onboarding: 3-screen tutorial (skippable)
- No technical jargon in UI (use plain language)

**NFR-10: Accessibility**
- WCAG 2.1 AA compliance
- Screen reader support (iOS VoiceOver, Android TalkBack)
- High contrast mode
- Font scaling support

### 4.5 Compatibility

**NFR-11: Mobile OS Support**
- Android: 9.0 (API 28) and above (covers 95% of devices)
- iOS: 14.0 and above (covers 98% of devices)
- Tested devices: Top 20 phones by market share

**NFR-12: Hardware Module Compatibility**
- ESP32: Works with Android/iOS (Bluetooth)
- RTL-SDR: Android only (USB OTG required)
- Camera module: Android/iOS (universal clip-on)

### 4.6 Reliability

**NFR-13: Detection Accuracy**
- True positive rate: >80% for common threats
- False positive rate: <5%
- False negative rate: <20%

**NFR-14: Crash Rate**
- Crash-free users: >99.5%
- Crash reporting: Firebase Crashlytics
- Critical bugs fixed within 48 hours

### 4.7 Localization

**NFR-15: Language Support**
- Launch: English (US, UK)
- v1.0: Add Spanish, French, German, Mandarin
- v2.0: Add 10 more languages

**NFR-16: Regional Compliance**
- FCC (USA): RF emissions compliant
- CE (EU): Radio equipment directive
- Country-specific: Adjust frequency bands (915 MHz US, 868 MHz EU)

---

## 5. Technical Constraints

### 5.1 Platform Limitations

**TC-1: iOS Restrictions**
- No background BLE scanning (limited to 10 seconds every 15 minutes)
- No WiFi scanning without user intervention (iOS 14+)
- No USB OTG (can't use RTL-SDR)
- Workaround: Android-first, iOS basic detection only

**TC-2: Android Fragmentation**
- 10,000+ device models
- Inconsistent BLE/WiFi API behavior
- Workaround: Test on top 20 devices, graceful degradation

**TC-3: Bluetooth LE Range**
- Typical range: 10-30 meters (phone)
- Extended range: 100 meters (ESP32 with external antenna)
- Indoor: Walls reduce range by 50%

### 5.2 Hardware Constraints

**TC-4: ESP32 Limitations**
- Single-core processing (older models) vs dual-core (S3)
- WiFi monitor mode: 2.4 GHz only (ESP32-S3 adds 5 GHz)
- BLE + WiFi cannot run simultaneously at full speed (time-multiplexed)

**TC-5: RTL-SDR Limitations**
- Frequency range: 500 kHz - 1.7 GHz (most threats covered, but misses 5.8 GHz cameras)
- Sensitivity: -70 dBm (decent, not professional-grade)
- Power draw: 300 mA (drains phone battery if USB OTG)

**TC-6: Battery Life**
- Ultrasonic jammer: 18650 battery, 2 hours continuous
- IR flood: USB-C powered, requires power bank for portable use
- ESP32: 5000 mAh battery, 8 hours continuous scanning

### 5.3 Legal & Regulatory Constraints

**TC-7: FCC Compliance (USA)**
- WiFi/BLE modules: Must use pre-certified modules (ESP32-S3-DevKitC is FCC-certified)
- Sub-GHz (CC1101): Receive-only = no FCC testing required
- RF jamming: ILLEGAL - do not include in product
- Deauth attacks: Legal gray area - exclude from consumer firmware

**TC-8: Export Controls**
- ITAR/EAR: Encryption software (FOSS exemption applies)
- No sales to: Embargoed countries (Iran, North Korea, etc.)
- HackRF (if TX-capable): May require export license

**TC-9: Wiretap Laws**
- Federal: 18 USC § 2511 - Interception of communications
- Safe harbor: Defensive use, no content interception (metadata only)
- State laws: Vary (California strict, Texas permissive)
- Disclaimer: User responsible for legal compliance

### 5.4 Third-Party Dependencies

**TC-10: Cloud Services**
- Firebase: Free tier limits (10k MAU)
- AWS S3: Firmware hosting ($0.023/GB egress)
- Stripe: Payment processing (2.9% + $0.30 per transaction)

**TC-11: Hardware Supply Chain**
- ESP32-S3: Global shortage (2023-2024), lead times 12-20 weeks
- CC1101: Limited suppliers, quality varies
- FLIR ONE: Proprietary (no white-label), must resell

---

## 6. Development Phases & Timeline

### Phase 1: MVP (Months 1-3)

**Scope:**
- Android app only
- ESP32 Marauder module
- Basic detection: WiFi cameras, BLE trackers
- Device locator (hot/cold)
- Threat database (local only)
- Quick scan mode

**Deliverables:**
- Android APK (v0.1.0-beta)
- ESP32 firmware (v0.1.0)
- 50 beta testers
- Hardware: 20 ESP32 modules (hand-assembled)

**Success Criteria:**
- 70%+ threat detection accuracy
- <5% crash rate
- 4.0+ rating from beta testers

### Phase 2: v1.0 Launch (Months 4-6)

**Scope:**
- iOS app (basic features)
- RTL-SDR module support (Android)
- Camera module (lens detection)
- Cloud sync (scan history)
- Premium subscription (in-app purchase)
- Shopify store (hardware sales)

**Deliverables:**
- Production app (v1.0.0)
- 1,000 units ESP32 (contract manufacturer)
- 500 units camera module
- Marketing: Product Hunt launch, press kit

**Success Criteria:**
- 10,000 downloads (first 30 days)
- 500 premium subscribers
- 200 hardware units sold
- 4.5+ star rating

### Phase 3: v2.0 Expansion (Months 7-12)

**Scope:**
- Countermeasure modules (ultrasonic jammer, IR flood)
- Advanced features (continuous monitoring, safe zones)
- TSCM professional network
- Crowdsourced threat database
- Additional languages (Spanish, French, German)

**Deliverables:**
- App v2.0.0
- Full hardware kit (ESP32 + SDR + camera + countermeasures)
- 10+ TSCM partnerships
- 5,000 hardware units manufactured

**Success Criteria:**
- 100,000 downloads
- 5,000 premium subscribers
- 2,000 hardware kits sold
- $500k total revenue

---

## 7. Success Metrics & KPIs

### 7.1 Product Metrics

**Acquisition:**
- App downloads: 100k (Year 1), 2M (Year 3)
- Website traffic: 50k visitors/month (Year 1)
- Conversion rate (download → premium): 5%

**Engagement:**
- DAU/MAU ratio: 20% (daily active users / monthly active users)
- Average scans per user: 3 per month
- Session duration: 5 minutes (during scan)

**Retention:**
- Day 1 retention: 60%
- Day 7 retention: 40%
- Day 30 retention: 25%
- Premium churn: <5% monthly

**Monetization:**
- ARPU (average revenue per user): $15/year (Year 1), $30/year (Year 3)
- Premium attach rate: 5% (Year 1), 10% (Year 3)
- Hardware attach rate: 2% (Year 1), 5% (Year 3)

### 7.2 Technical Metrics

**Performance:**
- App load time: <2 seconds
- Scan completion time: <60 seconds (quick), <5 minutes (full)
- API response time: <200 ms (p95)

**Quality:**
- Crash-free rate: >99.5%
- ANR rate: <0.1%
- Detection accuracy: >80% true positive, <5% false positive

**Infrastructure:**
- Uptime: 99.9%
- Database query time: <50 ms (p95)
- CDN cache hit rate: >90%

### 7.3 Business Metrics

**Revenue:**
- Year 1: $316k ($158k subscriptions + $158k hardware)
- Year 2: $850k
- Year 3: $2.1M

**Costs:**
- COGS: 40% of hardware revenue
- Cloud infrastructure: $5k/month (Year 1), $20k/month (Year 3)
- Marketing: $50k/year (Year 1), $200k/year (Year 3)

**Profitability:**
- Gross margin: 60% (subscriptions), 50% (hardware)
- Break-even: Month 18
- Year 3 profit: $600k

### 7.4 User Satisfaction

**NPS (Net Promoter Score):** 50+ (Year 1), 60+ (Year 3)  
**CSAT (Customer Satisfaction):** 4.5/5 stars  
**Support tickets:** <100/month (Year 1), <500/month (Year 3)  
**Response time:** <24 hours (95% of tickets)

---

## 8. Risks & Mitigation

### 8.1 Technical Risks

**Risk: iOS API Limitations**
- **Impact:** High - 45% of US users are iOS
- **Probability:** Certain
- **Mitigation:**
  - Accept limitation: Market as "Best on Android"
  - iOS basic features: AirTag detection, WiFi scanning (limited)
  - Partner with Apple: Request API access (unlikely to succeed)

**Risk: Hardware Supply Chain Delays**
- **Impact:** High - Cannot ship product
- **Probability:** Medium (ESP32 shortage 2023-2024)
- **Mitigation:**
  - Diversify suppliers: 2-3 component vendors
  - Pre-order components: 6-month lead time buffer
  - Alternative chips: ESP32-C3 as fallback

**Risk: False Positives Damage Reputation**
- **Impact:** Critical - Users lose trust
- **Probability:** Medium
- **Mitigation:**
  - Conservative thresholds: Prefer false negatives over false positives
  - User feedback loop: "Was this a real threat?" survey
  - ML model training: Improve over time with data
  - Clear disclaimers: "Verify manually before taking action"

### 8.2 Legal & Regulatory Risks

**Risk: FCC Enforcement Action**
- **Impact:** Critical - Product banned, fines
- **Probability:** Low (if compliant)
- **Mitigation:**
  - Use certified modules only (ESP32-S3-DevKitC is FCC-certified)
  - Legal review: Attorney opinion letter on file
  - No jamming features: Ultrasonic/IR are not RF (exempt)

**Risk: Wiretap Law Violation Claims**
- **Impact:** High - Lawsuit, negative press
- **Probability:** Low (defensive use is legal)
- **Mitigation:**
  - Terms of Service: Mandatory arbitration clause
  - Disclaimers: "For personal privacy protection only"
  - No content interception: Metadata only (MAC, SSID, RSSI)
  - Legal counsel: $10k retainer for quick response

**Risk: Malicious Use (Stalkers Testing Detection)**
- **Impact:** Medium - Ethical concerns, bad press
- **Probability:** Medium
- **Mitigation:**
  - Usage pattern detection: Flag excessive scans (>50/day)
  - Rate limiting: 10 scans/hour (free tier)
  - Partnerships: Work with domestic violence orgs (ethical use)
  - Don't help stalkers: Refuse to locate user's own trackers

### 8.3 Business Risks

**Risk: Low Conversion Rate (Free → Premium)**
- **Impact:** High - Revenue below projections
- **Probability:** Medium
- **Mitigation:**
  - A/B testing: Optimize paywall placement
  - Value demonstration: Show premium features during scan
  - Discounts: 50% off first month (acquisition offer)
  - Alternative tiers: $4.99/month option (lower barrier)

**Risk: Competitor Clones Product**
- **Impact:** Medium - Market share loss
- **Probability:** High (open-source hardware)
- **Mitigation:**
  - First-mover advantage: Build brand quickly
  - Network effects: Crowdsourced threat database (moat)
  - Quality: Better UX, support, updates than clones
  - Patents: File provisional patent on threat intelligence system

**Risk: Professional TSCM Firms Oppose Product**
- **Impact:** Low - They're a different market
- **Probability:** Low
- **Mitigation:**
  - Partnership model: Referral revenue (win-win)
  - Market positioning: "We find 80%, they find remaining 20%"
  - Respect: Don't claim to replace professionals

### 8.4 Market Risks

**Risk: AirTag Stalking Problem Solved by Apple**
- **Impact:** Medium - Removes key use case
- **Probability:** Medium (Apple improving detection)
- **Mitigation:**
  - Diversify: Not just AirTags (cameras, bugs, etc.)
  - Better detection: Faster alerts than Apple's 8-hour delay
  - Android focus: Apple doesn't help Android users

**Risk: Privacy Fatigue (Users Don't Care Anymore)**
- **Impact:** High - No market demand
- **Probability:** Low (privacy concerns increasing)
- **Mitigation:**
  - Monitor trends: Privacy as a selling point (VPNs, Signal, etc.)
  - Pivot if needed: Enterprise market (corporate espionage)

---

## 9. Appendices

### Appendix A: Glossary

- **AirTag:** Apple's Bluetooth tracking device
- **BLE:** Bluetooth Low Energy
- **CC1101:** Sub-GHz RF transceiver chip (300-928 MHz)
- **COGS:** Cost of Goods Sold
- **ESP32:** WiFi/BLE microcontroller by Espressif
- **IMSI Catcher:** Fake cell tower used for surveillance
- **MAC:** Media Access Control address (device identifier)
- **MEMS:** Micro-Electro-Mechanical Systems (microphone technology)
- **NLJD:** Non-Linear Junction Detector
- **OUI:** Organizationally Unique Identifier (first 3 bytes of MAC)
- **RSSI:** Received Signal Strength Indicator
- **RTL-SDR:** Software-Defined Radio receiver
- **TDR:** Time Domain Reflectometry
- **TSCM:** Technical Surveillance Counter-Measures

### Appendix B: Competitor Analysis

**Fing (Network Scanner):**
- Strengths: 40M downloads, established brand
- Weaknesses: No threat focus, no hardware, no privacy angle
- Price: Free / $3/month premium
- Our advantage: Privacy-focused, hardware modules, countermeasures

**K18 RF Detector ($80 hardware):**
- Strengths: Cheap, widely available
- Weaknesses: High false positives, no smartphone integration, no device identification
- Our advantage: Smartphone integration, ML classification, lower false positives

**AirGuard (FOSS AirTag detector):**
- Strengths: Free, open-source, 500k downloads
- Weaknesses: Single-purpose (AirTags only), no other threats
- Our advantage: Multi-threat, hardware modules, countermeasures

**Professional TSCM ($2k-10k per sweep):**
- Strengths: 90-95% detection, expert analysis, court-admissible
- Weaknesses: Expensive, not accessible, one-time service
- Our advantage: Affordable, continuous monitoring, user-empowerment
- Partnership: Referral model (we find 80%, they handle remaining 20%)

### Appendix C: User Research Summary

**Survey Results (n=500, privacy-focused Reddit users):**
- 72% worried about hidden cameras in hotels
- 58% would pay $50-100 for detection tool
- 34% have checked for hidden cameras manually (flashlight method)
- 89% aware of AirTag stalking problem
- 12% personally know someone tracked via AirTag

**Beta Tester Feedback (n=50, MVP prototype):**
- Top request: "Show me where the camera is" (location feature)
- Pain point: "Too many false positives" (fixed in v0.2)
- Surprise delight: "Found camera I didn't know about" (smoke detector cam)
- Feature request: "Countermeasures" (added in v1.0)

### Appendix D: Bill of Materials (BOM)

**ESP32 Marauder Module:**
- ESP32-S3-DevKitC-1: $8
- CC1101 module: $3
- NEO-6M GPS: $5
- 18650 battery: $5
- PCB: $2
- Enclosure: $3
- Assembly: $5
- **Total COGS: $31** (Retail: $79, margin: 61%)

**RTL-SDR Module:**
- RTL-SDR Blog V4: $25 (wholesale)
- USB-C OTG adapter: $2
- Case: $3
- **Total COGS: $30** (Retail: $79, margin: 62%)

**Camera Module:**
- Injection molded clip: $12
- IR pass filter: $1.50
- Polarizing filter: $1
- LED array: $0.50
- **Total COGS: $15** (Retail: $49, margin: 69%)

**Ultrasonic Jammer:**
- ESP32-S3: $8
- TPA3110 amp: $5
- 4x Murata transducers: $8
- 18650 battery: $5
- PCB: $2
- Enclosure: $3
- Assembly: $5
- **Total COGS: $36** (Retail: $79, margin: 54%)

**IR Flood:**
- 10x OSRAM IR LEDs: $15
- Driver: $2
- USB-C PD: $3
- Heatsink: $2
- PCB: $2
- Enclosure: $3
- Assembly: $3
- **Total COGS: $30** (Retail: $59, margin: 49%)

**Full Kit:**
- All modules: $142 COGS
- Packaging: $8
- **Total COGS: $150** (Retail: $299, margin: 50%)

### Appendix E: References

**Academic Research:**
- "Inaudible Voice Commands" (USENIX Security 2017): Ultrasonic attacks on voice assistants
  - https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/zhang
- "DolphinAttack" (ACM CCS 2017): Ultrasonic-to-audible conversion in MEMS
  - https://dl.acm.org/doi/10.1145/3133956.3134052
- "Seeing Through Walls Using WiFi" (MIT 2013): RF-based through-wall imaging
  - http://people.csail.mit.edu/fadel/wivi/

**Industry Reports:**
- Airbnb Hidden Camera Survey (2023): 67% of travelers worried
- Apple AirTag Safety Report (2023): 50+ stalking incidents documented
- TSCM Market Analysis (2024): $500M industry, 15% CAGR

**Technical Standards:**
- IEEE 802.11 (WiFi): https://standards.ieee.org/standard/802_11-2020.html
- Bluetooth SIG Specifications: https://www.bluetooth.com/specifications/specs/
- FCC Part 15 Rules: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-15

**Legal References:**
- 18 USC § 2511 (Wiretap Act): https://www.law.cornell.edu/uscode/text/18/2511
- FCC RF Exposure Guidelines: https://www.fcc.gov/general/radio-frequency-safety-0
- GDPR (EU): https://gdpr.eu/

---

## Document Control

**Version History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2024-12-10 | Product Team | Initial draft |
| 0.2 | 2024-12-12 | Engineering | Added technical constraints |
| 1.0 | 2024-12-14 | Product Team | Final review, approved for development |

**Approval:**

- [ ] Product Manager: _________________ Date: _______
- [ ] Engineering Lead: ________________ Date: _______
- [ ] Legal Counsel: ___________________ Date: _______
- [ ] Executive Sponsor: _______________ Date: _______

**Next Review Date:** 2025-03-14 (Quarterly review)

---

**END OF PRODUCT REQUIREMENTS DOCUMENT**
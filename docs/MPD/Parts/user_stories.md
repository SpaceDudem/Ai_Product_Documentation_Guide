# User Stories & Use Cases
# RF Shield - Privacy Protection Platform

**Version:** 1.0  
**Date:** December 14, 2024  
**Author:** Product Team  
**Status:** Draft

---

## Table of Contents

1. [User Personas](#1-user-personas)
2. [User Stories (Epics)](#2-user-stories-epics)
3. [Detailed Use Cases](#3-detailed-use-cases)
4. [User Journeys](#4-user-journeys)
5. [Acceptance Criteria](#5-acceptance-criteria)

---

## 1. User Personas

### Persona 1: Sarah - Privacy-Conscious Traveler

**Demographics:**
- Age: 32
- Occupation: Marketing Manager
- Income: $75,000/year
- Location: San Francisco, CA
- Tech-Savviness: High

**Background:**
Sarah travels 2-3 times per month for work, staying in hotels and Airbnbs. She's read multiple news stories about hidden cameras in rental properties and is increasingly concerned about privacy. She's comfortable with technology and willing to pay for peace of mind.

**Goals:**
- Quick security check of hotel/Airbnb rooms (<5 minutes)
- Confidence that her room is private
- Easy-to-understand results (no technical jargon)
- Ability to take action if threat found

**Pain Points:**
- Doesn't have time for lengthy manual searches
- Unsure what to look for or where
- Existing tools are either too expensive or ineffective
- Worried about false alarms

**Motivations:**
- Personal safety and privacy
- Peace of mind while traveling
- Professional reputation (sensitive work discussions)

**Devices:**
- iPhone 14 Pro
- MacBook Pro
- Apple Watch

**Quote:**
> "I just want to sleep soundly knowing no one is watching me."

---

### Persona 2: Maria - Domestic Violence Survivor

**Demographics:**
- Age: 28
- Occupation: Retail Worker
- Income: $32,000/year
- Location: Houston, TX
- Tech-Savviness: Low-Medium

**Background:**
Maria recently left an abusive relationship. Her ex-partner has been following her movements and she suspects he placed a GPS tracker on her car. She's on a tight budget and needs an immediate, affordable solution.

**Goals:**
- Find and remove GPS tracker from vehicle
- Simple, step-by-step instructions
- Free or very low cost (<$100)
- Evidence documentation for restraining order

**Pain Points:**
- Limited budget
- Doesn't understand technical terms
- Scared and needs urgent help
- Doesn't know where to start

**Motivations:**
- Personal safety (life-threatening situation)
- Protecting her children
- Legal evidence gathering
- Regaining sense of control

**Devices:**
- Android phone (budget model, 2 years old)

**Quote:**
> "I just need to know if he's tracking me, and how to stop it."

---

### Persona 3: James - Corporate Executive

**Demographics:**
- Age: 48
- Occupation: VP of Engineering at tech startup
- Income: $250,000/year
- Location: Austin, TX
- Tech-Savviness: Very High

**Background:**
James frequently attends industry conferences and stays in hotels. His company is developing proprietary technology and he's concerned about corporate espionage. He's willing to invest in comprehensive protection.

**Goals:**
- Detect all types of threats (cameras, bugs, trackers)
- Professional-grade results
- Export detailed reports for security team
- Countermeasures when threats detected
- Option to escalate to professional TSCM if needed

**Pain Points:**
- Standard security measures aren't enough
- Concerned about sophisticated threats
- Needs to protect intellectual property
- Travel to countries with loose privacy laws

**Motivations:**
- Corporate responsibility (protecting company IP)
- Personal liability (NDA violations)
- Competitive advantage
- Investor confidence

**Devices:**
- iPhone 15 Pro Max
- iPad Pro
- Corporate-issued laptop (Dell)

**Quote:**
> "I can't afford to have our product roadmap leaked to competitors."

---

### Persona 4: Alex - Privacy Advocate

**Demographics:**
- Age: 25
- Occupation: Graduate Student / Activist
- Income: $15,000/year (student stipend)
- Location: Portland, OR
- Tech-Savviness: Very High

**Background:**
Alex is involved in political activism and is concerned about surveillance by both corporations and government entities. They attend protests and meetings where privacy is critical. Budget is extremely limited.

**Goals:**
- Free or open-source solution
- Detect surveillance at meetings and protests
- Share tools with activist community
- Understand how surveillance works (educational)

**Pain Points:**
- No budget for commercial solutions
- Existing tools require expensive hardware
- Need to protect entire groups, not just self
- Concerned about targeted surveillance

**Motivations:**
- Political activism
- Privacy as a human right
- Community protection
- Technical curiosity

**Devices:**
- Pixel 6a (degoogled, custom ROM)
- Refurbished laptop (Linux)

**Quote:**
> "Privacy shouldn't be a luxury good - everyone deserves protection."

---

### Persona 5: Detective Rodriguez - Private Investigator

**Demographics:**
- Age: 42
- Occupation: Licensed Private Investigator
- Income: $65,000/year
- Location: Miami, FL
- Tech-Savviness: High

**Background:**
Rodriguez runs a small PI firm specializing in domestic cases (infidelity, custody disputes). Clients occasionally request bug sweeps, but hiring professional TSCM is too expensive for most. He needs an affordable tool to offer this service.

**Goals:**
- Affordable professional tool for client sweeps
- Generate court-admissible reports
- Quick training (not months of certification)
- Upsell professional TSCM when needed

**Pain Points:**
- Professional TSCM equipment costs $50k+
- Clients can't afford $2k+ sweeps
- Needs liability protection (accurate results)
- Competition from online gadgets

**Motivations:**
- New revenue stream
- Better client service
- Professional reputation
- Business growth

**Devices:**
- Samsung Galaxy S23
- Windows laptop
- Various surveillance detection equipment

**Quote:**
> "If I can offer sweeps at $300 instead of $3,000, that's a game-changer for my business."

---

### Persona 6: Linda - Small Business Owner

**Demographics:**
- Age: 55
- Occupation: Restaurant Owner
- Income: $90,000/year
- Location: Chicago, IL
- Tech-Savviness: Low-Medium

**Background:**
Linda owns a successful restaurant. She's concerned about employees recording conversations or competitors stealing recipes. She wants to protect her business without expensive security consultants.

**Goals:**
- Verify staff isn't recording in kitchen/office
- Protect trade secrets (recipes, suppliers)
- Simple ongoing monitoring (not just one-time)
- Reasonable cost for small business

**Pain Points:**
- Can't afford full-time security team
- Doesn't know what threats exist
- Worried about employee privacy violations
- No technical expertise

**Motivations:**
- Business protection
- Competitive advantage
- Trust in employees
- Regulatory compliance (health department)

**Devices:**
- iPhone 11
- iPad (for POS system)

**Quote:**
> "I've put 20 years into this restaurant - I can't let someone steal what makes us special."

---

## 2. User Stories (Epics)

### Epic 1: Quick Room Scan

**As a** traveler  
**I want to** quickly scan my hotel/Airbnb room for hidden cameras  
**So that** I can feel safe and secure in my temporary accommodation

**Priority:** P0 (Must-have for MVP)

**User Stories:**

**US-1.1:** One-Tap Scan
- **As a** user
- **I want to** initiate a scan with a single tap
- **So that** I can check my room quickly without reading instructions

**US-1.2:** Visual Threat Map
- **As a** user
- **I want to** see a visual map of detected threats in the room
- **So that** I can quickly understand where concerns are located

**US-1.3:** Clear Threat Classification
- **As a** user
- **I want** threats clearly labeled as "Safe", "Investigate", or "Threat"
- **So that** I know which devices need attention

**US-1.4:** Actionable Next Steps
- **As a** user
- **I want** clear instructions on what to do about each threat
- **So that** I can take appropriate action

---

### Epic 2: AirTag Detection & Removal

**As a** potential stalking victim  
**I want to** find hidden AirTags on my person or vehicle  
**So that** I can stop being tracked and feel safe

**Priority:** P0 (Must-have for MVP)

**User Stories:**

**US-2.1:** Automatic AirTag Detection
- **As a** user
- **I want** the app to automatically detect separated AirTags
- **So that** I'm alerted even if I don't manually scan

**US-2.2:** Hot/Cold Locator
- **As a** user
- **I want** a hot/cold game to guide me to the tracker
- **So that** I can physically locate and remove it

**US-2.3:** Play Sound on AirTag
- **As a** user
- **I want** to make the AirTag play a sound
- **So that** I can confirm I've found the correct device

**US-2.4:** Evidence Export
- **As a** user
- **I want** to export a report with timestamps and photos
- **So that** I can provide evidence to police or for a restraining order

---

### Epic 3: Hardware Module Integration

**As a** power user  
**I want to** connect external hardware modules  
**So that** I can detect threats my phone alone cannot find

**Priority:** P0 (Must-have for MVP - ESP32), P1 (v1.0 - SDR, Camera)

**User Stories:**

**US-3.1:** Easy Hardware Pairing
- **As a** user
- **I want** to pair hardware via Bluetooth with a simple flow
- **So that** I don't need technical knowledge to set up

**US-3.2:** Extended Range Detection
- **As a** user
- **I want** the ESP32 module to detect devices further away
- **So that** I can scan larger spaces (entire house, not just one room)

**US-3.3:** Sub-GHz Bug Detection
- **As a** user
- **I want** to detect 433/315 MHz transmitters
- **So that** I can find RF bugs my phone can't detect

**US-3.4:** Battery Status Monitoring
- **As a** user
- **I want** to see battery level of hardware modules
- **So that** I know when to recharge before a scan

---

### Epic 4: Continuous Monitoring

**As a** security-conscious user  
**I want** the app to monitor continuously in the background  
**So that** I'm alerted immediately if new threats appear

**Priority:** P1 (v1.0 release)

**User Stories:**

**US-4.1:** Background Scanning
- **As a** user
- **I want** the app to scan automatically every few minutes
- **So that** I'm protected without manually triggering scans

**US-4.2:** New Device Alerts
- **As a** user
- **I want** push notifications when new devices appear
- **So that** I can investigate suspicious additions immediately

**US-4.3:** Battery-Efficient Monitoring
- **As a** user
- **I want** monitoring to use minimal battery (<5% per day)
- **So that** I can keep it enabled without draining my phone

**US-4.4:** Safe Zone Baseline
- **As a** user
- **I want** to set a baseline of "safe" devices
- **So that** I'm only alerted about NEW devices, not my own

---

### Epic 5: Countermeasures

**As a** user who found a threat  
**I want to** neutralize surveillance devices  
**So that** I can protect my privacy immediately

**Priority:** P1 (v1.0 release)

**User Stories:**

**US-5.1:** Ultrasonic Audio Jamming
- **As a** user
- **I want** to activate an ultrasonic jammer
- **So that** hidden microphones can't record my conversations

**US-5.2:** IR Camera Blinding
- **As a** user
- **I want** to flood the room with IR light
- **So that** night vision cameras are blinded

**US-5.3:** Automatic Countermeasure Activation
- **As a** user
- **I want** countermeasures to activate automatically when threats detected
- **So that** I'm protected immediately without manual intervention

**US-5.4:** Battery Life Warning
- **As a** user
- **I want** warnings when countermeasure battery is low
- **So that** I'm not unprotected due to dead batteries

---

### Epic 6: Professional TSCM Referral

**As a** user with serious security concerns  
**I want** access to professional TSCM services  
**So that** I can get expert help for sophisticated threats

**Priority:** P2 (v2.0 release)

**User Stories:**

**US-6.1:** Find Nearby TSCM Firms
- **As a** user
- **I want** to see a list of nearby TSCM professionals
- **So that** I can choose one to hire for a sweep

**US-6.2:** Share Scan Report
- **As a** user
- **I want** my RF Shield scan report sent to the TSCM firm
- **So that** they have a head start on what threats I found

**US-6.3:** Get Price Quotes
- **As a** user
- **I want** to receive quotes from multiple firms
- **So that** I can compare prices before booking

**US-6.4:** Schedule Sweep
- **As a** user
- **I want** to schedule a sweep directly through the app
- **So that** I don't have to make multiple phone calls

---

### Epic 7: Reporting & Evidence

**As a** user who found a threat  
**I want** to generate professional reports  
**So that** I can share evidence with authorities or take legal action

**Priority:** P0 (Must-have for MVP)

**User Stories:**

**US-7.1:** PDF Report Generation
- **As a** user
- **I want** to export a PDF report of scan results
- **So that** I have a professional document to share

**US-7.2:** Photo Evidence
- **As a** user
- **I want** to attach photos of threats to the report
- **So that** I have visual proof of what I found

**US-7.3:** Timestamp & Geolocation
- **As a** user
- **I want** reports to include timestamps and location
- **So that** my evidence is credible and verifiable

**US-7.4:** Chain of Custody
- **As a** user
- **I want** reports to be cryptographically signed
- **So that** they can be used as legal evidence

---

## 3. Detailed Use Cases

### Use Case 1: Hotel Room Privacy Check

**Primary Actor:** Sarah (Privacy-Conscious Traveler)

**Preconditions:**
- Sarah has checked into a hotel room
- Sarah has the RF Shield app installed
- App has location and Bluetooth permissions

**Trigger:** Sarah opens the RF Shield app

**Main Flow:**

1. Sarah opens RF Shield app
2. App displays home screen with prominent "Scan This Room" button
3. Sarah taps "Scan This Room"
4. App shows "Scanning..." animation with progress indicator
5. App performs WiFi scan (5 seconds)
   - Detects: Hotel WiFi, 2 neighboring networks, 1 Wyze Cam
6. App performs BLE scan (10 seconds)
   - Detects: Sarah's AirPods, hotel TV remote
7. App completes scan and displays results screen:
   - **Threat Count:** 1 device flagged
   - **Total Devices:** 5 devices found
   - **Scan Duration:** 58 seconds
8. Results screen shows list:
   - ✅ Hotel_WiFi_Guest (Expected - Router)
   - ✅ Samsung Smart TV (Expected - Hotel TV)
   - 🚨 **Wyze_Cam_v3 (THREAT - Hidden Camera)**
   - ✅ AirPods Pro (Safe - Your Device)
   - ⚠️ Unknown BLE Device (Investigate)
9. Sarah taps on "Wyze_Cam_v3" entry
10. Detail screen shows:
    - **Device Type:** WiFi Camera
    - **Manufacturer:** Wyze Labs
    - **Signal Strength:** -45 dBm (Very Strong - Very Close)
    - **Channel:** 6
    - **Encryption:** WPA2-PSK
    - **Threat Reason:** "WiFi camera detected in bedroom area"
    - **Actions:**
      - 🎯 [Find It] (Hot/Cold locator)
      - 📸 [Take Photo]
      - 📋 [Export Report]
      - ☎️ [Contact Hotel Management]
11. Sarah taps [Find It]
12. App shows RSSI meter (hot/cold game)
13. Sarah walks around room, meter shows:
    - Near window: -65 dBm (Cold)
    - Near bathroom: -70 dBm (Colder)
    - Near smoke detector on ceiling: -35 dBm (🔥 HOT!)
14. Sarah investigates smoke detector
15. Sarah finds camera lens in smoke detector
16. Sarah taps [Take Photo] and photographs device
17. Sarah taps [Export Report]
18. App generates PDF report:
    - Scan timestamp: 2024-12-14 22:15:30 CST
    - Location: Hotel Monaco Houston (GPS coords)
    - Threat: Wyze Cam v3
    - Photo evidence (attached)
    - Technical details (MAC, RSSI, channel)
19. App prompts: "Send report to hotel management?"
20. Sarah taps "Yes"
21. App generates pre-filled email:
    - To: frontdesk@hotelmonaco.com
    - Subject: Security Concern - Hidden Camera in Room 302
    - Body: Professional report attached
22. Sarah sends email
23. Sarah contacts hotel security

**Postconditions:**
- Threat identified and documented
- Evidence collected for authorities
- Hotel management notified
- Sarah has peace of mind or takes further action

**Alternative Flows:**

**Alt-1: No Threats Found**
- Step 7: App shows "✅ Room is Clear - No Threats Detected"
- Sarah feels reassured and goes to sleep

**Alt-2: Camera is False Positive (user's own device)**
- Step 9: Sarah recognizes the Wyze Cam as her own device
- Sarah taps "Mark as Safe"
- App remembers device for future scans

**Alt-3: Unable to Locate Threat Physically**
- Step 13: Sarah can't find device despite hot signal
- Sarah taps "Unable to Locate"
- App suggests: "Device may be hidden in wall or ceiling. Consider professional TSCM sweep."
- App offers [Request Pro Sweep] button

---

### Use Case 2: AirTag Stalking Detection

**Primary Actor:** Maria (Domestic Violence Survivor)

**Preconditions:**
- Maria suspects she's being tracked
- Maria has downloaded the free RF Shield app
- Maria is near her car (where tracker is suspected)

**Trigger:** Maria opens the app after advocacy group recommendation

**Main Flow:**

1. Maria opens RF Shield app for the first time
2. App shows quick 3-screen tutorial:
   - Screen 1: "Find Hidden Trackers"
   - Screen 2: "Follow Hot/Cold Guide"
   - Screen 3: "Document Evidence"
3. Maria skips tutorial (urgent need)
4. App home screen shows:
   - 🎯 **[Find AirTag]** (prominent button)
   - [Scan This Room]
   - [Help & Resources]
5. Maria taps [Find AirTag]
6. App shows: "Scanning for trackers..." (15 seconds)
7. App displays result:
   - **🚨 ALERT: Unknown AirTag Detected**
   - **Status:** Not registered to you
   - **Signal:** -52 dBm (Nearby)
   - **Separated from Owner:** Yes (tracking you)
8. Screen shows large [Locate It] button
9. Maria taps [Locate It]
10. App switches to hot/cold locator mode:
    - Screen shows large RSSI meter (visual + haptic)
    - Instructions: "Walk around your car. Meter will show when you're close."
11. Maria walks around car:
    - Near driver door: -55 dBm (Warm)
    - Near rear bumper: -40 dBm (Hot)
    - Under rear bumper: -30 dBm (🔥 VERY HOT!)
12. Phone vibrates intensely (haptic feedback)
13. Maria crouches down and looks under bumper
14. Maria sees AirTag in magnetic case
15. Maria removes AirTag
16. App detects signal disappeared:
    - "✅ Tracker Removed - Signal Lost"
    - "Do you want to document this as evidence?"
17. Maria taps "Yes"
18. App opens evidence documentation flow:
    - [Take Photo of Tracker]
    - [Take Photo of Location Where Found]
    - [Add Notes] (optional)
19. Maria takes photos
20. App asks: "Where did you find it?"
    - Maria selects: "Vehicle - Under Bumper"
21. App generates evidence report (PDF):
    - Detection timestamp
    - Removal timestamp
    - Photos
    - AirTag serial number (from BLE broadcast)
    - Location found
22. App offers options:
    - [Save to Phone]
    - [Email to Myself]
    - [Share with Police]
    - [Share with Advocate]
23. Maria selects [Email to Myself] + [Share with Advocate]
24. App displays domestic violence resources:
    - National DV Hotline: 1-800-799-7233
    - Local shelter: (713) 555-0199
    - Legal aid: texaslawhelp.org
25. Maria saves report and calls advocate

**Postconditions:**
- Tracker found and removed
- Evidence documented
- Maria has proof for restraining order
- Maria connected to support resources

**Alternative Flows:**

**Alt-1: No AirTag Found**
- Step 7: App shows "No AirTags Detected"
- App suggests: "Check other areas (home, belongings)"
- App offers: [Scan for Other Trackers] (GPS, Tile, etc.)

**Alt-2: AirTag Belongs to User**
- Step 7: App shows "AirTag Found - Registered to Your Apple ID"
- App: "This is your own AirTag, not a threat"

**Alt-3: Multiple AirTags Found**
- Step 7: App shows "2 Unknown AirTags Detected"
- Maria taps [Locate First One]
- After removing first: App shows [Locate Second One]

**Alt-4: AirTag Disabled**
- Step 11: AirTag battery dead or removed
- App shows: "Signal weak or intermittent. Tracker may be powered off."
- App suggests: "Perform physical search of suspected areas"

---

### Use Case 3: Corporate Espionage Prevention

**Primary Actor:** James (Corporate Executive)

**Preconditions:**
- James has Executive Protection Kit ($299)
- James checked into conference hotel
- James needs to have confidential call with investors

**Trigger:** James enters hotel room before important call

**Main Flow:**

1. James unpacks RF Shield Executive Kit:
   - ESP32 Marauder module
   - RTL-SDR module
   - Camera lens detector
   - Ultrasonic jammer
   - IR flood light
2. James opens RF Shield app (Pro tier)
3. App home screen shows:
   - [Quick Scan]
   - **[Full Scan]** (recommended for James)
   - [Countermeasures]
   - [Pro TSCM Request]
4. James taps [Full Scan]
5. App shows: "Connect hardware modules"
6. James powers on ESP32 module
7. App auto-discovers ESP32 via Bluetooth:
   - "RF Shield ESP32 (v1.3.0) Connected ✓"
8. App detects RTL-SDR plugged into phone USB-C:
   - "RTL-SDR Module Connected ✓"
9. App shows scan options:
   - ☑️ WiFi (Phone + ESP32)
   - ☑️ Bluetooth (Phone + ESP32)
   - ☑️ Sub-GHz 315/433 MHz (ESP32)
   - ☑️ Analog Cameras 1.2/2.4/5.8 GHz (RTL-SDR)
   - ☑️ GPS Jamming Detection (RTL-SDR)
   - [Start Full Scan] (Est. 5 minutes)
10. James taps [Start Full Scan]
11. App displays progress:
    - ⏳ WiFi scan... (3 sec)
    - ⏳ BLE scan... (10 sec)
    - ⏳ Sub-GHz sweep... (30 sec)
    - ⏳ Spectrum analysis... (2 min)
12. Scan completes after 4 minutes 23 seconds
13. Results screen shows:
    - **🚨 2 Threats Detected**
    - **⚠️ 1 Suspicious Device**
    - ✅ 12 Safe Devices
14. Threats listed:
    - 🚨 **Evil Twin AP: "Conference_WiFi_Guest"**
      - Real Hotel WiFi: "ConferenceHotel_Guest"
      - Threat: Man-in-the-middle attack (intercepting data)
      - Location: Signal strongest near window
    - 🚨 **433 MHz Transmitter**
      - Detected: Continuous transmission
      - Frequency: 433.920 MHz
      - Modulation: ASK/OOK
      - Location: Signal strongest near desk lamp
15. Suspicious device:
    - ⚠️ **Unknown WiFi Device (MAC: 11:22:33...)**
      - No manufacturer data
      - Hidden SSID
      - Signal: -35 dBm (Very close)
16. James taps on "433 MHz Transmitter"
17. Detail screen shows:
    - **Type:** RF Bug (likely audio/video transmitter)
    - **Range:** ~100 meters
    - **Battery:** Likely powered (continuous transmission)
    - **Recording:** Possible audio/video transmission
    - [Locate Device]
    - [Activate Jammer]
    - [View Spectrum]
18. James taps [Locate Device]
19. App shows hot/cold locator for 433 MHz signal
20. James walks around room:
    - Near bed: -75 dBm
    - Near desk lamp: -45 dBm (Hot)
    - Inside desk lamp base: -30 dBm (VERY HOT)
21. James unplugs lamp and examines base
22. James finds small RF transmitter hidden in lamp base
23. James takes photos (attached to evidence report)
24. James returns to app and taps [Activate Jammer]
25. App shows countermeasure controls:
    - 🔊 **Ultrasonic Audio Jammer**
      - Status: Off
      - [Activate] button
    - 💡 **IR Flood Light**
      - Status: Off
      - [Activate] button
26. James activates ultrasonic jammer:
    - App sends Bluetooth command to jammer module
    - Jammer emits 25 kHz tone (inaudible to humans)
    - Confirmation: "Audio protection active ✓"
27. James reviews WiFi threats
28. James sees "Evil Twin AP" warning
29. James disables hotel WiFi on phone
30. James enables VPN over cellular data
31. James conducts investor call (protected):
    - RF bug disabled (physical removal)
    - Ultrasonic jammer active (protects from other mics)
    - VPN over cellular (no evil twin risk)
32. After call, James exports comprehensive report:
    - Scan timestamp
    - 2 threats found (with photos)
    - 1 suspicious device
    - Technical details (frequencies, MAC addresses, RSSI)
    - Countermeasures activated
    - GPS location (hotel address)
33. James emails report to company InfoSec team
34. InfoSec team responds: "Recommend professional sweep of conference room"
35. James opens app, taps [Pro TSCM Request]
36. App shows form:
    - Location: Pre-filled (current hotel)
    - Type: James selects "Conference Room"
    - Urgency: James selects "High"
    - Notes: "Found RF bug in hotel room, need sweep of meeting space"
37. James submits request
38. App matches 3 nearby TSCM firms:
    - Houston TSCM Services ($2,500)
    - Texas Security Sweeps ($2,200)
    - Executive Protection LLC ($3,000)
39. James selects "Texas Security Sweeps"
40. Firm responds within 1 hour:
    - "Available tomorrow morning 8 AM"
    - "Quote: $2,500 for conference room sweep"
41. James books sweep through app
42. Next morning, TSCM team performs professional sweep
43. TSCM report confirms: No additional threats in conference room
44. James proceeds with investor meetings (confident in security)

**Postconditions:**
- All threats identified
- Immediate countermeasures activated
- Professional verification obtained
- Investor call secure
- Company IP protected
- Evidence documented for insurance/legal

**Alternative Flows:**

**Alt-1: No Threats Found**
- Step 13: "✅ All Clear - No Threats Detected"
- James activates countermeasures anyway (paranoid mode)
- James proceeds with call (high confidence)

**Alt-2: Unable to Afford Pro TSCM**
- Step 35: James reviews $2,500 quote
- Too expensive for personal budget
- James asks company to cover cost
- Company approves (business expense)

**Alt-3: Sophisticated Threat (GPS Jammer Detected)**
- Step 13: App shows "GPS Jamming Detected"
- James realizes: Someone is jamming GPS (sophisticated attack)
- James immediately calls company security
- Company security contacts FBI (potential criminal activity)

---

## 4. User Journeys

### Journey 1: First-Time User (Sarah)

**Phase 1: Discovery**
- Sarah reads news article about hidden cameras in Airbnb
- Article mentions RF Shield app
- Sarah searches "RF Shield" in App Store
- Sarah reads app description and reviews (4.8 stars)
- Sarah sees free tier available
- Sarah downloads app

**Phase 2: Onboarding**
- App opens to welcome screen
- Tutorial (3 screens, 30 seconds):
  1. "Find hidden cameras & trackers"
  2. "Get instant results"
  3. "Take action with confidence"
- Sarah grants permissions (Location, Bluetooth)
- App shows home screen

**Phase 3: First Scan**
- Sarah in hotel room, opens app
- Large "Scan This Room" button visible
- Sarah taps button (no hesitation - clear CTA)
- Scan runs (58 seconds)
- Sarah sees: "1 Threat Detected"
- Sarah taps on threat
- Clear explanation: "WiFi camera found"
- Sarah uses hot/cold to locate
- Sarah finds camera

**Phase 4: Evidence & Action**
- Sarah takes photos
- Sarah exports PDF report
- Sarah emails hotel management
- Sarah feels empowered (solved problem)

**Phase 5: Conversion to Premium**
- Next day, Sarah tries second scan
- App shows: "2 of 3 free scans used today"
- Sarah realizes limitations
- Sarah travels often (2-3x/month)
- Sarah upgrades to premium ($79/year)
- Reasoning: "Worth $2.50/night for peace of mind"

**Phase 6: Loyalty**
- Sarah scans every hotel/Airbnb
- Sarah recommends app to friends
- Sarah writes 5-star review
- Sarah renews premium subscription

**Emotional Arc:**
- **Discovery:** Curious, concerned
- **Onboarding:** Hopeful, slightly skeptical
- **First Scan:** Nervous, then shocked (found threat!)
- **Evidence:** Empowered, validated
- **Conversion:** Confident in value
- **Loyalty:** Advocating, trusting

---

### Journey 2: Urgent Need (Maria)

**Phase 1: Crisis**
- Maria realizes she's being tracked
- Maria calls domestic violence hotline
- Advocate recommends RF Shield (free tier)
- Maria downloads immediately

**Phase 2: Immediate Use**
- Maria skips tutorial (urgent)
- Maria taps "Find AirTag"
- Scan runs (15 seconds - fast!)
- Alert: "Unknown AirTag Detected"
- Maria follows hot/cold guide
- Maria removes tracker (relief!)

**Phase 3: Evidence**
- App prompts: "Document this?"
- Maria takes photos
- App generates report
- App shows DV resources
- Maria emails evidence to advocate

**Phase 4: Safety**
- Maria feels safer (tracker removed)
- Maria shares app with support group
- Maria doesn't upgrade (free tier sufficient)
- Maria leaves positive review (free tier is generous)

**Emotional Arc:**
- **Crisis:** Terrified, desperate
- **Immediate Use:** Hopeful, determined
- **Evidence:** Relieved, grateful
- **Safety:** Empowered, cautious optimism

---

### Journey 3: Professional Use (Detective Rodriguez)

**Phase 1: Business Need**
- Client requests bug sweep ($300 quote)
- Rodriguez can't afford $2k TSCM firm
- Rodriguez searches for affordable tools
- Rodriguez finds RF Shield ($299 Executive Kit)

**Phase 2: Evaluation**
- Rodriguez orders kit
- Rodriguez tests on own office
- Rodriguez compares to professional TSCM quote
- Results: 70-80% effective vs pro (good enough!)

**Phase 3: Client Service**
- Rodriguez offers sweeps ($300 vs $2k competitor)
- Rodriguez books 5 sweeps first month
- Rodriguez uses app to generate reports
- Clients satisfied (professional-looking PDFs)

**Phase 4: Growth**
- Rodriguez offers sweeps as package deal
- Rodriguez recommends pro TSCM for serious cases
- RF Shield partner program: Rodriguez earns referral fee
- Revenue stream grows (10 sweeps/month @ $300 = $3k/mo revenue)

**Phase 5: Advocacy**
- Rodriguez writes case study for PI magazine
- Rodriguez trains other PIs on tool
- Rodriguez becomes RF Shield affiliate

**Emotional Arc:**
- **Business Need:** Frustrated (can't serve clients)
- **Evaluation:** Skeptical, then impressed
- **Client Service:** Confident, professional
- **Growth:** Excited (new revenue stream)
- **Advocacy:** Loyal, evangelizing

---

## 5. Acceptance Criteria

### Feature: Quick Room Scan

**Scenario: Successful scan with no threats**

**Given** I am a logged-in user  
**And** I am in a room with no surveillance devices  
**When** I tap "Scan This Room"  
**Then** The scan should complete in <60 seconds  
**And** Results should show "✅ Room is Clear"  
**And** Results should list all detected devices (WiFi, BLE)  
**And** All devices should be marked as "Safe" or "Expected"  

---

**Scenario: Scan detects WiFi camera**

**Given** I am a logged-in user  
**And** There is a WiFi camera (Wyze Cam) in the room  
**When** I tap "Scan This Room"  
**Then** The scan should detect the WiFi camera  
**And** Results should show "🚨 1 Threat Detected"  
**And** The camera should be labeled "Wyze_Cam_v3"  
**And** Threat level should be "THREAT"  
**And** Threat reason should be "WiFi camera detected"  
**And** I should see options: [Find It], [Take Photo], [Export Report]  

---

**Scenario: Hot/cold device location**

**Given** I detected a threat  
**And** I tapped [Find It]  
**When** I move closer to the device  
**Then** The RSSI meter should show stronger signal  
**And** The meter color should change (cold → warm → hot)  
**And** My phone should vibrate when very close (< 1 meter)  
**And** Accuracy should be within 2 meters  

---

**Scenario: Evidence export**

**Given** I detected a threat  
**And** I took photos of the device  
**When** I tap [Export Report]  
**Then** A PDF should be generated  
**And** PDF should include: timestamp, location, threat details, photos  
**And** PDF should be cryptographically signed (SHA-256 hash)  
**And** I should be able to share via email, cloud storage, or save locally  

---

### Feature: AirTag Detection

**Scenario: Detect separated AirTag**

**Given** There is an AirTag within BLE range  
**And** The AirTag is separated from its owner  
**When** I tap "Find AirTag"  
**Then** The app should detect the AirTag within 15 seconds  
**And** Results should show "🚨 Unknown AirTag Detected"  
**And** Status should show "Separated from Owner: Yes"  
**And** I should see a [Locate It] button  

---

**Scenario: Play sound on AirTag**

**Given** I detected an unknown AirTag  
**When** I tap [Play Sound]  
**Then** The AirTag should emit an audible beep  
**And** The beep should last 5-10 seconds  
**And** I should see confirmation: "Sound played on AirTag"  

**Note:** This requires Apple's Find My network cooperation or direct BLE command

---

**Scenario: AirTag belongs to user**

**Given** There is an AirTag within range  
**And** The AirTag is registered to my Apple ID  
**When** I scan for AirTags  
**Then** The app should identify it as mine  
**And** Results should show "✅ Your AirTag"  
**And** No threat alert should be shown  

---

### Feature: Hardware Module Pairing

**Scenario: Pair ESP32 module**

**Given** I have an RF Shield ESP32 module  
**And** The module is powered on  
**When** I open the app  
**Then** The app should discover the module automatically  
**And** I should see "RF Shield ESP32 Found"  
**And** I should tap [Connect]  
**And** Pairing should complete within 10 seconds  
**And** Module status should show "Connected ✓"  

---

**Scenario: Firmware update available**

**Given** My ESP32 module is connected  
**And** A new firmware version is available  
**When** The app checks for updates  
**Then** I should see a notification: "Update Available (v1.3.0)"  
**And** I should tap [Update Now]  
**And** The update should download (progress bar)  
**And** The update should install via BLE  
**And** The module should reboot  
**And** The new version should be verified  
**And** The entire process should take <5 minutes  

---

**Scenario: Low battery warning**

**Given** My ESP32 module battery is <20%  
**When** I start a scan  
**Then** I should see a warning: "Module battery low (15%)"  
**And** The scan should still proceed  
**And** I should be prompted to charge after scan completes  

---

### Feature: Continuous Monitoring

**Scenario: Background scan detects new device**

**Given** I enabled continuous monitoring  
**And** A new WiFi camera appears in the room  
**When** The background scan runs (every 5 minutes)  
**Then** I should receive a push notification: "New Device Detected"  
**And** Notification should show device name and threat level  
**And** Tapping notification should open the app to results  

---

**Scenario: Battery impact acceptable**

**Given** Continuous monitoring is enabled  
**When** Monitoring runs for 24 hours  
**Then** Battery drain should be <5%  
**And** No ANR (Application Not Responding) errors should occur  
**And** App should remain responsive  

---

### Feature: Countermeasures

**Scenario: Activate ultrasonic jammer**

**Given** I have an ultrasonic jammer module  
**And** The module is connected and charged  
**When** I tap [Activate Audio Protection]  
**Then** The jammer should activate within 1 second  
**And** I should see confirmation: "Ultrasonic jammer active ✓"  
**And** The module should emit 25 kHz tone (inaudible to me)  
**And** Battery status should be displayed  
**And** Auto-shutoff should activate after 2 hours (safety)  

---

**Scenario: Verify jammer effectiveness**

**Given** The ultrasonic jammer is active  
**And** I have a MEMS microphone to test  
**When** I record audio near the jammer  
**Then** The recording should be unintelligible (saturated)  
**And** Frequency analysis should show 25 kHz spike  

---

### Feature: TSCM Professional Referral

**Scenario: Request professional sweep**

**Given** I am a premium user  
**And** I found a threat I can't remove myself  
**When** I tap [Request Pro Sweep]  
**Then** I should see a form with: Location, Urgency, Notes  
**And** I should fill out the form  
**And** I should tap [Submit Request]  
**And** I should see "Request sent to 3 nearby firms"  
**And** I should receive responses within 24 hours  

---

**Scenario: Compare TSCM quotes**

**Given** I submitted a sweep request  
**And** 3 firms responded with quotes  
**When** I view the responses  
**Then** I should see: Firm name, price range, availability, rating  
**And** I should be able to select a firm  
**And** I should be able to schedule a sweep  

---

### Feature: Premium Subscription

**Scenario: Free tier limitations**

**Given** I am a free tier user  
**When** I perform 3 scans in one day  
**Then** The 4th scan should be blocked  
**And** I should see: "Daily limit reached (3/3 scans)"  
**And** I should see an upgrade prompt: "Get unlimited scans with Premium ($79/year)"  

---

**Scenario: Upgrade to premium**

**Given** I am a free tier user  
**When** I tap [Upgrade to Premium]  
**Then** I should see pricing options: $9.99/month or $79/year  
**And** I should select a plan  
**And** I should complete payment via Stripe  
**And** Payment should process within 5 seconds  
**And** I should see confirmation: "Welcome to Premium!"  
**And** I should immediately have unlimited scans  

---

### Feature: Reporting

**Scenario: Generate professional report**

**Given** I completed a scan  
**And** I detected 2 threats  
**When** I tap [Export Report]  
**Then** A PDF should be generated within 5 seconds  
**And** PDF should include:
  - Cover page with logo
  - Scan summary (date, time, location)
  - Threat list with details (MAC, RSSI, photos)
  - Technical appendix (raw data)
  - Digital signature (SHA-256 hash)  
**And** PDF should be formatted professionally (not just raw text)  

---

**Scenario: Share report with authorities**

**Given** I generated a report  
**When** I tap [Share with Police]  
**Then** I should see a pre-filled email:
  - To: [Local PD email or blank]
  - Subject: "Security Incident Report - [Date]"
  - Body: Brief explanation + PDF attached  
**And** I should be able to send the email  

---

**END OF USER STORIES & USE CASES**
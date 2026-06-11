# Motion Detection Alarm System - User Manual & Setup Guide

## 🎯 Quick Start

### Installation

1. **Install Python Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   python run.py
   ```

   OR for CLI mode:
   ```bash
   python main.py
   ```

### System Requirements

- **Python**: 3.7 or higher
- **RAM**: 512 MB minimum
- **CPU**: Dual-core processor recommended
- **Camera**: USB webcam or built-in camera
- **OS**: Windows, macOS, or Linux

---

## 📊 GUI Application Overview

The Motion Detection Alarm System GUI provides a professional, user-friendly interface with 5 main tabs:

### 1. **📹 Live Feed Tab**

**Purpose:** Real-time video monitoring with motion detection visualization

**Components:**
- **Video Display Area**: 800x600 px live camera feed
- **Motion Notifications**: Red "MOTION DETECTED!" text appears when motion is detected
- **Bounding Boxes**: Green rectangles highlight detected motion regions
- **Real-time Statistics**:
  - FPS (Frames Per Second)
  - Total Frames Processed
  - Motion Status Indicator
  - Snapshot Count

**Controls:**
- ▶ **Start Monitoring**: Begins motion detection
- ⏹ **Stop Monitoring**: Stops camera capture and monitoring
- 📸 **Manual Snapshot**: Captures current frame manually

**Motion Detection Algorithm:**
The system uses frame-by-frame differencing:
1. Each frame is converted to grayscale and blurred (noise reduction)
2. Current frame is subtracted from previous frame
3. Threshold is applied to identify significant changes
4. Contours are detected and filtered by minimum area
5. If motion contours exceed threshold → Alert triggered

---

### 2. **⚙️ Configuration Tab**

**Purpose:** Fine-tune system sensitivity and alert parameters

**Settings:**

#### Camera Settings
- **Camera ID** (0-10)
  - `0` = Built-in/Default camera
  - `1` = External USB camera
  - `2+` = Additional cameras or virtual cameras
  - Default: `0`

#### Motion Detection Settings
- **Sensitivity Threshold** (Range: 5-100)
  - Controls how much pixel change triggers detection
  - **Lower value** = More sensitive (detects subtle motion)
  - **Higher value** = Less sensitive (only obvious motion)
  - **Recommended values by environment**:
    - Office/Indoor: 20-30
    - Home Security: 15-25
    - Warehouse: 25-40
    - Low-light: 10-20
  - Default: `25`

- **Min Motion Area** (Range: 100-10,000 pixels²)
  - Minimum contour area to trigger alarm
  - Filters out noise and small artifacts
  - **Recommended values**:
    - Small room: 300-500
    - Large room: 500-1000
    - Warehouse: 1000-2000
  - Default: `500`

#### Alert Settings
- **Beep Frequency** (Range: 100-5,000 Hz)
  - Audio pitch of alert sound
  - 1000 Hz = Default beep tone
  - Higher = Higher pitched sound
  - Lower = Lower pitched sound

- **Beep Duration** (Range: 100-2,000 ms)
  - How long the alert sound plays
  - 500 ms = 0.5 seconds (default)
  - Longer = More noticeable alert

**Actions:**
- ✓ **Apply Settings**: Save configuration changes (requires monitoring restart for camera changes)
- ↻ **Reset to Defaults**: Revert all settings to original values

---

### 3. **📊 Event History Tab**

**Purpose:** Track and analyze all motion detection events

**Features:**
- **Event Table** displays:
  - **Timestamp**: Date and time of event (YYYY-MM-DD HH:MM:SS.mmm)
  - **Event Type**: Motion Alert, Manual Snapshot, Configuration Changed, etc.
  - **Details**: Additional information about the event

- **Event Types**:
  - `Motion Alert` - Motion detected by system
  - `Manual Snapshot` - User captured snapshot manually
  - `Configuration Updated` - Settings changed
  - `System Started/Stopped` - Monitoring state change
  - `History Cleared` - Event log cleared

**Actions:**
- 🗑️ **Clear History**: Delete all logged events (cannot be undone)
- 💾 **Export to CSV**: Save all events to CSV file for analysis/backup

**CSV Export Format:**
```
Timestamp,Event Type,Details
"2026-04-04 14:30:25.123","Motion Alert","Motion detected with 3 region(s)"
"2026-04-04 14:30:30.456","Manual Snapshot","User captured snapshot manually"
```

---

### 4. **📷 Snapshots Tab**

**Purpose:** Manage captured snapshots from motion detection

**Display Information:**
- Total snapshot count
- File list with:
  - Filename (timestamp-based format)
  - File size (KB)
  - Date modified

**Snapshot Filename Format:**
```
snapshot_YYYY_MM_DD_HHMMSS_MMM.jpg
```
Example: `snapshot_2026_04_04_143025_123.jpg`

**Actions:**
- 🔄 **Refresh**: Update list of snapshots in folder
- 📂 **Open Folder**: Launch file explorer/finder to browse snapshots
- 🗑️ **Delete Old Snapshots**: Remove snapshots older than 7 days

**Snapshot Storage:**
- Default folder: `snapshots/` (relative to application)
- Snapshots are JPEG format
- ~50-100 KB per snapshot (depends on resolution)
- Approximately 500-1000 snapshots per 50 MB of storage

---

### 5. **📖 Help & Documentation Tab**

**Contains:**
- Complete system overview
- Component descriptions
- Configuration recommendations
- Best practices
- Troubleshooting guide
- Technical details
- System requirements
- Keyboard shortcuts

---

## 🔧 Configuration Examples

### Office Building Security
```
Camera ID:              0
Sensitivity Threshold:  25
Min Motion Area:        500
Beep Frequency:         1000 Hz
Beep Duration:          500 ms
```
**Why:** Medium sensitivity for normal lighting, standard alert

### Home 24/7 Monitoring
```
Camera ID:              0
Sensitivity Threshold:  18
Min Motion Area:        300
Beep Frequency:         800 Hz
Beep Duration:          1000 ms
```
**Why:** Higher sensitivity for catching all motion, longer alert for nighttime awareness

### Warehouse with High Ceilings
```
Camera ID:              0
Sensitivity Threshold:  35
Min Motion Area:        1500
Beep Frequency:         1500 Hz
Beep Duration:          500 ms
```
**Why:** Less sensitive to reduce false positives from distant movement, larger min area

### Dark/Low-Light Environment
```
Camera ID:              0
Sensitivity Threshold:  12
Min Motion Area:        200
Beep Frequency:         1000 Hz
Beep Duration:          800 ms
```
**Why:** Very sensitive for detecting any change, larger audio alert

---

## 🐛 Troubleshooting

### Problem: Camera Not Opening
**Error Message:** "Failed to open camera. Check camera ID in settings."

**Solutions:**
1. Try different Camera ID values (0, 1, 2...)
2. Check if camera is already in use by another app
3. Restart the application
4. Restart your computer
5. Check Device Manager for camera drivers (Windows)
6. Grant camera permissions (macOS/Linux)

### Problem: No Motion Detected
**Symptoms:** System running but not detecting obvious motion

**Solutions:**
1. **Lower the Sensitivity Threshold**:
   - Try values: 15, 10, 5
   - Lower = more sensitive
2. **Increase lighting** in monitored area
3. **Lower Min Motion Area** setting
4. **Check camera position** - ensure clear view of movement
5. **Move closer** to camera to test detection

### Problem: Too Many False Alerts
**Symptoms:** Alert triggering without real motion

**Solutions:**
1. **Increase Sensitivity Threshold**:
   - Try values: 40, 50, 60
   - Higher = less sensitive
2. **Increase Min Motion Area** to filter noise
3. **Reduce camera sensitivity** (camera settings, not app settings)
4. **Eliminate light sources** creating flicker
5. **Stabilize camera** (reduce vibration)
6. **Filter reflective surfaces** (minimize window glare)

### Problem: Low FPS (Slow Video)
**Symptoms:** Video appears choppy, low FPS indicator

**Solutions:**
1. Close other applications
2. Reduce monitor resolution temporarily
3. Disable other resource-heavy applications
4. Use lower camera resolution
5. Check CPU usage (Task Manager)

### Problem: Snapshots Not Saving
**Symptoms:** Snapshot button doesn't create files

**Solutions:**
1. Check folder permissions for `snapshots/` directory
2. Ensure disk space available (at least 100 MB)
3. Verify snapshots folder exists and is writable
4. Check file explorer - files may be hidden
5. Try opening snapshots folder from app (will create if missing)

### Problem: Beep/Audio Not Working
**Windows:**
- Check system volume settings
- Verify audio output device is enabled
- Test with other applications

**macOS/Linux:**
- Check volume settings
- Verify audio system is functional
- May require installing `playsound` package

---

## 📈 Performance Tips

1. **CPU Usage**
   - Close unnecessary background applications
   - Disable screen overlays (Discord, OBS, etc.)
   - Use FPS indicator to monitor performance

2. **Memory Usage**
   - Regularly clear event history
   - Delete old snapshots periodically
   - Restart application if memory usage grows

3. **Network (if using cloud saving)**
   - Use local storage for snapshots (faster)
   - Export logs periodically to backup to cloud

4. **Camera Performance**
   - Use appropriate resolution (720p-1080p sufficient)
   - Ensure good USB connection
   - Use USB 3.0+ for faster transfer rates

---

## 🔐 Security Notes

- **Snapshots location**: Default is local `snapshots/` folder
- **Event logs**: Stored in application memory (exported as CSV)
- **Configuration**: Stored in memory during session
- **No cloud upload**: By default, data stays local
- **Recording**: System does NOT record video - only snapshots on motion

---

## 📝 File Structure

```
Motion-Detection Alarm System/
├── run.py                    # GUI launcher (start here)
├── main.py                   # CLI version
├── gui.py                    # GUI application code
├── config.py                 # Configuration settings
├── motion_detector.py        # Motion detection algorithm
├── alarm.py                  # Audio alert system
├── snapshot_manager.py       # Snapshot management
├── utils.py                  # Image processing utilities
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── snapshots/                # Captured snapshots (auto-created)
    └── snapshot_*.jpg        # Snapshot files
```

---

## 🚀 Advanced Usage

### Running in Headless Mode (No GUI)
```bash
python main.py
```

### Exporting Event Logs
1. Open "Event History" tab
2. Click "Export to CSV"
3. Select save location
4. CSV file contains all motion events with timestamps

### Batch Deleting Old Snapshots
1. Open "Snapshots" tab
2. Click "Delete Old Snapshots" button
3. Removes all snapshots older than 7 days

### Changing Default Configuration
Edit `config.py`:
```python
CAMERA_ID = 0
THRESHOLD_VALUE = 25
MIN_CONTOUR_AREA = 500
BEEP_FREQUENCY = 1000
BEEP_DURATION = 500
```

---

## 📞 Support & FAQ

**Q: Can I use multiple cameras?**
A: Yes! Change Camera ID in Configuration tab (0=first, 1=second, etc.)

**Q: How many snapshots can I store?**
A: Approximately 500-1000 per 50 MB. Delete old ones regularly.

**Q: Can I export video instead of snapshots?**
A: Current version captures snapshots only. Video requires additional setup.

**Q: What's the maximum monitoring duration?**
A: Unlimited! System runs continuously until stopped.

**Q: Can I run on Raspberry Pi?**
A: Yes! Ensure Python 3.7+ and required packages installed.

**Q: Does it work with IP cameras?**
A: Yes! If your IP camera supports RTSP protocol, use RTSP URL as camera input.

---

## Version Information

- **Application**: Motion Detection Alarm System v1.0
- **GUI Framework**: PyQt5 5.15.9
- **OpenCV**: 4.8.1.78
- **Python**: 3.7+
- **Release Date**: 2026

---

## License & Attribution

© 2026 Motion Detection Alarm System
Educational use permitted.

---

## Changelog

### Version 1.0 (2026-04-04)
- Initial release
- GUI implementation with 5 tabs
- Real-time motion detection
- Event logging and history
- Snapshot management
- Built-in documentation
- Configuration management

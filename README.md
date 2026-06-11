# Motion Detection Alarm System

A professional Python-based motion detection and alarm system with GUI support, ROI (Region of Interest) selection, real-time monitoring, snapshot capture, and configurable alerts.

![Python](https://img.shields.io/badge/Python-3.7+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 📋 Table of Contents
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **Real-time Motion Detection** - Advanced frame-differencing algorithm with customizable sensitivity
- **GUI Application** - Professional PyQt5-based user interface with 5 main tabs
- **ROI Support** - Define custom Region of Interest for focused motion detection
- **Snapshot Capture** - Automatically save motion-triggered snapshots with timestamps
- **Audio Alerts** - Configurable beep sounds with frequency and duration control
- **Live Statistics** - Real-time FPS, frame count, and motion status monitoring
- **CLI Mode** - Headless operation for server environments
- **Cross-Platform** - Works on Windows, macOS, and Linux

## 🖥️ System Requirements

- **Python**: 3.7 or higher
- **RAM**: 512 MB minimum
- **CPU**: Dual-core processor recommended
- **Camera**: USB webcam or built-in camera
- **OS**: Windows, macOS, or Linux
- **Dependencies**: OpenCV, NumPy, PyQt5, Pillow (see requirements.txt)

---

## � Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RameeshaAkram/Motion-Detection-Alarm-System-.git
   cd Motion-Detection-Alarm-System-
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Python requirements:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Start

### GUI Mode (Recommended)
```bash
python run.py
```
Launches the professional PyQt5 GUI with 5 feature-rich tabs.

### CLI Mode
```bash
python main.py
```
Runs in terminal mode for headless/server environments.

---

## 📖 Usage

### GUI Application

The GUI provides 5 main tabs:

#### 1. **📹 Live Feed Tab**
- Real-time video stream with motion detection
- Motion indicators (red text + green bounding boxes)
- Live FPS and frame statistics
- Start/Stop Monitoring buttons
- Manual snapshot capture

#### 2. **⚙️ Configuration Tab**
- **Camera ID**: Select which camera to use (0=default, 1=external)
- **Sensitivity Threshold**: 5-100 (lower = more sensitive)
- **Min Motion Area**: Minimum pixels to trigger alarm (100-10,000)
- **Beep Frequency**: Customize alarm sound (100-5,000 Hz)
- **Beep Duration**: Alarm length in milliseconds

#### 3. **🎯 ROI (Region of Interest) Tab**
- Draw custom rectangular regions for focused detection
- Multiple ROIs supported
- Visual preview of selected areas
- Save/Load ROI configurations

#### 4. **📸 Snapshots Tab**
- View all captured motion snapshots
- Thumbnail gallery with timestamps
- Delete individual snapshots
- Open snapshots in default viewer
- Show snapshot metadata (time, size)

#### 5. **📚 Documentation Tab**
- In-app help and feature documentation
- Configuration recommendations
- Troubleshooting guide
- Keyboard shortcuts

### CLI Mode Features
- Command-line operation without GUI
- Real-time frame display in terminal window
- Press 'q' to quit, 's' to manually save snapshot
- Useful for remote servers and automation

---

## ⚙️ Configuration

Edit `config.py` to customize behavior:

```python
# Camera settings
CAMERA_ID = 0                          # 0=built-in, 1=external
BLUR_KERNEL_SIZE = (5, 5)             # Gaussian blur kernel

# Motion detection
THRESHOLD_VALUE = 25                   # Sensitivity (5-100, lower=more sensitive)
MIN_CONTOUR_AREA = 500                # Minimum motion area in pixels

# Display
WINDOW_NAME = "Motion Detection Alarm"
TEXT_COLOR = (0, 0, 255)              # Red
BOX_COLOR = (0, 255, 0)               # Green

# Audio alerts
BEEP_FREQUENCY = 1000                 # Hz
BEEP_DURATION = 500                   # milliseconds

# Storage
SNAPSHOT_FOLDER = "snapshots"          # Where to save snapshots
```

### Recommended Settings by Environment

| Environment | Threshold | Min Area |
|------------|-----------|----------|
| Office/Indoor | 20-30 | 300-500 |
| Home Security | 15-25 | 300-700 |
| Warehouse | 25-40 | 1000-2000 |
| Low-light | 10-20 | 200-500 |

---

## 📂 Project Structure

```
Motion-Detection-Alarm-System/
├── run.py                    # Entry point for GUI
├── main.py                   # Entry point for CLI
├── gui.py                    # PyQt5 GUI implementation
├── motion_detector.py        # Core motion detection algorithm
├── alarm.py                  # Audio alert functionality
├── snapshot_manager.py       # Snapshot capture & management
├── config.py                 # Configuration settings
├── utils.py                  # Utility functions
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── GUI_DOCUMENTATION.md      # Detailed GUI documentation
├── SETUP_GUIDE.md           # Installation & setup guide
└── snapshots/               # Captured motion snapshots (auto-created)
```

### Core Modules

**motion_detector.py**
- Frame-differencing algorithm
- ROI mask support
- Contour detection and filtering
- Configurable sensitivity

**gui.py**
- PyQt5 main application window
- VideoThread for background processing
- Tab-based interface design
- Real-time signal/slot communication

**alarm.py**
- Cross-platform audio alerts (Windows/Linux/macOS)
- Frequency and duration control

**snapshot_manager.py**
- Automatic snapshot saving with timestamps
- Snapshot gallery management
- File organization

**utils.py**
- Frame preprocessing (grayscale, blur)
- Image utility functions
- Shared helper methods

---

## 🎯 ROI (Region of Interest) Features

Focus motion detection on specific areas:

1. Open **ROI Tab** in GUI
2. Click **Draw ROI** to start
3. Click and drag to create rectangular region
4. Add multiple ROIs for complex monitoring scenarios
5. Click **Save ROI** to persist configuration
6. Motion detection only triggers within selected regions

Benefits:
- Eliminate false positives from irrelevant areas
- Reduce CPU usage
- Improve detection accuracy
- Monitor multiple zones independently

---

## 🔧 Troubleshooting

### Camera Not Opening
- Check `CAMERA_ID` in config.py (try 0, 1, or -1)
- Verify camera permissions (Linux may need `chmod`)
- Restart the application
- Test camera with other applications first

### Motion Not Detected
- Lower `THRESHOLD_VALUE` in Configuration tab (increase sensitivity)
- Reduce `MIN_CONTOUR_AREA` for smaller movements
- Check lighting conditions
- Ensure camera has clear view of motion area
- Review ROI settings if using regions

### Too Many False Positives
- Increase `THRESHOLD_VALUE` (decrease sensitivity)
- Increase `MIN_CONTOUR_AREA` to filter noise
- Improve lighting to reduce noise
- Avoid pointing camera at reflective surfaces
- Use ROI to exclude problem areas

### No Audio Alerts
- **Windows**: Verify system volume is on
- **Linux/macOS**: Check audio device is available
- Modify `BEEP_FREQUENCY` and `BEEP_DURATION` in config.py
- Ensure PyAudio is properly installed (if using custom audio)

### Snapshots Not Saving
- Verify `snapshots` folder exists and is writable
- Check disk space availability
- Review file permissions on snapshot folder
- Check `SNAPSHOT_FOLDER` path in config.py

### Performance Issues (Low FPS)
- Reduce camera resolution in config settings
- Increase blur kernel size for faster processing
- Reduce monitor window size
- Close other CPU-intensive applications
- Use CLI mode instead of GUI

---

## 📦 Dependencies

All dependencies are in `requirements.txt`:
```
opencv-python==4.8.1.78    # Computer vision
numpy==1.24.3              # Numerical computing
PyQt5==5.15.9              # GUI framework
Pillow==10.0.0             # Image processing
```

---

## 💡 Performance Tips

1. **Use ROI selection** to limit detection area
2. **Adjust blur kernel size** in config for faster processing
3. **Increase MIN_CONTOUR_AREA** to skip small movements
4. **Disable GUI updates** in CLI mode for server use
5. **Use CLI mode** instead of GUI for headless systems

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

## 🎬 Example Use Cases

- **Home Security**: Monitor entry points for intrusions
- **Warehouse Monitoring**: Track movement in storage areas
- **Office Surveillance**: Detect after-hours activity
- **Pet Monitoring**: Watch pets while away
- **Construction Site**: Monitor job sites 24/7
- **Lab Automation**: Trigger actions on motion events

---

**Last Updated**: June 2026
**Author**: Ramesha Akram
**Repository**: https://github.com/RameeshaAkram/Motion-Detection-Alarm-System-
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

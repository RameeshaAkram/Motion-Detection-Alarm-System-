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

---

## 🔐 Security & Privacy

- **Snapshots location**: Default is local `snapshots/` folder
- **Configuration**: Stored in `config.py` on local filesystem
- **No cloud upload**: By default, all data stays local
- **Recording**: System captures snapshots only - no continuous video recording
- **Permissions**: Ensure `snapshots/` folder has write permissions

---

## 📞 FAQ

**Q: Can I use multiple cameras?**
A: Yes! Change `CAMERA_ID` in Configuration tab (0=built-in, 1=external, 2+=additional)

**Q: How many snapshots can I store?**
A: Approximately 500-1000 per 50 MB of storage. Use Snapshots tab to delete old files.

**Q: Can I export video instead of snapshots?**
A: Current version captures snapshots only on motion. For continuous recording, use OpenCV separately.

**Q: What's the maximum monitoring duration?**
A: Unlimited! System runs continuously until manually stopped.

**Q: Does it work on Raspberry Pi?**
A: Yes! Ensure Python 3.7+ and required packages installed.

**Q: Can I use IP cameras?**
A: Yes! If your IP camera supports RTSP, you can use RTSP URL instead of camera ID.

---

## 📋 Version & License

- **Version**: 1.0
- **Python**: 3.7+
- **License**: MIT
- **Author**: Ramesha Akram
- **Last Updated**: June 2026
- **Repository**: https://github.com/RameeshaAkram/Motion-Detection-Alarm-System-

---

## 🚀 Next Steps

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Configure settings**: Edit `config.py` for your environment
3. **Run GUI**: `python run.py`
4. **Set sensitivity**: Use Configuration tab to adjust thresholds
5. **Start monitoring**: Click "Start Monitoring" in Live Feed tab

---

**For detailed GUI documentation, refer to `GUI_DOCUMENTATION.md` and `SETUP_GUIDE.md`**

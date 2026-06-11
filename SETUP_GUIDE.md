# Quick Setup Guide

## Installation (5 minutes)

### Step 1: Verify Python Installation
```bash
python --version
```
Should show Python 3.7 or higher.

### Step 2: Install Dependencies
```bash
cd "w:\Projects\Motion-Detection Alarm System"
pip install -r requirements.txt
```

### Step 3: Run the Application

**GUI Version (Recommended):**
```bash
python run.py
```

**CLI Version (Alternative):**
```bash
python main.py
```

---

## First Time Setup

### Initial Configuration

1. **Open the GUI** (via `python run.py`)
2. **Go to "⚙️ Configuration" tab**
3. **Set Camera ID:**
   - Try `0` first (built-in camera)
   - If no video appears, try `1`, `2`, etc.
   - Click "✓ Apply Settings"

4. **Go to "📹 Live Feed" tab**
5. **Click "▶ Start Monitoring"**
   - Should see live video
   - Move in front of camera
   - Should see "MOTION DETECTED!" and green boxes

### Tuning for Your Environment

**If detecting too little motion:**
- Lower "Sensitivity Threshold" to 15-20
- Check lighting - increase brightness
- Click "✓ Apply Settings"

**If too many false alerts:**
- Raise "Sensitivity Threshold" to 30-40
- Increase "Min Motion Area"
- Click "✓ Apply Settings"

---

## GUI Tabs Explained Simply

### 📹 Live Feed
- **What to see:** Live video from camera
- **What to do:** Click "▶ Start" to begin monitoring
- **Bottom right:** Real-time stats (FPS, snapshots, motion status)

### ⚙️ Configuration
- **What to adjust:** Sensitivity and camera settings
- **Try this:** Drag "Sensitivity" slider while monitoring to see effect
- **Remember:** Some changes require clicking "✓ Apply Settings"

### 📊 Event History
- **What shows up:** List of all motion events with timestamps
- **Useful for:** Reviewing when motion was detected
- **Can export:** Click "💾 Export to CSV" to save as spreadsheet

### 📷 Snapshots
- **What shows:** All captured images from motion events
- **Can delete:** Remove old snapshots to free disk space
- **Can browse:** Click "📂 Open Folder" to see files

### 📖 Help & Docs
- **Full manual:** Complete documentation inside app
- **Troubleshooting:** Solutions for common problems
- **Best practices:** Setup recommendations

---

## Common Issues & Quick Fixes

### "Failed to open camera"
1. Pick different Camera ID: try 1, 2, 3...
2. Restart the app
3. Restart your computer
4. Check no other app is using camera

### No motion detected when there clearly is
1. Lower Sensitivity Threshold (try 15)
2. Lower Min Motion Area (try 300)
3. Increase lighting
4. Make bigger/faster movements

### Too many false alerts
1. Raise Sensitivity Threshold (try 40)
2. Raise Min Motion Area (try 700)
3. Stop near window/lights that are flickering
4. Stabilize camera/tripod

### Video is slow/choppy
1. Close other programs
2. Lower camera resolution in system settings
3. Restart app and computer

---

## Default Settings Explained

```
Camera ID:          0          (Built-in camera)
Sensitivity:        25         (Medium - good for offices)
Min Motion Area:    500        (~3x3 inch area at 1080p)
Beep Frequency:     1000 Hz    (Standard beep tone)
Beep Duration:      500 ms     (Half second alert)
```

These work well for most home/office use.

---

## File Structure

```
Motion-Detection Alarm System/
├── run.py                 👈 Click here to start
├── config.py              (Settings file)
├── gui.py                 (GUI application)
├── motion_detector.py     (Detection engine)
├── alarm.py               (Sound alerts)
├── snapshot_manager.py    (Photo storage)
├── requirements.txt       (Dependencies list)
├── README.md              (Full manual)
└── snapshots/             (Captured photos)
```

---

## Next Steps

1. **Explore the GUI** - Click through each tab
2. **Read the Help** - In the "📖 Help & Docs" tab
3. **Fine-tune settings** - In the "⚙️ Configuration" tab
4. **Review events** - Check "📊 Event History"
5. **Manage snapshots** - Use "📷 Snapshots" tab

---

## Hardware Recommendations

| Spec | Minimum | Recommended |
|------|---------|-------------|
| CPU | Dual-core | Quad-core |
| RAM | 512 MB | 2+ GB |
| Drive | 500 MB free | 10+ GB free |
| Camera | USB or built-in | USB 3.0 webcam |
| OS | Windows/Mac/Linux | Windows 10+ or modern OS |

---

## Troubleshooting Flowchart

```
GUI won't start?
├─ Python installed? → Install Python 3.7+
├─ Dependencies installed? → Run: pip install -r requirements.txt
└─ Try closing other apps → Frees up resources

Video won't show?
├─ Try Camera ID 1, 2, 3... → Different camera
├─ Is camera in use? → Close other video apps
└─ Restart computer → Resets camera drivers

No motion detected?
├─ Lower sensitivity → Drag threshold slider left
├─ Increase lighting → Add lights to area
├─ Move closer → Test with hand near camera
└─ Check Min Area → Lower the value

Too many false alerts?
├─ Raise sensitivity → Drag threshold slider right
├─ Increase Min Area → Set higher value
├─ Stabilize camera → Use tripod
└─ Reduce reflections → Avoid windows/mirrors

Audio not working?
├─ Check volume → Windows volume mixer
├─ Test speakers → Try other audio app
├─ Restart → Reboot computer
└─ System settings → Check audio devices
```

---

## Performance Monitoring

**Check FPS (Frames Per Second):**
- Look at "📹 Live Feed" tab
- "FPS: XX.X" shown in status
- **Good:** 25+ FPS
- **Acceptable:** 20+ FPS
- **Poor:** Below 20 FPS (try closing other apps)

---

## Tips for Best Results

1. **Lighting:** Even, consistent lighting in monitored area
2. **Camera angle:** Clear view of space you're monitoring
3. **Sensitivity:** Start at 25, adjust up/down based on results
4. **Movement:** Larger, faster movements detected better
5. **Background:** Minimize moving curtains, branches, etc.
6. **Position:** Mount camera high, looking down diagonal
7. **Testing:** Test with your hand before full deployment
8. **Regular cleanup:** Delete old snapshots monthly

---

## Getting Help

**In-App:**
- Click "📖 Help & Docs" tab for full documentation
- Scroll down for troubleshooting section
- Configuration examples for different environments

**Files:**
- `README.md` - Full user manual
- `GUI_DOCUMENTATION.md` - Technical details
- `config.py` - All configuration options

---

## System Requirements Verification

Run this to check your setup:
```bash
python -m pip list
```

Should show:
- ✓ opencv-python (4.8.1.78)
- ✓ PyQt5 (5.15.9)
- ✓ numpy (1.24.3)
- ✓ Pillow (10.0.0)

If missing, run:
```bash
pip install -r requirements.txt
```

---

## You're Ready!

1. ✓ Python installed
2. ✓ Dependencies installed
3. ✓ Run: `python run.py`
4. ✓ Click "▶ Start Monitoring"
5. ✓ Watch for motion detection
6. ✓ Explore tabs and features

**Enjoy your Motion Detection Alarm System! 🎉**

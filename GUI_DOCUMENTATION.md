# GUI Code Documentation

## Overview

This document explains the implementation details of the PyQt5-based GUI for the Motion Detection Alarm System.

## File: `gui.py`

### Module Structure

```python
gui.py
├── Imports (PyQt5, OpenCV, threading, etc.)
├── VideoThread (QThread subclass)
│   ├── __init__()
│   ├── run()
│   └── stop()
├── MotionDetectionGUI (QMainWindow subclass)
│   ├── setup_ui()
│   ├── create_live_feed_tab()
│   ├── create_configuration_tab()
│   ├── create_logging_tab()
│   ├── create_snapshots_tab()
│   ├── create_documentation_tab()
│   └── [Event handlers]
└── main() - Entry point
```

### Key Classes

#### 1. **VideoThread**

**Purpose:** Handle video capture and motion detection in a separate thread to prevent UI freezing

**Signals:**
- `frame_captured`: Emits processed frames for display
- `motion_detected`: Emits motion detection events (bool, contours)
- `error_occurred`: Emits error messages
- `stats_updated`: Emits real-time statistics (FPS, frame count, etc.)

**Key Methods:**
- `run()`: Main video loop - continuously captures frames and performs motion detection
- `stop()`: Gracefully stop the thread

**Thread Safety:**
- PyQt5 signals/slots handle thread-safe communication
- GUI thread receives signals from worker thread
- No direct UI manipulation from worker thread

**Implementation Details:**
```python
# In run() method:
1. Initialize camera capture (cv2.VideoCapture)
2. Loop while self.running == True:
   a. Capture frame
   b. Calculate FPS
   c. Perform motion detection
   d. Draw indicators (boxes, text)
   e. Apply cooldown logic (prevent spam)
   f. Emit signals to update GUI
3. Clean up on exit
```

**Motion Detection in Thread:**
```python
# Using existing MotionDetector class
motion_detected, contours = self.detector.detect(frame)

# Apply cooldown mechanism
if motion_detected and self.motion_cooldown <= 0:
    play_beep()  # Emit audio alert
    self.snapshot_manager.save_snapshot(frame)
    self.motion_cooldown = 30  # ~1 second at 30fps
```

#### 2. **MotionDetectionGUI**

**Purpose:** Main application window orchestrating all GUI components

**Inheritance:** `QMainWindow` (PyQt5)

**Key Attributes:**
```python
self.detector              # MotionDetector instance
self.snapshot_manager      # SnapshotManager instance
self.current_config       # Dict of configuration settings
self.is_monitoring        # Bool: monitoring active?
self.video_thread         # VideoThread instance
self.motion_history       # List of motion events with timestamps
```

**Main Methods:**

##### `__init__()`
Initializes GUI components:
- Creates motion detector and snapshot manager
- Sets up configuration dictionary from config.py
- Calls setup_ui()

##### `setup_ui()`
Creates main UI structure:
- Creates QTabWidget
- Adds 5 tabs with different functionality
- Sets window properties (title, geometry)

##### Tab Creation Methods

**`create_live_feed_tab()`**
- Places video display label (800x600)
- Creates start/stop/snapshot buttons
- Creates status panel showing:
  - Motion status
  - FPS indicator
  - Frame counter
  - Snapshot count
  - Monitoring status

**`create_configuration_tab()`**
- Uses QScrollArea for large content
- QGroupBox sections for organization:
  - Camera settings (Camera ID spinbox)
  - Motion detection (Threshold slider, Min Area spinbox)
  - Alert settings (Frequency, Duration spinboxes)
- Action buttons (Apply, Reset)

**`create_logging_tab()`**
- QTableWidget with 4 columns:
  - Timestamp
  - Event Type
  - Details
  - Action (optional)
- Buttons: Clear History, Export to CSV

**`create_snapshots_tab()`**
- Statistics label showing total count
- QTableWidget listing snapshots:
  - Filename
  - File size
  - Date modified
- Buttons: Refresh, Open Folder, Delete Old

**`create_documentation_tab()`**
- QTextEdit with markdown-formatted help text
- Covers all tabs, settings, troubleshooting
- Read-only for user reference

##### Event Handlers

**`start_monitoring()`**
- Validates no monitoring already running
- Updates button states
- Creates and starts VideoThread
- Connects thread signals to slots
- Logs event

**`stop_monitoring()`**
- Stops VideoThread
- Updates status indicators
- Cleans up resources

**`update_video_frame(frame)`** [Slot]
- Receives frame from VideoThread signal
- Converts BGR → RGB
- Resizes to label size (800x600)
- Converts to QImage and QPixmap
- Displays in video_label

**`on_motion_detected(motion, contours)`** [Slot]
- Updates motion_status_label color
- Logs motion event with timestamp

**`update_stats(stats)`** [Slot]
- Updates FPS, frame count, snapshot count displays

**`on_video_error(error_msg)`** [Slot]
- Shows error dialog
- Stops monitoring if running

**`take_manual_snapshot()`**
- Captures current frame from video thread
- Saves using snapshot_manager
- Shows success dialog

**`apply_configuration()`**
- Reads values from UI widgets
- Updates self.current_config dictionary
- Logs event
- Shows dialog if restart needed

**`reset_configuration()`**
- Sets all UI widgets to default values
- Uses values from config.py

**`log_event(event_type, details)`**
- Adds row to event history table
- Captures timestamp
- Scrolls table to show newest event

**`export_event_history()`**
- QFileDialog to select save location
- Exports all table rows to CSV file
- Handles exceptions

**`clear_event_history()`**
- Confirms with user
- Clears all rows from table

**`refresh_snapshots_list()`**
- Scans snapshots folder
- Updates table with file listing
- Shows file size and modification date
- Limits display to last 100 snapshots

**`open_snapshots_folder()`**
- Cross-platform file explorer open:
  - Windows: `os.startfile()`
  - macOS: `open` command
  - Linux: `xdg-open` command

**`delete_old_snapshots()`**
- Calculates 7-day cutoff date
- Deletes snapshots older than cutoff
- Refreshes list display
- Shows count of deleted files

**`closeEvent(event)`**
- Checks if monitoring active
- Prompts user to stop before exit
- Ensures proper cleanup

### Signal/Slot Architecture

```
VideoThread (Worker)
    |
    ├─→ frame_captured signal ─→ update_video_frame() slot
    ├─→ motion_detected signal ─→ on_motion_detected() slot
    ├─→ stats_updated signal ──→ update_stats() slot
    └─→ error_occurred signal ──→ on_video_error() slot

User Actions (GUI clicks)
    |
    ├─→ start_button ──────→ start_monitoring()
    ├─→ stop_button ───────→ stop_monitoring()
    ├─→ snapshot_button ───→ take_manual_snapshot()
    ├─→ apply_config_button → apply_configuration()
    ├─→ reset_config_button → reset_configuration()
    ├─→ clear_logs_button ──→ clear_event_history()
    ├─→ export_logs_button ─→ export_event_history()
    ├─→ refresh_snap_button → refresh_snapshots_list()
    ├─→ open_folder_button ─→ open_snapshots_folder()
    └─→ delete_old_button ──→ delete_old_snapshots()
```

### Threading Model

```
Main Thread (GUI)
    ├─ Handles user input (button clicks, etc.)
    ├─ Renders UI updates
    └─ Creates VideoThread when monitoring starts

VideoThread (Worker)
    ├─ Continuous frame capture loop
    ├─ Motion detection algorithm
    ├─ Emits signals (thread-safe)
    └─ GUI updates via signals, not direct calls
```

**Why Threading?**
- Prevents UI freeze during video processing
- Allows smooth button interaction
- Enables responsive GUI while detecting motion

### Data Flow

```
1. User clicks "Start Monitoring"
   ↓
2. start_monitoring() creates VideoThread
   ↓
3. VideoThread.run() loop starts
   ├─ Captures frame from camera
   ├─ Preprocesses (grayscale, blur)
   ├─ Calls detector.detect(frame)
   ├─ Draws bounding boxes/text
   ├─ Emits frame_captured signal
   ↓
4. Main thread receives signals
   ├─ Displays frame via update_video_frame()
   ├─ Updates stats via update_stats()
   ├─ Handles motion via on_motion_detected()
   ↓
5. User can see live video and stats in real-time
   ↓
6. User clicks "Stop Monitoring" or closes app
   ├─ stop_monitoring() called
   ├─ VideoThread.running = False
   ├─ Thread exits loop and cleans up
   ↓
7. Application continues or exits
```

### UI Components Reference

| Component | Type | Purpose |
|-----------|------|---------|
| `video_label` | QLabel | Display video frames |
| `start_button` | QPushButton | Start monitoring |
| `stop_button` | QPushButton | Stop monitoring |
| `snapshot_button` | QPushButton | Manual snapshot |
| `motion_status_label` | QLabel | Show motion status |
| `fps_label` | QLabel | Display FPS |
| `frame_label` | QLabel | Frame counter |
| `snap_count_label` | QLabel | Snapshot counter |
| `monitoring_status_label` | QLabel | Monitoring state |
| `camera_id_spinbox` | QSpinBox | Select camera |
| `threshold_slider` | QSlider | Set sensitivity |
| `threshold_value_label` | QLabel | Show threshold value |
| `contour_spinbox` | QSpinBox | Min area setting |
| `freq_spinbox` | QSpinBox | Beep frequency |
| `duration_spinbox` | QSpinBox | Beep duration |
| `apply_config_button` | QPushButton | Save settings |
| `reset_config_button` | QPushButton | Reset to defaults |
| `event_table` | QTableWidget | Event logging |
| `clear_logs_button` | QPushButton | Clear history |
| `export_logs_button` | QPushButton | Export to CSV |
| `snapshots_list_table` | QTableWidget | Snapshot listing |
| `refresh_snapshots_button` | QPushButton | Refresh list |
| `open_folder_button` | QPushButton | Browse folder |
| `delete_old_button` | QPushButton | Delete old files |
| `snapshot_stats_label` | QLabel | Snapshot statistics |

### Styling

**Buttons:**
- Start: Green (#4CAF50)
- Stop: Red (#f44336)
- Snapshot: Blue (#2196F3)
- Apply: Green
- Reset: Orange (#FF9800)
- Others: Gray (default)

**Labels:**
- Active motion: Red (#f44336)
- Inactive: Gray (#666)
- Monitoring active: Green (#4CAF50)
- Monitoring stopped: Red

**Frames:**
- Status panel: Light gray (#f5f5f5)
- Video area: Black with border

### Configuration Management

**Current Config Dictionary:**
```python
self.current_config = {
    'CAMERA_ID': config.CAMERA_ID,
    'BLUR_KERNEL_SIZE': config.BLUR_KERNEL_SIZE,
    'THRESHOLD_VALUE': config.THRESHOLD_VALUE,
    'MIN_CONTOUR_AREA': config.MIN_CONTOUR_AREA,
    'BEEP_FREQUENCY': config.BEEP_FREQUENCY,
    'BEEP_DURATION': config.BEEP_DURATION,
}
```

**Loading Defaults:**
- Read from config.py module on startup
- Displayed in UI widgets

**Applying Changes:**
- Read from UI widgets in apply_configuration()
- Update self.current_config
- For camera changes: requires restart
- For sensitivity changes: takes effect on next frame

### Error Handling

**Camera Errors:**
```python
# In VideoThread.run()
try:
    self.cap = cv2.VideoCapture(...)
    if not self.cap.isOpened():
        self.error_occurred.emit("Failed to open camera...")
except Exception as e:
    self.error_occurred.emit(f"Error in video thread: {str(e)}")
```

**File Errors:**
```python
# In export_event_history()
try:
    with open(file_path, 'w') as f:
        # Write CSV data
except Exception as e:
    QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
```

### Performance Considerations

1. **Frame Processing:**
   - Each frame processed in VideoThread
   - FPS calculated every second
   - Large contours array managed efficiently

2. **GUI Updates:**
   - Frame display updated via signals
   - Stats updated every frame
   - No blocking operations in main thread

3. **Memory Management:**
   - Event table limited to ~1000 rows
   - Snapshots limited to ~100 files shown
   - Old snapshots can be deleted

4. **CPU Usage:**
   - 1 thread for video processing
   - Main thread handles UI
   - FPS indicator shows performance

### Testing Recommendations

1. **Basic Functionality:**
   - Test start/stop button
   - Verify video display
   - Check motion detection with hand movement

2. **Configuration:**
   - Test each slider/spinbox
   - Apply settings and verify changes take effect
   - Reset and verify defaults

3. **Event Logging:**
   - Generate motion events
   - Verify logging
   - Export and check CSV format

4. **Snapshots:**
   - Take manual snapshots
   - Verify automatic snapshots on motion
   - Test refresh and delete functions

5. **Error Handling:**
   - Unplug camera (should show error)
   - Close window while monitoring (should prompt)
   - Test with invalid settings

### Future Enhancements

- Video recording capability
- Motion detection heatmap
- Advanced analytics (daily patterns)
- Cloud integration
- Multi-camera support UI
- Motion zones (detection areas)
- Custom alert sounds
- Dark mode theme
- Sound level visualization
- Motion replay

---

## Dependencies Explained

- **PyQt5**: GUI framework - provides widgets and main window
- **cv2 (OpenCV)**: Video capture and image processing
- **numpy**: Array operations for image processing
- **PIL/Pillow**: Image file handling
- **threading**: Python's threading module for VideoThread
- **datetime**: Timestamp generation
- **pathlib**: Cross-platform file path handling
- **os**: File operations and system commands

---

## Integration with Core Modules

**motion_detector.py**
- Imported: `from motion_detector import MotionDetector`
- Used in: VideoThread.run() to detect motion
- Method called: `detector.detect(frame)` returns (bool, contours)

**alarm.py**
- Imported: `from alarm import play_beep`
- Used in: VideoThread.run() on motion detection
- Called with: `play_beep(frequency, duration)`

**snapshot_manager.py**
- Imported: `from snapshot_manager import SnapshotManager`
- Used in: VideoThread and GUI for snapshot operations
- Methods called:
  - `save_snapshot(frame)` - saves captured frame
  - `get_snapshot_count()` - returns snapshot count

**config.py**
- Imported: `import config`
- Used in: MotionDetectionGUI.__init__() to load defaults
- Values accessed: All configuration constants

**utils.py**
- Imported: `from utils import preprocess_frame`
- Used in: (Currently not used in GUI, functions available if needed)

---

## Code Documentation Standards

All functions and classes include docstrings:
```python
def function_name(param):
    """
    Short description.
    
    Longer description if needed.
    
    Args:
        param (type): Description
        
    Returns:
        type: Description
        
    Example:
        >>> result = function_name("value")
        >>> print(result)
    """
```

All complex logic includes inline comments explaining the "why"

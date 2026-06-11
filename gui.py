"""
Motion Detection Alarm System - GUI Application
===============================================

This module provides a comprehensive PyQt5-based graphical user interface for the
Motion Detection Alarm System. It offers real-time video monitoring, configuration
controls, event logging, and detailed documentation.

Features:
- Live video feed with motion detection overlay
- Real-time motion status and alerts
- Configuration panel for tuning sensitivity
- Event history with timestamps
- Snapshot gallery management
- Built-in documentation and help system

Author: Motion Detection System
Date: 2026
"""

import sys
import cv2
import threading
import os
import numpy as np
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QSpinBox, QDoubleSpinBox, QCheckBox,
    QComboBox, QTextEdit, QTableWidget, QTableWidgetItem, QScrollArea,
    QGridLayout, QGroupBox, QFileDialog, QMessageBox, QProgressBar, QFrame
)
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize, QPointF

import config
from motion_detector import MotionDetector
from alarm import play_beep
from snapshot_manager import SnapshotManager
from utils import preprocess_frame


class VideoDisplayLabel(QLabel):
    """Clickable video label used for ROI selection."""

    mousePressed = pyqtSignal(int, int)
    mouseMoved = pyqtSignal(int, int)
    mouseReleased = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            self.mousePressed.emit(pos.x(), pos.y())

    def mouseMoveEvent(self, event):
        pos = event.pos()
        self.mouseMoved.emit(pos.x(), pos.y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            self.mouseReleased.emit(pos.x(), pos.y())


class ROIManager:
    """Stores and renders the optional region of interest used for motion detection."""

    def __init__(self, display_width=800, display_height=600):
        self.display_width = display_width
        self.display_height = display_height
        self.roi = None
        self.selecting = False
        self.start_point = None
        self.current_point = None

    def start_roi_selection(self):
        """Enable ROI selection mode."""
        self.selecting = True
        self.start_point = None
        self.current_point = None

    def cancel_roi(self):
        """Clear ROI and return to full frame."""
        self.roi = None
        self.selecting = False
        self.start_point = None
        self.current_point = None

    def begin_selection(self, point):
        if not self.selecting:
            return
        self.start_point = point
        self.current_point = point

    def update_selection(self, point):
        if not self.selecting or self.start_point is None:
            return
        self.current_point = point

    def finish_selection(self, point):
        if not self.selecting or self.start_point is None:
            return False

        self.current_point = point
        x1, y1 = self.start_point
        x2, y2 = self.current_point

        left = max(0, min(x1, x2))
        right = min(self.display_width, max(x1, x2))
        top = max(0, min(y1, y2))
        bottom = min(self.display_height, max(y1, y2))

        if abs(right - left) < 10 or abs(bottom - top) < 10:
            self.cancel_roi()
            return False

        self.roi = (left, top, right, bottom)
        self.selecting = False
        self.start_point = None
        self.current_point = None
        return True

    def get_mask(self, frame_shape):
        """Return a binary mask for the active ROI, or None for full-frame detection."""
        if self.roi is None:
            return None

        height, width = frame_shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)

        scale_x = width / float(self.display_width)
        scale_y = height / float(self.display_height)

        x1, y1, x2, y2 = self.roi
        left = int(round(x1 * scale_x))
        right = int(round(x2 * scale_x))
        top = int(round(y1 * scale_y))
        bottom = int(round(y2 * scale_y))

        cv2.rectangle(mask, (left, top), (right, bottom), 255, -1)
        return mask

    def draw_on_frame(self, frame):
        """Draw ROI feedback on a display frame."""
        if self.roi is not None:
            x1, y1, x2, y2 = self.roi
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, "ROI ACTIVE", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        else:
            cv2.putText(frame, "FULL FRAME", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if self.selecting and self.start_point is not None and self.current_point is not None:
            x1, y1 = self.start_point
            x2, y2 = self.current_point
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, "SELECT ROI", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        return frame


class VideoThread(QThread):
    """
    Worker thread for capturing and processing video frames.
    
    This thread runs independently to avoid blocking the GUI.
    It continuously captures frames, performs motion detection,
    and emits signals to update the GUI with real-time data.
    
    Signals:
        frame_captured: Emits processed frame for display
        motion_detected: Emits motion detection event
        error_occurred: Emits error messages
    """
    
    frame_captured = pyqtSignal(object)
    motion_detected = pyqtSignal(bool, list)
    error_occurred = pyqtSignal(str)
    stats_updated = pyqtSignal(dict)
    
    def __init__(self, detector, snapshot_manager, config_dict, roi_manager=None):
        """
        Initialize the video thread.
        
        Args:
            detector (MotionDetector): Motion detector instance
            snapshot_manager (SnapshotManager): Snapshot manager instance
            config_dict (dict): Current configuration settings
        """
        super().__init__()
        self.detector = detector
        self.snapshot_manager = snapshot_manager
        self.config_dict = config_dict
        self.roi_manager = roi_manager
        self.cap = None
        self.running = False
        self.motion_cooldown = 0
        self.frame_count = 0
        self.fps = 0
        
    def run(self):
        """Main video capture and processing loop."""
        try:
            self.cap = cv2.VideoCapture(self.config_dict['CAMERA_ID'])
            if not self.cap.isOpened():
                self.error_occurred.emit("Failed to open camera. Check camera ID in settings.")
                return
            
            self.running = True
            fps_timer_frame = 0
            fps_timer_start = datetime.now()
            
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    self.error_occurred.emit("Failed to capture frame from camera.")
                    break
                
                self.frame_count += 1
                
                # Calculate FPS
                fps_timer_frame += 1
                elapsed = (datetime.now() - fps_timer_start).total_seconds()
                if elapsed >= 1.0:
                    self.fps = fps_timer_frame / elapsed
                    fps_timer_frame = 0
                    fps_timer_start = datetime.now()
                
                # Perform motion detection
                roi_mask = self.roi_manager.get_mask(frame.shape) if self.roi_manager else None
                motion_detected, contours = self.detector.detect(frame, roi_mask=roi_mask)
                
                # Draw motion indicators
                display_frame = frame.copy()
                if motion_detected:
                    cv2.putText(display_frame, "MOTION DETECTED!", (20, 40),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
                    for contour in contours:
                        x, y, w, h = cv2.boundingRect(contour)
                        cv2.rectangle(display_frame, (x, y), (x + w, y + h),
                                    (0, 255, 0), 2)
                
                # Handle motion alerts with cooldown
                if motion_detected and self.motion_cooldown <= 0:
                    play_beep(self.config_dict['BEEP_FREQUENCY'],
                            self.config_dict['BEEP_DURATION'])
                    self.snapshot_manager.save_snapshot(frame)
                    self.motion_cooldown = 30
                
                if self.motion_cooldown > 0:
                    self.motion_cooldown -= 1
                
                # Add stats
                cv2.putText(display_frame, f"FPS: {self.fps:.1f}", (20, 70),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                cv2.putText(display_frame, f"Snapshots: {self.snapshot_manager.get_snapshot_count()}",
                          (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                # Emit signals
                self.frame_captured.emit(display_frame)
                self.motion_detected.emit(motion_detected, contours)
                self.stats_updated.emit({
                    'fps': self.fps,
                    'frame_count': self.frame_count,
                    'motion': motion_detected,
                    'snapshot_count': self.snapshot_manager.get_snapshot_count()
                })
                
        except Exception as e:
            self.error_occurred.emit(f"Error in video thread: {str(e)}")
        finally:
            if self.cap:
                self.cap.release()
    
    def stop(self):
        """Stop the video thread gracefully."""
        self.running = False
        self.wait()


class MotionDetectionGUI(QMainWindow):
    """
    Main GUI Application for Motion Detection Alarm System.
    
    This is the primary window that orchestrates all GUI components including:
    - Real-time video display
    - Configuration management
    - Event logging
    - Snapshot management
    - Documentation
    """
    
    def __init__(self):
        """Initialize the GUI application."""
        super().__init__()
        self.setWindowTitle("Motion Detection Alarm System - Professional Monitor")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize components
        self.detector = MotionDetector()
        self.snapshot_manager = SnapshotManager()
        self.roi_manager = ROIManager()
        self.current_config = {
            'CAMERA_ID': config.CAMERA_ID,
            'BLUR_KERNEL_SIZE': config.BLUR_KERNEL_SIZE,
            'THRESHOLD_VALUE': config.THRESHOLD_VALUE,
            'MIN_CONTOUR_AREA': config.MIN_CONTOUR_AREA,
            'BEEP_FREQUENCY': config.BEEP_FREQUENCY,
            'BEEP_DURATION': config.BEEP_DURATION,
        }
        
        # State variables
        self.is_monitoring = False
        self.video_thread = None
        self.motion_history = []
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main user interface with tabs."""
        # Create central widget with tab structure
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Create tabs
        self.tabs.addTab(self.create_live_feed_tab(), "📹 Live Feed")
        self.tabs.addTab(self.create_configuration_tab(), "⚙️ Configuration")
        self.tabs.addTab(self.create_logging_tab(), "📊 Event History")
        self.tabs.addTab(self.create_snapshots_tab(), "📷 Snapshots")
        self.tabs.addTab(self.create_documentation_tab(), "📖 Help & Docs")
        
    def create_live_feed_tab(self):
        """
        Create the Live Feed tab showing real-time video.
        
        Components:
        - Video display area
        - Motion status indicator
        - Control buttons (Start/Stop)
        - Real-time statistics
        
        Returns:
            QWidget: Configured live feed tab
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title_label = QLabel("Live Motion Detection Feed")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Main content area
        content_layout = QHBoxLayout()
        
        # Video display (left side)
        video_layout = QVBoxLayout()
        self.video_label = VideoDisplayLabel()
        self.video_label.setFixedSize(800, 600)
        self.video_label.setStyleSheet("border: 2px solid #333; background-color: #000;")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.mousePressed.connect(self.on_video_mouse_pressed)
        self.video_label.mouseMoved.connect(self.on_video_mouse_moved)
        self.video_label.mouseReleased.connect(self.on_video_mouse_released)
        video_layout.addWidget(self.video_label)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("▶ Start Monitoring")
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.start_button.clicked.connect(self.start_monitoring)
        
        self.stop_button = QPushButton("⏹ Stop Monitoring")
        self.stop_button.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 10px;")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_monitoring)
        
        self.snapshot_button = QPushButton("📸 Manual Snapshot")
        self.snapshot_button.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 10px;")
        self.snapshot_button.clicked.connect(self.take_manual_snapshot)

        self.select_roi_button = QPushButton("⬚ Select ROI")
        self.select_roi_button.setStyleSheet("background-color: #3F51B5; color: white; font-weight: bold; padding: 10px;")
        self.select_roi_button.clicked.connect(self.start_roi_selection)

        self.cancel_roi_button = QPushButton("✕ Full Frame")
        self.cancel_roi_button.setStyleSheet("background-color: #607D8B; color: white; font-weight: bold; padding: 10px;")
        self.cancel_roi_button.clicked.connect(self.cancel_roi)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.snapshot_button)
        button_layout.addWidget(self.select_roi_button)
        button_layout.addWidget(self.cancel_roi_button)
        video_layout.addLayout(button_layout)
        
        content_layout.addLayout(video_layout, 3)
        
        # Statistics panel (right side)
        stats_layout = QVBoxLayout()
        
        stats_label = QLabel("System Status")
        stats_font = QFont()
        stats_font.setBold(True)
        stats_label.setFont(stats_font)
        stats_layout.addWidget(stats_label)
        
        # Status boxes
        self.status_frame = QFrame()
        self.status_frame.setStyleSheet("background-color: #f5f5f5; border-radius: 5px; padding: 15px;")
        status_inner_layout = QVBoxLayout(self.status_frame)
        
        # Motion status
        self.motion_status_label = QLabel("🔴 No Motion")
        self.motion_status_label.setStyleSheet("color: #666; font-size: 12pt;")
        status_inner_layout.addWidget(self.motion_status_label)
        
        # FPS indicator
        self.fps_label = QLabel("FPS: --")
        self.fps_label.setStyleSheet("color: #666; font-size: 11pt;")
        status_inner_layout.addWidget(self.fps_label)
        
        # Frame count
        self.frame_label = QLabel("Frames: 0")
        self.frame_label.setStyleSheet("color: #666; font-size: 11pt;")
        status_inner_layout.addWidget(self.frame_label)
        
        # Snapshot count
        self.snap_count_label = QLabel("Snapshots: 0")
        self.snap_count_label.setStyleSheet("color: #666; font-size: 11pt;")
        status_inner_layout.addWidget(self.snap_count_label)
        
        # Monitoring status
        self.monitoring_status_label = QLabel("Status: Stopped")
        self.monitoring_status_label.setStyleSheet("color: #f44336; font-size: 11pt; font-weight: bold;")
        status_inner_layout.addWidget(self.monitoring_status_label)
        
        stats_layout.addWidget(self.status_frame)
        stats_layout.addStretch()
        
        content_layout.addLayout(stats_layout, 1)
        layout.addLayout(content_layout)
        
        return widget
    
    def create_configuration_tab(self):
        """
        Create the Configuration tab for adjusting system parameters.
        
        Components:
        - Camera selection
        - Motion detection sensitivity sliders
        - Beep settings
        - Min contour area
        - Apply/Reset buttons
        
        Returns:
            QWidget: Configured settings tab
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title_label = QLabel("System Configuration")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Camera Selection
        camera_group = QGroupBox("Camera Settings")
        camera_layout = QVBoxLayout()
        camera_layout.addWidget(QLabel("Camera ID (0=Built-in, 1=External):"))
        self.camera_id_spinbox = QSpinBox()
        self.camera_id_spinbox.setValue(self.current_config['CAMERA_ID'])
        self.camera_id_spinbox.setMinimum(0)
        self.camera_id_spinbox.setMaximum(10)
        camera_layout.addWidget(self.camera_id_spinbox)
        camera_group.setLayout(camera_layout)
        scroll_layout.addWidget(camera_group)
        
        # Motion Detection Settings
        motion_group = QGroupBox("Motion Detection")
        motion_layout = QGridLayout()
        
        # Threshold
        motion_layout.addWidget(QLabel("Sensitivity Threshold:"), 0, 0)
        motion_layout.addWidget(QLabel("(Lower = More Sensitive)"), 0, 1)
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setMinimum(5)
        self.threshold_slider.setMaximum(100)
        self.threshold_slider.setValue(self.current_config['THRESHOLD_VALUE'])
        self.threshold_value_label = QLabel(str(self.current_config['THRESHOLD_VALUE']))
        self.threshold_slider.valueChanged.connect(
            lambda v: self.threshold_value_label.setText(str(v))
        )
        motion_layout.addWidget(self.threshold_slider, 1, 0)
        motion_layout.addWidget(self.threshold_value_label, 1, 1)
        
        # Min Contour Area
        motion_layout.addWidget(QLabel("Min Motion Area (pixels²):"), 2, 0)
        self.contour_spinbox = QSpinBox()
        self.contour_spinbox.setValue(self.current_config['MIN_CONTOUR_AREA'])
        self.contour_spinbox.setMinimum(100)
        self.contour_spinbox.setMaximum(10000)
        self.contour_spinbox.setSingleStep(100)
        motion_layout.addWidget(self.contour_spinbox, 2, 1)
        
        motion_group.setLayout(motion_layout)
        scroll_layout.addWidget(motion_group)
        
        # Alert Settings
        alert_group = QGroupBox("Alert Settings")
        alert_layout = QGridLayout()
        
        # Beep Frequency
        alert_layout.addWidget(QLabel("Beep Frequency (Hz):"), 0, 0)
        self.freq_spinbox = QSpinBox()
        self.freq_spinbox.setValue(self.current_config['BEEP_FREQUENCY'])
        self.freq_spinbox.setMinimum(100)
        self.freq_spinbox.setMaximum(5000)
        self.freq_spinbox.setSingleStep(100)
        alert_layout.addWidget(self.freq_spinbox, 0, 1)
        
        # Beep Duration
        alert_layout.addWidget(QLabel("Beep Duration (ms):"), 1, 0)
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setValue(self.current_config['BEEP_DURATION'])
        self.duration_spinbox.setMinimum(100)
        self.duration_spinbox.setMaximum(2000)
        self.duration_spinbox.setSingleStep(100)
        alert_layout.addWidget(self.duration_spinbox, 1, 1)
        
        alert_group.setLayout(alert_layout)
        scroll_layout.addWidget(alert_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.apply_config_button = QPushButton("✓ Apply Settings")
        self.apply_config_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.apply_config_button.clicked.connect(self.apply_configuration)
        
        self.reset_config_button = QPushButton("↻ Reset to Defaults")
        self.reset_config_button.setStyleSheet("background-color: #FF9800; color: white; padding: 10px;")
        self.reset_config_button.clicked.connect(self.reset_configuration)
        
        button_layout.addWidget(self.apply_config_button)
        button_layout.addWidget(self.reset_config_button)
        
        scroll_layout.addLayout(button_layout)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        return widget
    
    def create_logging_tab(self):
        """
        Create the Event History/Logging tab.
        
        Displays all motion detection events with timestamps
        and detailed information.
        
        Returns:
            QWidget: Configured logging tab
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title_label = QLabel("Motion Detection Event History")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Event table
        self.event_table = QTableWidget()
        self.event_table.setColumnCount(4)
        self.event_table.setHorizontalHeaderLabels(["Timestamp", "Event Type", "Details", "Action"])
        self.event_table.setColumnWidth(0, 180)
        self.event_table.setColumnWidth(1, 150)
        self.event_table.setColumnWidth(2, 400)
        layout.addWidget(self.event_table)
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.clear_logs_button = QPushButton("🗑️ Clear History")
        self.clear_logs_button.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        self.clear_logs_button.clicked.connect(self.clear_event_history)
        
        self.export_logs_button = QPushButton("💾 Export to CSV")
        self.export_logs_button.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        self.export_logs_button.clicked.connect(self.export_event_history)
        
        button_layout.addWidget(self.clear_logs_button)
        button_layout.addWidget(self.export_logs_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        return widget
    
    def create_snapshots_tab(self):
        """
        Create the Snapshots tab for managing captured images.
        
        Returns:
            QWidget: Configured snapshots tab
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title_label = QLabel("Snapshot Management")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Stats
        stats_layout = QHBoxLayout()
        self.snapshot_stats_label = QLabel("Total Snapshots: 0 | Folder: snapshots/")
        stats_layout.addWidget(self.snapshot_stats_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        # Snapshot display area
        self.snapshots_list_table = QTableWidget()
        self.snapshots_list_table.setColumnCount(3)
        self.snapshots_list_table.setHorizontalHeaderLabels(["Filename", "Size", "Date Modified"])
        self.snapshots_list_table.setColumnWidth(0, 300)
        self.snapshots_list_table.setColumnWidth(1, 100)
        layout.addWidget(self.snapshots_list_table)
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.refresh_snapshots_button = QPushButton("🔄 Refresh")
        self.refresh_snapshots_button.clicked.connect(self.refresh_snapshots_list)
        
        self.open_folder_button = QPushButton("📂 Open Folder")
        self.open_folder_button.clicked.connect(self.open_snapshots_folder)
        
        self.delete_old_button = QPushButton("🗑️ Delete Old Snapshots")
        self.delete_old_button.clicked.connect(self.delete_old_snapshots)
        
        button_layout.addWidget(self.refresh_snapshots_button)
        button_layout.addWidget(self.open_folder_button)
        button_layout.addWidget(self.delete_old_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Refresh on startup
        self.refresh_snapshots_list()
        
        return widget
    
    def create_documentation_tab(self):
        """
        Create the Help & Documentation tab with comprehensive system information.
        
        Returns:
            QWidget: Configured documentation tab
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title_label = QLabel("Help & Documentation")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Documentation text
        doc_text = QTextEdit()
        doc_text.setReadOnly(True)
        doc_text.setMarkdown("""
# Motion Detection Alarm System - Documentation

## Overview
This application monitors your camera feed in real-time to detect motion and trigger audio alerts when motion is detected.

## System Components

### 1. **Live Feed Tab**
- **Video Display**: Shows real-time video from your camera
- **Motion Indicator**: Red text "MOTION DETECTED!" appears when motion is detected
- **Bounding Boxes**: Green rectangles highlight areas where motion was detected
- **Start/Stop Button**: Control the monitoring system
- **Manual Snapshot**: Capture a frame manually

**Real-time Statistics**:
- FPS (Frames Per Second): Shows camera capture rate
- Frame Count: Total frames processed
- Motion Status: Current motion detection state
- Snapshot Count: Total captured snapshots

### 2. **Configuration Tab**
Adjust system parameters to fine-tune motion detection:

- **Camera ID**: Select which camera to use (0=built-in, 1=external)
- **Sensitivity Threshold**: Lower values = more sensitive to motion (range: 5-100)
  - *Recommendation*: 20-30 for normal office/home environments
  - *Sensitive*: 10-15 for low-light or minimal motion detection
  - *Less Sensitive*: 40-60 to reduce false positives
- **Min Motion Area**: Minimum pixel area required to trigger alert (default: 500)
- **Beep Frequency**: Audio frequency of alert in Hz (default: 1000)
- **Beep Duration**: How long the alert sounds in milliseconds (default: 500)

### 3. **Event History Tab**
Comprehensive logging of all motion detection events:
- Timestamp of each event
- Event type (Motion Detected, Manual Snapshot, etc.)
- Details about the detection
- Export capability to CSV for analysis

**Features**:
- Clear History: Delete all logged events
- Export to CSV: Save event logs for external analysis

### 4. **Snapshots Tab**
Manage captured images from motion detection events:
- View all captured snapshots with metadata
- File size and modification date information
- Refresh list to see new snapshots
- Open folder to browse with file explorer
- Delete old snapshots to free disk space

### 5. **Help & Documentation Tab**
This page containing system information and usage guidelines.

## How Motion Detection Works

1. **Frame Capture**: System continuously captures frames from your camera
2. **Preprocessing**: Frame converted to grayscale and blurred to reduce noise
3. **Comparison**: Current frame compared to previous frame to detect changes
4. **Contour Detection**: Changed areas (motion) identified using edge detection
5. **Filtering**: Small changes filtered out based on Min Motion Area setting
6. **Alert Trigger**: If motion area exceeds threshold:
   - → Audio beep is played
   - → Snapshot is saved
   - → Bounding box displayed on video
   - → Event logged with timestamp

## Best Practices

### Optimal Configuration
- **Indoor Office**: Threshold=25, Min Area=500
- **Home Security**: Threshold=20, Min Area=400
- **Warehouse**: Threshold=30, Min Area=800
- **Dark/Low-Light**: Threshold=15, Min Area=300

### Tips for Better Detection
1. **Lighting**: Ensure adequate, consistent lighting
2. **Camera Placement**: Mount camera with clear view of monitored area
3. **Background Motion**: Minimize trees/curtains (wind sensitive objects)
4. **Angle**: Avoid direct sunlight/reflections in lens
5. **Calibration**: Test different threshold values for your environment

### Performance Optimization
- Close other applications using camera
- Ensure good CPU availability
- Use lower camera resolution if running on older machines
- Monitor FPS indicator (should be 25+ for consistent detection)

## Troubleshooting

### Camera Not Opening
- **Problem**: "Failed to open camera" error
- **Solution**: 
  - Check Camera ID in Configuration (try 0, 1, 2...)
  - Ensure camera is not used by another application
  - Restart application

### No Motion Detected
- **Problem**: Motion not triggering alerts
- **Solution**:
  - Lower Sensitivity Threshold value
  - Increase lighting in monitored area
  - Check Min Motion Area isn't too high
  - Verify camera is properly positioned

### False Positives (Too Many Alerts)
- **Problem**: Alerts triggered by non-motion
- **Solution**:
  - Increase Sensitivity Threshold value
  - Increase Min Motion Area value
  - Reduce camera sensitivity in lighting
  - Minimize background motion sources

### Low FPS
- **Problem**: Slow video playback
- **Solution**:
  - Close other applications
  - Lower monitor refresh rate
  - Use lower camera resolution
  - Reduce GUI update frequency

## Technical Details

### Motion Detection Algorithm
- **Method**: Frame differencing with adaptive thresholding
- **Preprocessing**: Gaussian blur (kernel 5x5) to reduce noise
- **Comparison**: Binary subtraction between sequential frames
- **Threshold**: Pixel intensity change must exceed configurable value
- **Filtering**: Contours with area < Min Motion Area are ignored

### File Structure
- `snapshots/`: Directory where captured frames are stored
- Filenames: Timestamp-based (e.g., `snapshot_2026_04_04_143025_123.jpg`)
- Event logs: Stored in memory (can be exported to CSV)

## System Requirements

- **Python**: 3.7+
- **Dependencies**: opencv-python, numpy, PyQt5, Pillow
- **Camera**: Any USB or built-in camera
- **RAM**: 512 MB minimum
- **CPU**: Dual-core processor recommended
- **Storage**: ~100 MB for application, ~50 MB per 1000 snapshots

## Keyboard Shortcuts
- `Q`: Quit application
- `S`: Save manual snapshot (in CLI mode)

## Contact & Support
For issues or questions, check the Configuration and Event History tabs for diagnostics.
        """)
        layout.addWidget(doc_text)
        
        return widget
    
    # ==================== EVENT HANDLERS ====================
    
    def start_monitoring(self):
        """Start the motion detection monitoring system."""
        if self.is_monitoring:
            QMessageBox.warning(self, "Already Running", "Monitoring is already active!")
            return
        
        self.is_monitoring = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.monitoring_status_label.setText("Status: 🟢 Monitoring Active")
        self.monitoring_status_label.setStyleSheet("color: #4CAF50; font-size: 11pt; font-weight: bold;")
        
        # Create and start video thread
        self.video_thread = VideoThread(self.detector, self.snapshot_manager, self.current_config, self.roi_manager)
        self.video_thread.frame_captured.connect(self.update_video_frame)
        self.video_thread.motion_detected.connect(self.on_motion_detected)
        self.video_thread.stats_updated.connect(self.update_stats)
        self.video_thread.error_occurred.connect(self.on_video_error)
        self.video_thread.start()
        
        self.log_event("System Started", "Monitoring system activated")
    
    def stop_monitoring(self):
        """Stop the motion detection monitoring system."""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.monitoring_status_label.setText("Status: 🔴 Monitoring Stopped")
        self.monitoring_status_label.setStyleSheet("color: #f44336; font-size: 11pt; font-weight: bold;")
        
        if self.video_thread:
            self.video_thread.stop()
        
        self.log_event("System Stopped", "Monitoring system deactivated")
    
    def update_video_frame(self, frame):
        """
        Update the video display with the latest frame.
        
        Args:
            frame: OpenCV frame (BGR format)
        """
        # Resize to the display size and overlay ROI status before converting.
        display_frame = cv2.resize(frame, (self.video_label.width(), self.video_label.height()))
        display_frame = self.roi_manager.draw_on_frame(display_frame)

        # Convert BGR to RGB for QImage
        rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        
        bytes_per_line = 3 * w
        
        # Convert to QImage
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        
        # Display
        self.video_label.setPixmap(pixmap)

    def start_roi_selection(self):
        """Start interactive ROI selection on the video feed."""
        self.roi_manager.start_roi_selection()
        self.video_label.setCursor(Qt.CrossCursor)
        self.log_event("ROI Selection", "User started ROI selection")

    def cancel_roi(self):
        """Clear the active ROI and return to full-frame detection."""
        self.roi_manager.cancel_roi()
        self.video_label.setCursor(Qt.ArrowCursor)
        self.detector.previous_frame = None
        self.log_event("ROI Cleared", "Returned to full-frame motion detection")

    def on_video_mouse_pressed(self, x, y):
        if self.roi_manager.selecting:
            self.roi_manager.begin_selection((x, y))

    def on_video_mouse_moved(self, x, y):
        if self.roi_manager.selecting:
            self.roi_manager.update_selection((x, y))

    def on_video_mouse_released(self, x, y):
        if self.roi_manager.selecting:
            roi_created = self.roi_manager.finish_selection((x, y))
            self.video_label.setCursor(Qt.ArrowCursor)
            if roi_created:
                self.detector.previous_frame = None
                self.log_event("ROI Updated", "Motion detection restricted to selected region")
            else:
                self.log_event("ROI Selection", "ROI selection canceled or too small")
    
    def on_motion_detected(self, motion, contours):
        """
        Handle motion detection events.
        
        Args:
            motion (bool): Whether motion was detected
            contours (list): List of contours detected
        """
        if motion:
            self.motion_status_label.setText("🟢 Motion Detected!")
            self.motion_status_label.setStyleSheet("color: #f44336; font-size: 12pt; font-weight: bold;")
            self.log_event("Motion Alert", f"Motion detected with {len(contours)} region(s)")
            self.motion_history.append(datetime.now())
        else:
            self.motion_status_label.setText("🔴 No Motion")
            self.motion_status_label.setStyleSheet("color: #666; font-size: 12pt;")
    
    def update_stats(self, stats):
        """Update system statistics display."""
        self.fps_label.setText(f"FPS: {stats['fps']:.1f}")
        self.frame_label.setText(f"Frames: {stats['frame_count']}")
        self.snap_count_label.setText(f"Snapshots: {stats['snapshot_count']}")
    
    def on_video_error(self, error_msg):
        """Handle video thread errors."""
        QMessageBox.critical(self, "Video Error", error_msg)
        if self.is_monitoring:
            self.stop_monitoring()
    
    def take_manual_snapshot(self):
        """Take a manual snapshot."""
        if self.video_thread and self.video_thread.cap:
            ret, frame = self.video_thread.cap.read()
            if ret:
                self.snapshot_manager.save_snapshot(frame)
                self.log_event("Manual Snapshot", "User captured snapshot manually")
                QMessageBox.information(self, "Success", "Snapshot saved successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to capture snapshot")
        else:
            QMessageBox.warning(self, "Not Active", "Start monitoring first to take snapshots")
    
    def apply_configuration(self):
        """Apply configuration changes."""
        self.current_config['CAMERA_ID'] = self.camera_id_spinbox.value()
        self.current_config['THRESHOLD_VALUE'] = self.threshold_slider.value()
        self.current_config['MIN_CONTOUR_AREA'] = self.contour_spinbox.value()
        self.current_config['BEEP_FREQUENCY'] = self.freq_spinbox.value()
        self.current_config['BEEP_DURATION'] = self.duration_spinbox.value()

        # Push the updated settings into the active detector so changes take effect immediately.
        self.detector.threshold_value = self.current_config['THRESHOLD_VALUE']
        self.detector.min_contour_area = self.current_config['MIN_CONTOUR_AREA']
        self.detector.blur_kernel_size = self.current_config['BLUR_KERNEL_SIZE']
        
        self.log_event("Configuration Updated", "System settings changed")
        
        # If monitoring is active, restart it
        if self.is_monitoring:
            QMessageBox.information(self, "Restart Required",
                                  "Please restart monitoring for camera changes to take effect.")
        
        QMessageBox.information(self, "Success", "Configuration Applied!")
    
    def reset_configuration(self):
        """Reset configuration to defaults."""
        self.camera_id_spinbox.setValue(config.CAMERA_ID)
        self.threshold_slider.setValue(config.THRESHOLD_VALUE)
        self.contour_spinbox.setValue(config.MIN_CONTOUR_AREA)
        self.freq_spinbox.setValue(config.BEEP_FREQUENCY)
        self.duration_spinbox.setValue(config.BEEP_DURATION)

        self.current_config['CAMERA_ID'] = config.CAMERA_ID
        self.current_config['THRESHOLD_VALUE'] = config.THRESHOLD_VALUE
        self.current_config['MIN_CONTOUR_AREA'] = config.MIN_CONTOUR_AREA
        self.current_config['BEEP_FREQUENCY'] = config.BEEP_FREQUENCY
        self.current_config['BEEP_DURATION'] = config.BEEP_DURATION

        self.detector.threshold_value = config.THRESHOLD_VALUE
        self.detector.min_contour_area = config.MIN_CONTOUR_AREA
        self.detector.blur_kernel_size = config.BLUR_KERNEL_SIZE
        
        self.log_event("Configuration Reset", "Settings reset to defaults")
        QMessageBox.information(self, "Reset", "Configuration reset to defaults!")
    
    def log_event(self, event_type, details):
        """Log an event to the event history table."""
        row_position = self.event_table.rowCount()
        self.event_table.insertRow(row_position)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        self.event_table.setItem(row_position, 0, QTableWidgetItem(timestamp))
        self.event_table.setItem(row_position, 1, QTableWidgetItem(event_type))
        self.event_table.setItem(row_position, 2, QTableWidgetItem(details))
        
        # Scroll to latest event
        self.event_table.scrollToBottom()
    
    def clear_event_history(self):
        """Clear all event history."""
        reply = QMessageBox.question(self, "Confirm", "Clear all event history?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.event_table.setRowCount(0)
            self.log_event("History Cleared", "Event history cleared by user")
    
    def export_event_history(self):
        """Export event history to CSV file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Event History",
                                                   "event_history.csv", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write("Timestamp,Event Type,Details\n")
                    for row in range(self.event_table.rowCount()):
                        timestamp = self.event_table.item(row, 0).text()
                        event_type = self.event_table.item(row, 1).text()
                        details = self.event_table.item(row, 2).text()
                        f.write(f'"{timestamp}","{event_type}","{details}"\n')
                QMessageBox.information(self, "Success", f"Event history exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def refresh_snapshots_list(self):
        """Refresh the snapshots list table."""
        self.snapshots_list_table.setRowCount(0)
        
        snap_dir = Path(config.SNAPSHOT_FOLDER)
        if not snap_dir.exists():
            return
        
        snapshots = list(snap_dir.glob("*.jpg"))
        self.snapshot_stats_label.setText(f"Total Snapshots: {len(snapshots)} | Folder: {config.SNAPSHOT_FOLDER}/")
        
        for idx, snap_file in enumerate(sorted(snapshots, reverse=True)[:100]):  # Show last 100
            self.snapshots_list_table.insertRow(idx)
            
            filename = snap_file.name
            size = f"{snap_file.stat().st_size / 1024:.1f} KB"
            mod_time = datetime.fromtimestamp(snap_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            
            self.snapshots_list_table.setItem(idx, 0, QTableWidgetItem(filename))
            self.snapshots_list_table.setItem(idx, 1, QTableWidgetItem(size))
            self.snapshots_list_table.setItem(idx, 2, QTableWidgetItem(mod_time))
    
    def open_snapshots_folder(self):
        """Open the snapshots folder in file explorer."""
        snap_dir = Path(config.SNAPSHOT_FOLDER).absolute()
        snap_dir.mkdir(parents=True, exist_ok=True)
        
        if sys.platform == 'win32':
            os.startfile(str(snap_dir))
        elif sys.platform == 'darwin':
            os.system(f'open "{snap_dir}"')
        else:
            os.system(f'xdg-open "{snap_dir}"')
    
    def delete_old_snapshots(self):
        """Delete snapshots older than 7 days."""
        from datetime import timedelta
        
        reply = QMessageBox.question(self, "Confirm",
                                    "Delete snapshots older than 7 days? This cannot be undone.",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            snap_dir = Path(config.SNAPSHOT_FOLDER)
            if not snap_dir.exists():
                return
            
            cutoff_time = datetime.now() - timedelta(days=7)
            deleted_count = 0
            
            for snap_file in snap_dir.glob("*.jpg"):
                if datetime.fromtimestamp(snap_file.stat().st_mtime) < cutoff_time:
                    snap_file.unlink()
                    deleted_count += 1
            
            self.refresh_snapshots_list()
            QMessageBox.information(self, "Success", f"Deleted {deleted_count} old snapshots")
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self.is_monitoring:
            reply = QMessageBox.question(self, "Exit",
                                        "Monitoring is still active. Stop and exit?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.stop_monitoring()
            else:
                event.ignore()
                return
        
        event.accept()


def main():
    """Main entry point for the GUI application."""
    app = QApplication(sys.argv)
    window = MotionDetectionGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

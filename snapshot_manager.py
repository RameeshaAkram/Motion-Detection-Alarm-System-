"""
Snapshot Manager Module
Handles saving and managing captured snapshot files
"""

import cv2
import os
from datetime import datetime
import config


class SnapshotManager:
    """Manages snapshot capture and storage."""
    
    def __init__(self):
        """Initialize snapshot manager and create snapshots folder if needed."""
        # Create snapshots folder if it doesn't exist
        if not os.path.exists(config.SNAPSHOT_FOLDER):
            os.makedirs(config.SNAPSHOT_FOLDER)
    
    def save_snapshot(self, frame):
        """
        Save current frame as JPEG with timestamp.
        
        Args:
            frame: Input frame from video capture (OpenCV format)
            
        Returns:
            str: Path to saved snapshot file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"motion_{timestamp}.jpg"
        filepath = os.path.join(config.SNAPSHOT_FOLDER, filename)
        cv2.imwrite(filepath, frame)
        return filepath
    
    def get_snapshot_count(self):
        """
        Get total number of snapshots in the folder.
        
        Returns:
            int: Number of .jpg files in snapshot folder
        """
        if not os.path.exists(config.SNAPSHOT_FOLDER):
            return 0
        return len([f for f in os.listdir(config.SNAPSHOT_FOLDER) 
                   if f.endswith('.jpg')])
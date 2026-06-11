# Configuration settings for motion detector

# Camera settings
CAMERA_ID = 0                  # 0 = built-in webcam, 1 = external

# Image processing
BLUR_KERNEL_SIZE = (5, 5)      # Kernel size for Gaussian blur
THRESHOLD_VALUE = 25           # Sensitivity (lower = more sensitive)
MIN_CONTOUR_AREA = 500         # Minimum motion area to trigger alarm

# Display settings
WINDOW_NAME = "Motion Detection Alarm"
TEXT_COLOR = (0, 0, 255)       # Red color for text
BOX_COLOR = (0, 255, 0)        # Green color for bounding box

# Alarm settings
BEEP_FREQUENCY = 1000          # Hz (1000 = standard beep)
BEEP_DURATION = 500            # milliseconds

# Snapshot settings
SNAPSHOT_FOLDER = "snapshots"
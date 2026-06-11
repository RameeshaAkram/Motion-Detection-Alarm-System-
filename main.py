import cv2
import config
from motion_detector import MotionDetector
from alarm import play_beep
from snapshot_manager import SnapshotManager

def main():
    # Initialize components
    cap = cv2.VideoCapture(config.CAMERA_ID)
    detector = MotionDetector()
    snapshot_mgr = SnapshotManager()
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera")
        print("Try changing CAMERA_ID in config.py to 1 or -1")
        return
    
    print("=" * 50)
    print("MOTION DETECTION ALARM SYSTEM")
    print("=" * 50)
    print(f"Snapshots will be saved to: {config.SNAPSHOT_FOLDER}/")
    print("Press 'q' to quit")
    print("Press 's' to save a manual snapshot")
    print("=" * 50)
    
    motion_cooldown = False
    cooldown_frames = 0
    
    while True:
        # Read frame from camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame")
            break
        
        # Make a copy for display
        display_frame = frame.copy()
        
        # Detect motion
        motion_detected, contours = detector.detect(frame)
        
        # Draw bounding boxes if motion detected
        if motion_detected and not motion_cooldown:
            # Draw boxes
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(display_frame, (x, y), (x+w, y+h), 
                            config.BOX_COLOR, 2)
            
            # Show alert text
            cv2.putText(display_frame, "MOTION DETECTED!", (50, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, config.TEXT_COLOR, 2)
            
            # Trigger alarm
            play_beep()
            
            # Save snapshot
            snapshot_path = snapshot_mgr.save_snapshot(frame)
            print(f"[!] Motion detected! Snapshot saved: {snapshot_path}")
            
            # Cooldown to prevent too many beeps
            motion_cooldown = True
            cooldown_frames = 30  # ~1 second at 30fps
        
        # Handle cooldown
        if motion_cooldown:
            cooldown_frames -= 1
            if cooldown_frames <= 0:
                motion_cooldown = False
        
        # Show snapshot count
        count = snapshot_mgr.get_snapshot_count()
        cv2.putText(display_frame, f"Snapshots: {count}", (50, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Show instructions
        cv2.putText(display_frame, "Press 'q' to quit", (10, display_frame.shape[0] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Display the frame
        cv2.imshow(config.WINDOW_NAME, display_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print(f"\nExiting. Total snapshots taken: {snapshot_mgr.get_snapshot_count()}")
            break
        elif key == ord('s'):
            manual_path = snapshot_mgr.save_snapshot(frame)
            print(f"[*] Manual snapshot saved: {manual_path}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
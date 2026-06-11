import cv2

def preprocess_frame(frame, kernel_size):
    """Convert to grayscale, blur, and return processed frame"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, kernel_size, 0)
    return blurred

def draw_motion_indicators(frame, contours, min_area):
    """Draw bounding boxes around motion areas"""
    motion_detected = False
    boxes = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            motion_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            boxes.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    return motion_detected, boxes
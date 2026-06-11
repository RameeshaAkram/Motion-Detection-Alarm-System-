import cv2
import config
from utils import preprocess_frame


class MotionDetector:
    """Frame-differencing motion detector used by CLI and GUI modes."""

    def __init__(self, threshold_value=None, min_contour_area=None, blur_kernel_size=None):
        self.threshold_value = threshold_value if threshold_value is not None else config.THRESHOLD_VALUE
        self.min_contour_area = min_contour_area if min_contour_area is not None else config.MIN_CONTOUR_AREA
        self.blur_kernel_size = blur_kernel_size if blur_kernel_size is not None else config.BLUR_KERNEL_SIZE
        self._previous_frame = None

    def reset(self):
        """Reset detector state (for camera restart or source change)."""
        self._previous_frame = None

    def detect(self, frame, roi_mask=None):
        """
        Detect motion in a frame.

        Returns:
            tuple[bool, list]: (motion_detected, filtered_contours)
        """
        processed = preprocess_frame(frame, self.blur_kernel_size)

        if self._previous_frame is None:
            self._previous_frame = processed
            return False, []

        frame_delta = cv2.absdiff(self._previous_frame, processed)

        # Restrict motion analysis to the selected ROI when provided.
        if roi_mask is not None:
            frame_delta = cv2.bitwise_and(frame_delta, frame_delta, mask=roi_mask)

        thresh = cv2.threshold(frame_delta, self.threshold_value, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        filtered = [c for c in contours if cv2.contourArea(c) >= self.min_contour_area]

        self._previous_frame = processed
        return bool(filtered), filtered

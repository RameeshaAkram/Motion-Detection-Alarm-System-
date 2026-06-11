"""
Alarm Module
Provides audio alert functionality for motion detection
"""

import config


def play_beep(frequency=None, duration=None):
    """
    Play a beep sound when motion is detected.
    
    Args:
        frequency (int, optional): Beep frequency in Hz. Defaults to config value.
        duration (int, optional): Beep duration in milliseconds. Defaults to config value.
    """
    # Use config defaults if parameters not provided
    if frequency is None:
        frequency = config.BEEP_FREQUENCY
    if duration is None:
        duration = config.BEEP_DURATION
    
    try:
        # For Windows
        import winsound
        winsound.Beep(frequency, duration)
    except ImportError:
        # For Linux/Mac - alternative method
        try:
            import os
            os.system('printf "\a"')
        except Exception:
            print("🔔 MOTION DETECTED!")
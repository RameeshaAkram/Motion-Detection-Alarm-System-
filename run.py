"""
Motion Detection Alarm System - Entry Point
===========================================

This is the main entry point for the Motion Detection Alarm System.
It launches the professional GUI application.

To use in CLI mode instead, run: python main.py
"""

import sys
from gui import main

if __name__ == "__main__":
    print("=" * 60)
    print("Motion Detection Alarm System - GUI Interface")
    print("=" * 60)
    print("\nLaunching GUI application...")
    print("\nFeatures:")
    print("  • Real-time motion detection with video feed")
    print("  • Configurable sensitivity and alert settings")
    print("  • Event logging and history tracking")
    print("  • Snapshot management and export")
    print("  • Built-in documentation and help")
    print("\nStarting GUI window...\n")
    
    main()
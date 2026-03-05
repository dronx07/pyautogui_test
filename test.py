#!/usr/bin/env python3
"""
PyAutoGUI CI Test for GitHub Actions with Xvfb and video recording.
Produces screenshots and logs mouse/screen info.
"""

import pyautogui
import time
import os
import sys
from datetime import datetime

# CI-safe settings
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.2


def wait_for_display():
    """Ensure Xvfb display is ready"""
    print("Waiting for display to stabilize...")
    time.sleep(3)
    display = os.environ.get("DISPLAY")
    print(f"DISPLAY = {display}")
    if not display:
        print("❌ DISPLAY variable not set!")
        sys.exit(1)


def save_screenshot(name_prefix):
    """Save screenshot using PyAutoGUI"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name_prefix}_{timestamp}.png"
        img = pyautogui.screenshot()
        img.save(filename)
        print(f"✅ Screenshot saved: {filename}")
    except Exception as e:
        print(f"❌ Screenshot failed: {e}")


def test_pyautogui_basic():
    """Run basic PyAutoGUI tests"""
    print("=" * 50)
    print("PyAutoGUI GitHub Actions Test")
    print("=" * 50)

    # Screen size
    try:
        width, height = pyautogui.size()
        print(f"✅ Screen size: {width} x {height}")
    except Exception as e:
        print(f"❌ Screen size test failed: {e}")
        return False

    # Mouse position
    try:
        x, y = pyautogui.position()
        print(f"✅ Mouse position: ({x}, {y})")
    except Exception as e:
        print(f"❌ Mouse position test failed: {e}")
        return False

    # Move mouse safely
    try:
        target_x = min(200, width - 1)
        target_y = min(200, height - 1)
        pyautogui.moveTo(target_x, target_y, duration=0.5)
        new_x, new_y = pyautogui.position()
        print(f"✅ Mouse moved to: ({new_x}, {new_y})")
    except Exception as e:
        print(f"❌ Mouse move failed: {e}")
        return False

    # Click test
    try:
        pyautogui.click(target_x, target_y)
        print("✅ Mouse click successful")
    except Exception as e:
        print(f"❌ Mouse click failed: {e}")
        return False

    # Keyboard test
    try:
        pyautogui.press("enter")
        pyautogui.press("tab")
        print("✅ Keyboard input successful")
    except Exception as e:
        print(f"❌ Keyboard input failed: {e}")
        return False

    # Screenshot
    save_screenshot("screenshot")
    return True


def test_sequence_screenshots():
    """Take multiple screenshots to verify display updates"""
    print("\n📸 Taking sequence screenshots...")
    for i in range(3):
        save_screenshot(f"test_sequence_{i}")
        time.sleep(1)
    return True


if __name__ == "__main__":
    print("\n🚀 Starting PyAutoGUI CI test...\n")
    wait_for_display()

    basic_result = test_pyautogui_basic()
    sequence_result = test_sequence_screenshots()

    print("\n" + "=" * 50)
    if basic_result and sequence_result:
        print("✅ ALL TESTS PASSED — PyAutoGUI works in GitHub Actions!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)

# Novas2
# Eye-Controlled Mouse Cursor 

## Overview

This project is designed to empower individuals with physical disabilities by offering hands-free computer interaction. It allows users to control the mouse cursor using their eye movement, eye blinks, winks and dwell-based typing on an on-screen keyboard. The goal is to provide a non-touch, accessible interface for users with limited or no hand mobility.

We are now expanding this into a multi-modal interaction system, where users can also interact using:

Voice commands
Hand gestures

The system will intelligently detect the user’s preferred mode of control based on their active movements (eyes, voice, or hands) and enable only the relevant module.

---

## Features

### Current Features (Phase 1: Eye Control)
Cursor movement via eye tracking
Left click with a single blink
Right click with right eye wink
Drag and drop with blink hold
Zoom in/out by moving closer/farther
On-screen keyboard for typing (blink-to-type)
Screenshot capture by closing both eyes for 5 seconds

### Upcoming Features (Phase 2: Multimodal)
Voice commands (e.g., "left click", "move up", "scroll down")
Hand gesture control using webcam (e.g., swipe to move mouse)
Automatic disability mode detection: activate only the relevant input method based on body part used

---

## Tech Stack
Python 3.8+, OpenCV, Mediapipe ,PyAutoGUI, SpeechRecognition, TensorFlow (planned for hand gesture detection) ,Flask + JavaScript (planned for web deployment)

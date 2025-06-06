# Hand Gesture Controller

A Python application that converts hand gestures into keyboard inputs.

## Features
- Control games with natural hand movements
- Customizable gesture mappings
- Real-time hand tracking visualization
- Low latency input simulation

## Gesture Mappings
| Gesture              | Keyboard Input | Description                          |
|----------------------|----------------|--------------------------------------|
| ✋ All fingers open   | UP             | Raise all five fingers               |
| ✊ Fist closed       | DOWN           | Close all fingers into a fist        |
| 👍 Thumb+Index      | LEFT           | Extend thumb and index finger only   |
| ✌️ Peace sign      | RIGHT          | Extend index and middle fingers only |
| 🖖 3-finger salute | SPACE          | Extend index, middle and ring fingers |

## Requirements
- Python 3.8+
- Webcam
- Supported OS: Windows/macOS/Linux

## Installation
1. Clone the repository:
```bash
git clone https://github.com/Prayoga-bit/Control-Hands-Tracker.git
cd hand-gesture-controller
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Usage
- Run the controller:

```bash
python hands_tracker_control.py
```
4. Gesture tips:
* Keep hand visible in camera frame
* Maintain good lighting conditions
* Make deliberate, clear gestures

5. Configuration
> Modify these parameters in hands_tracker_control.py:
* min_detection_confidence: 0.7-0.9 (higher = more strict)
* gesture_debounce_time: 0.3-1.0 seconds (prevents rapid inputs)

6. Troubleshooting
**Issue**: Gestures not recognized
* Ensure your webcam is working
* Try different lighting conditions
* Adjust detection confidence threshold

**Issue**: Inputs too sensitive
* Increase the debounce time
* Make more distinct gestures

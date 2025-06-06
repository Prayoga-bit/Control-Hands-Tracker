import cv2
import mediapipe as mp
import pyautogui
import time

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.85,  # Meningkatkan confidence threshold
    min_tracking_confidence=0.85
)
mp_drawing = mp.solutions.drawing_utils

def count_extended_fingers(hand_landmarks):
    # Daftar ujung jari dan sendi pembanding
    finger_tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    finger_mcps = [
        mp_hands.HandLandmark.INDEX_FINGER_MCP,
        mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
        mp_hands.HandLandmark.RING_FINGER_MCP,
        mp_hands.HandLandmark.PINKY_MCP
    ]
    
    # Deteksi ibu jari (logika khusus)
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_open = thumb_tip.x < thumb_ip.x if hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < thumb_ip.x else thumb_tip.x > thumb_ip.x
    
    # Deteksi jari lainnya
    extended_fingers = []
    for tip, mcp in zip(finger_tips, finger_mcps):
        tip_point = hand_landmarks.landmark[tip]
        mcp_point = hand_landmarks.landmark[mcp]
        if tip_point.y < mcp_point.y - 0.05:  # Menambahkan threshold -0.05 untuk lebih pasti
            extended_fingers.append(True)
        else:
            extended_fingers.append(False)
    
    return thumb_open, extended_fingers

def detect_hand_gesture(hand_landmarks):
    thumb_open, extended_fingers = count_extended_fingers(hand_landmarks)
    index_open, middle_open, ring_open, pinky_open = extended_fingers
    
    # Hitung jumlah jari yang terbuka (selain ibu jari)
    extended_count = sum(extended_fingers)
    
    # Deteksi gestur berdasarkan kombinasi jari
    if thumb_open and extended_count == 4:  # Semua jari terbuka
        return "up"
    elif not thumb_open and extended_count == 0:  # Semua jari menutup
        return "down"
    elif thumb_open and index_open and extended_count == 1:  # Hanya ibu jari + telunjuk
        return "left"
    elif not thumb_open and extended_count == 2 and index_open and middle_open:  # Telunjuk + tengah
        return "right"
    elif not thumb_open and extended_count == 3 and index_open and middle_open and ring_open:  # Telunjuk + tengah + manis
        return "space"
    else:
        return None

def main():
    cap = cv2.VideoCapture(0)
    last_gesture = None
    last_gesture_time = 0
    gesture_debounce_time = 0.6  # Meningkatkan debounce time
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
            
        # Konversi warna dan proses
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        
        # Gambar hasil deteksi
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                current_gesture = detect_hand_gesture(hand_landmarks)
                current_time = time.time()
                
                if current_gesture and (current_gesture != last_gesture or 
                                      current_time - last_gesture_time > gesture_debounce_time):
                    print(f"Gesture detected: {current_gesture}")
                    
                    if current_gesture == "up":
                        pyautogui.press('up')
                    elif current_gesture == "down":
                        pyautogui.press('down')
                    elif current_gesture == "left":
                        pyautogui.press('left')
                    elif current_gesture == "right":
                        pyautogui.press('right')
                    elif current_gesture == "space":
                        pyautogui.press('space')
                    
                    last_gesture = current_gesture
                    last_gesture_time = current_time
        
        cv2.imshow('Hand Gesture Control', image)
        if cv2.waitKey(5) & 0xFF == 27:  # ESC untuk keluar
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
import cv2
import mediapipe as mp
import math
# import serial  # 將這行注釋掉，暫時取消串口初始化

# 載入 Mediapipe 模組
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# 設置進度條的尺寸和位置
progress_bar_height = 20
progress_bar_length = 300
progress_bar_start_x = 50
progress_bar_start_y = 50

# 初始化串口通訊（暫時注釋掉）
# ser = serial.Serial('COM3', 9600)  # 請將 'COM3' 替換成你的 Arduino 串口，9600 為波特率

# 打開攝像頭
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("攝像頭無法開啟")
    exit()

# 使用 mediapipe 偵測手掌
with mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5) as hands:
    while True:
        ret, img = cap.read()
        if not ret:
            print("無法接收影格")
            break
        img = cv2.flip(img, 1)  
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
        results = hands.process(imgRGB) 
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                
                distance = math.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)
                brightness = min(distance / 0.5, 1)
                
                if brightness < 0.1:
                    brightness_value = 0
                    brightness_text = "off"
                else:
                    brightness_value = int(brightness * 255)  # 將亮度映射到 0 到 255 的範圍
                    brightness_text = f'{brightness:.2f}'
                
                # 送亮度值到 Arduino（暫時注釋掉）
                print("Output to Arduino:", brightness_value)
                # ser.write(str(brightness_value).encode())

                for i in range(int(brightness * 10)):
                    cv2.rectangle(img, (progress_bar_start_x + i * 30, progress_bar_start_y),
                                  (progress_bar_start_x + (i + 1) * 30, progress_bar_start_y + progress_bar_height),
                                  (0, 0, 0), -1)
                    cv2.rectangle(img, (progress_bar_start_x + i * 30, progress_bar_start_y),
                                  (progress_bar_start_x + (i + 1) * 30, progress_bar_start_y + progress_bar_height),
                                  (0, 255, 0), -1)
                
                fontFace = cv2.FONT_HERSHEY_SIMPLEX  
                font_size = 2  
                thickness = 5  
                lineType = cv2.LINE_AA  
                cv2.putText(img, f'Brightness: {brightness_text}', (30, 120), fontFace, font_size, (0, 0, 0), thickness + 5, lineType)
                cv2.putText(img, f'Brightness: {brightness_text}', (30, 120), fontFace, font_size, (255, 255, 255), thickness, lineType)

        cv2.imshow('Finger Distance Progress Bar', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

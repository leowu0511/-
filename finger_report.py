import cv2
import mediapipe as mp
import math

# 載入 Mediapipe 模組
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# 根據兩點的座標，計算手指的角度
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos((v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 180
    return angle_

# 根據傳入的節點座標，得到手指的角度
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
        ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
    )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
    )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
        ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
    )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
        ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
    )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
        ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
    )
    angle_list.append(angle_)
    return angle_list

# 根據手指角度的串列內容，返回對應的手勢名稱
def hand_pos(finger_angle):
    f1 = finger_angle[0]  # 大拇指角度
    f2 = finger_angle[1]  # 食指角度
    f3 = finger_angle[2]  # 中指角度
    f4 = finger_angle[3]  # 無名指角度
    f5 = finger_angle[4]  # 小拇指角度
    # 小於 50 表示手指伸直，大於等於 50 表示手指彎起來
    if f1 < 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return 'good'
    elif f1 >= 50 and f2 >= 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
        return 'no good'
    elif f1 >= 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 < 50:
        return 'lol'
    elif f1 < 50 and f2 >= 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return 'ok'
    elif f1 >= 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return '0'
    elif f1 >= 50 and f2 < 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return '1'
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
        return '2'
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 >= 50:
        return '3'
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return '4'
    elif f1 < 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return '5'
    elif f1 < 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 < 50:
        return '6'
    elif f1 < 50 and f2 < 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return '7'
    elif f1 < 50 and f2 < 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
        return '8'
    elif f1 < 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 >= 50:
        return '9'
    else:
        return ' '

# 打開攝像頭
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("攝像頭無法開啟")
    exit()

fontFace = cv2.FONT_HERSHEY_SIMPLEX  # 文字字體
lineType = cv2.LINE_AA  # 文字邊框

# 使用 mediapipe 偵測手掌
with mp_hands.Hands(
    #參數設定
    model_complexity=0,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8) as hands:
    w, h = 540, 310  # 影像大小
    while True:
        ret, img = cap.read()
        if not ret:
            print("無法接收影格")
            break
        img = cv2.resize(img, (w, h))  # 調整影像大小，加快處理效率
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉換成 RGB
        results = hands.process(img2)  # 偵測手勢
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_points = []  # 紀錄手指節點座標的串列
                for i in hand_landmarks.landmark:
                    # 將 21 個節點換算成座標，記錄到 finger_points
                    x = int(i.x * w)
                    y = int(i.y * h)
                    finger_points.append((x, y))
                    # 輸出節點
                    cv2.circle(img, (x, y), 5, (0, 0, 255), -1)  # 红色节点
                # 輸出連接線
                for connection in mp_hands.HAND_CONNECTIONS:
                    start_idx, end_idx = connection
                    cv2.line(img, finger_points[start_idx], finger_points[end_idx], (0, 255, 0), 2)  # 綠色的連接線
                
                if finger_points:
                        finger_angle = hand_angle(finger_points)  # 計算手指角度
                        text = hand_pos(finger_angle)  # 取得手勢名稱
                        font_size = 2  # 調整文字大小
                        thickness = 5  # 調整邊框厚度
                        # 繪製黑邊文字
                        cv2.putText(img, text, (30, 120), fontFace, font_size, (0, 0, 0), thickness + 5, lineType)
                        # 繪製白色文字
                        cv2.putText(img, text, (30, 120), fontFace, font_size, (255, 255, 255), thickness, lineType)
        cv2.imshow('Report(press q to stop)', img)
        # 每 5ms 偵測是否按下 'q' 鍵,如果有就結束程序。
        if cv2.waitKey(5) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

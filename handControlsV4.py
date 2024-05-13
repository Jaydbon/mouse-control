import cv2
import mediapipe as mp
import pyautogui as cntrl
import keyboard

screenx = 0
screeny = 0

g_pressed = False
clicked = {'left':False, 'right':False}

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def map_value_x(val):
    percentage = (500 - val) / 500
    mapped_value = percentage * 1920
    return mapped_value

def map_value_y(val):
    percentage = (val) / (400)
    mapped_value = percentage * (1080)
    return mapped_value

def moveMouse():
    x = map_value_x(thumbx)
    y = map_value_y(thumby)
    cntrl.moveTo(x, y, duration=0)

def click(fingLoc, click):
    if abs(thumby-fingLoc[1]) <= 40 and abs(thumbx-fingLoc[0]) <= 10 and clicked[click] == False:
        cntrl.mouseDown(button=click)
        clicked[click] = True
        print(clicked)

    elif abs(thumby-fingLoc[1]) > 40 and abs(thumbx-fingLoc[0]) > 10 and clicked[click] == True:
        cntrl.mouseUp(button=click)
        clicked[click] = False
        print(clicked)


def exitCode(event):
    global g_pressed
    if event.name == 'g':
        g_pressed = True

def mouseOn():
    point = hand_landmarks.landmark[8]
    pointx, pointy = int(point.x * frame.shape[1]), int(point.y * frame.shape[0])
    cv2.circle(frame, (pointx, pointy), 10, (0, 255, 0), cv2.FILLED)
    click((pointx,pointy), 'right')
    
    index = hand_landmarks.landmark[16]
    indexx, indexy = int(index.x * frame.shape[1]), int(index.y * frame.shape[0])
    cv2.circle(frame, (indexx, indexy), 10, (0, 255, 0), cv2.FILLED)
    click((indexx,indexy), 'left')
    
    moveMouse()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            pinky = hand_landmarks.landmark[20]
            pinkyx, pinkyy = int(pinky.x * frame.shape[1]), int(pinky.y * frame.shape[0])
            cv2.circle(frame, (pinkyx, pinkyy), 10, (255, 0, 255), cv2.FILLED)
            
            thumb = hand_landmarks.landmark[4]
            thumbx, thumby = int(thumb.x * frame.shape[1]), int(thumb.y * frame.shape[0])
            cv2.circle(frame, (thumbx, thumby), 10, (255, 0, 255), cv2.FILLED)
            
            if pinkyx - thumbx <= 20 and pinkyy - thumby <= 20:
                mouseOn()
        
    if cv2.waitKey(1) & 0xFF == ord('g'):
         break

    cv2.imshow('Hand Tracking', frame)

    cv2.waitKey(1)
    keyboard.on_press(exitCode)
    if g_pressed == True:
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
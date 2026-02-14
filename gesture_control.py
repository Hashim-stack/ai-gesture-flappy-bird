import cv2
import mediapipe as mp

class GestureController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def get_frame_and_gesture(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, False

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        gesture = False

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                wrist_y = hand_landmarks.landmark[0].y
                index_y = hand_landmarks.landmark[8].y

                if index_y < wrist_y:
                    gesture = True
                    cv2.putText(frame, "JUMP", (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0,255,0), 2)
                else:
                    cv2.putText(frame, "DOWN", (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0,0,255), 2)
        else:
            cv2.putText(frame, "NO HAND", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0,0,255), 2)

        return frame, gesture

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

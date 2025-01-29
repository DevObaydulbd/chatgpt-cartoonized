
import cv2

def apply_cartoon_effect(input_video, output_video):
    cap = cv2.VideoCapture(input_video)
    output_path = output_video
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(frame, 9, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        cv2.imwrite(output_path, cartoon)

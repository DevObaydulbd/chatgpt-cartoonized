from flask import Flask, request, send_file
from flask_cors import CORS
import cv2
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/cartoonize', methods=['POST'])
def cartoonize():
    video = request.files['video']
    video_path = f'static/{video.filename}'
    video.save(video_path)
    
    cap = cv2.VideoCapture(video_path)
    output_path = f"static/output_{video.filename}"
    
    # Cartoon effect processing
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(frame, 9, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        
        # Write to output video
        cv2.imwrite(output_path, cartoon)
    
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

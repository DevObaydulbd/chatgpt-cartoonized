from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import cv2
import os

app = Flask(__name__)

# Allow all origins (for testing). You can restrict it later.
CORS(app, resources={r"/*": {"origins": "*"}})  

@app.route('/cartoonize', methods=['POST'])
def cartoonize():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400

        video = request.files['video']
        video_path = f'static/{video.filename}'

        if not os.path.exists('static'):
            os.makedirs('static')

        video.save(video_path)
        print(f"Video saved to {video_path}")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Error opening video file")

        # Get video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        output_path = f"static/output_{os.path.splitext(video.filename)[0]}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame is None:
                print("Skipping invalid frame")
                continue  # Skip processing if frame is empty

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(frame, 9, 250, 250)
            cartoon = cv2.bitwise_and(color, color, mask=edges)

            out.write(cartoon)

        cap.release()
        out.release()

        print(f"Processed video saved to {output_path}")

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

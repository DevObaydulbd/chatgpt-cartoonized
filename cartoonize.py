import cv2

def apply_cartoon_effect(input_video, output_video):
    cap = cv2.VideoCapture(input_video)
    
    # ভিডিও প্রপার্টি সেট করা
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 ফরম্যাট
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # প্রতি ৫টি ফ্রেমে ১টি প্রসেস করা হবে
        if frame_count % 5 == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(frame, 9, 250, 250)
            cartoon = cv2.bitwise_and(color, color, mask=edges)
        else:
            cartoon = frame  # স্কিপ করা ফ্রেমগুলো আসল ফ্রেম রাখবে
        
        out.write(cartoon)  # প্রসেস করা ফ্রেম আউটপুট ভিডিওতে সংরক্ষণ

        frame_count += 1

    cap.release()
    out.release()
    print(f"Cartoon effect applied and saved to {output_video}")

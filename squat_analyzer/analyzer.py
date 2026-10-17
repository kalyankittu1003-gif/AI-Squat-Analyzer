import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import tempfile
import os
import json

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle

import shutil

def process_video(video_path, progress_callback=None):
    cap = cv2.VideoCapture(video_path)
    
    orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if fps == 0 or np.isnan(fps):
        fps = 30.0

    # Downscale high-resolution videos (1080p/4K) to max 720px for 5x-10x faster processing
    MAX_DIM = 720
    max_orig = max(orig_width, orig_height)
    if max_orig > MAX_DIM:
        scale = MAX_DIM / float(max_orig)
        width = int(orig_width * scale)
        height = int(orig_height * scale)
    else:
        width = orig_width
        height = orig_height

    # Ensure even dimensions for video codecs
    width = width if width % 2 == 0 else width - 1
    height = height if height % 2 == 0 else height - 1

    # Intelligent frame sampling: if video is > 35 FPS, sample down to ~25-30 FPS to cut work in half
    if fps > 35:
        frame_step = max(1, int(round(fps / 25.0)))
    else:
        frame_step = 1

    out_fps = fps / frame_step
    
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "annotated_video.mp4")
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, out_fps, (width, height))
    
    # Initialize PoseLandmarker Tasks API with in-memory buffer and explicit CPU delegate
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_asset_path = os.path.join(base_dir, 'pose_landmarker.task')
    if not os.path.exists(model_asset_path):
        model_asset_path = 'pose_landmarker.task'
    
    with open(model_asset_path, 'rb') as f:
        model_bytes = f.read()

    base_options = python.BaseOptions(
        model_asset_buffer=model_bytes,
        delegate=python.BaseOptions.Delegate.CPU
    )
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        output_segmentation_masks=False)
    detector = vision.PoseLandmarker.create_from_options(options)
    
    frame_idx = 0
    processed_count = 0
    metrics = []
    bar_path = []
    last_timestamp_ms = -1
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        current_frame_idx = frame_idx
        frame_idx += 1
        
        # Skip frames if sampling is active
        if current_frame_idx % frame_step != 0:
            continue

        processed_count += 1
        timestamp = current_frame_idx / fps
        timestamp_ms = max(last_timestamp_ms + 1, int(timestamp * 1000))
        last_timestamp_ms = timestamp_ms

        # Resize frame to optimized resolution if needed
        if (orig_width, orig_height) != (width, height):
            frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
            
        # Convert to RGB and then to mp.Image
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Fast Video-mode Detect
        detection_result = detector.detect_for_video(mp_image, timestamp_ms)
        
        image = frame.copy() # BGR for writing
        
        try:
            if detection_result.pose_landmarks and len(detection_result.pose_landmarks) > 0:
                landmarks = detection_result.pose_landmarks[0]
                
                # Indexes for Pose Landmarker:
                # 0: nose, 7,8: ears
                # 11,12: shoulders
                # 23,24: hips
                # 25,26: knees
                # 27,28: ankles
                # 31,32: foot indices (toes)
                
                if landmarks[24].visibility > landmarks[23].visibility:
                    # RIGHT side
                    hip = [landmarks[24].x, landmarks[24].y]
                    knee = [landmarks[26].x, landmarks[26].y]
                    ankle = [landmarks[28].x, landmarks[28].y]
                    shoulder = [landmarks[12].x, landmarks[12].y]
                    ear = [landmarks[8].x, landmarks[8].y]
                    toe = [landmarks[32].x, landmarks[32].y]
                else:
                    # LEFT side
                    hip = [landmarks[23].x, landmarks[23].y]
                    knee = [landmarks[25].x, landmarks[25].y]
                    ankle = [landmarks[27].x, landmarks[27].y]
                    shoulder = [landmarks[11].x, landmarks[11].y]
                    ear = [landmarks[7].x, landmarks[7].y]
                    toe = [landmarks[31].x, landmarks[31].y]
                
                # Draw joint points
                for pt in [hip, knee, ankle, shoulder, ear, toe]:
                    cv2.circle(image, (int(pt[0]*width), int(pt[1]*height)), 4, (0, 255, 255), -1)
                
                bar_x = int(shoulder[0] * width)
                bar_y = int(shoulder[1] * height)
                bar_path.append((bar_x, bar_y))
                
                midfoot_x = (ankle[0] + toe[0]) / 2.0
                back_angle = calculate_angle([shoulder[0], 0], shoulder, hip)
                
                metrics.append({
                    'frame': current_frame_idx,
                    'timestamp': timestamp,
                    'hip_y': hip[1],
                    'knee_y': knee[1],
                    'shoulder_x': shoulder[0],
                    'shoulder_y': shoulder[1],
                    'midfoot_x': midfoot_x,
                    'bar_x': bar_x,
                    'bar_y': bar_y,
                    'back_angle': back_angle,
                    'knee_x': knee[0],
                    'toe_x': toe[0],
                    'ear_x': ear[0],
                    'ear_y': ear[1]
                })
                
                midfoot_px = int(midfoot_x * width)
                cv2.line(image, (midfoot_px, 0), (midfoot_px, height), (255, 255, 0), 1)
                cv2.putText(image, "Midfoot", (midfoot_px - 20, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
                
                # Fast vectorized polyline drawing for bar trajectory
                if len(bar_path) > 1:
                    pts = np.array(bar_path, dtype=np.int32).reshape((-1, 1, 2))
                    cv2.polylines(image, [pts], isClosed=False, color=(0, 0, 255), thickness=2)
                    
                cv2.line(image, (int(shoulder[0]*width), int(shoulder[1]*height)), (int(hip[0]*width), int(hip[1]*height)), (0, 255, 0), 2)
                
                knee_px_y = int(knee[1] * height)
                hip_px_y = int(hip[1] * height)
                cv2.line(image, (0, knee_px_y), (width, knee_px_y), (255, 0, 255), 1)
                cv2.circle(image, (int(hip[0]*width), hip_px_y), 5, (255, 0, 0), -1)
                
                if hip[1] > knee[1]:
                    depth_status = "Below Parallel"
                    color = (0, 255, 0)
                else:
                    depth_status = "Above Parallel"
                    color = (0, 0, 255)
                    
                cv2.putText(image, depth_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                
        except Exception as e:
            print("Error parsing frame:", e)
        
        out.write(image)

        # Notify progress callback periodically
        if progress_callback and total_frames > 0 and (processed_count % 5 == 0 or current_frame_idx >= total_frames - 1):
            progress_callback(min(current_frame_idx + 1, total_frames), total_frames)
        
    cap.release()
    out.release()
    
    # Fast transcode if ffmpeg binary actually exists on the system
    final_output = os.path.join(temp_dir, "annotated_video_web.mp4")
    if shutil.which("ffmpeg"):
        os.system(f"ffmpeg -y -i {output_path} -preset ultrafast -crf 23 -vcodec libx264 -f mp4 {final_output}")
    
    reps = analyze_reps(metrics)
    
    return final_output if os.path.exists(final_output) else output_path, reps

def analyze_reps(metrics):
    if not metrics:
        return []
        
    smoothed_hip_y = [m['hip_y'] for m in metrics]
    for i in range(1, len(smoothed_hip_y)-1):
        smoothed_hip_y[i] = (smoothed_hip_y[i-1] + smoothed_hip_y[i] + smoothed_hip_y[i+1]) / 3
        
    reps = []
    in_rep = False
    rep_start = 0
    bottom = 0
    max_y = 0
    
    standing_y = np.mean(smoothed_hip_y[:10]) if len(smoothed_hip_y) > 10 else smoothed_hip_y[0]
    threshold = 0.05
    
    for i, y in enumerate(smoothed_hip_y):
        if not in_rep and y > standing_y + threshold:
            in_rep = True
            rep_start = i
            max_y = y
            bottom = i
        elif in_rep:
            if y > max_y:
                max_y = y
                bottom = i
            
            if y < standing_y + threshold and i - bottom > 10:
                in_rep = False
                
                rep_data = metrics[rep_start:i]
                bottom_data = metrics[bottom]
                
                bar_xs = [m['shoulder_x'] for m in rep_data]
                midfoot_x = np.mean([m['midfoot_x'] for m in rep_data])
                max_dev = max([abs(bx - midfoot_x) for bx in bar_xs]) if bar_xs else 0
                
                reps.append({
                    'rep_number': len(reps) + 1,
                    'start_time': metrics[rep_start]['timestamp'],
                    'bottom_time': metrics[bottom]['timestamp'],
                    'end_time': metrics[i]['timestamp'],
                    'achieved_depth': 'Below Parallel' if bottom_data['hip_y'] > bottom_data['knee_y'] else 'Above Parallel',
                    'max_bar_deviation_x': max_dev,
                    'bottom_back_angle': bottom_data['back_angle'],
                    'forward_knee_travel': bottom_data['knee_x'] - bottom_data['toe_x']
                })
                
    return reps

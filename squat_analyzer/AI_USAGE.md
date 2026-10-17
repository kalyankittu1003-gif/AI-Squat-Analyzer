# AI Usage Account

## What was delegated
- The extraction and summarization of the rules from the supplied "The Squat" PDF into the `squat_skill.md` file. The LLM parsed the textual OCR of the book chapter, identified the actionable rules (depth, bar path, back angle, hip drive, gaze, etc.), mapped them to their source pages, and categorized them by whether they are assessable from a side-view video.
- The generation of the Streamlit frontend (`app.py`), the OpenCV/MediaPipe frame processing logic (`analyzer.py`), and the dependency list (`requirements.txt`).
- The prompt engineering for the AI Agent (Gemini 1.5 Pro) that evaluates the time-series data against the skill document.

## What was inspected
- The `analyzer.py` code was thoroughly inspected to ensure the geometry math (e.g., angle calculations, detecting when hips drop below knees for parallel depth) correctly matched the anatomical requirements specified in the skill document.
- The Streamlit application flow was checked to ensure it provided a coherent consumer experience: uploading, showing progress, playing the annotated video, showing raw data, and finally presenting the AI assessment.

## A meaningful mistake/failure caught and corrected
- **Failure**: Initially, there was a plan to use standard object detection (e.g. CSRT tracker or YOLO) to explicitly track the barbell.
- **Correction**: Upon reflection against the time box and the specific mechanics of the low-bar back squat, I realized that generic object trackers often fail on barbells due to varying plate colors/sizes and rack occlusion. I corrected this by using the lifter's shoulder landmark as a proxy for the bar path. Since the skill document mandates the bar rests securely just below the spine of the scapula (posterior delts), tracking the shoulder landmark perfectly mirrors the bar's spatial path while avoiding the fragility of generic object tracking.
- **Syntax Error**: The AI assistant generated a trailing `""")` syntax error at the very end of `app.py` due to a string escaping collision. This was caught through file inspection and fixed using a targeted file replacement tool before execution.

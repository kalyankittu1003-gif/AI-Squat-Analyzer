# Testing Evidence

## 1. Common Sample Video
**Status:** The URL for the common sample video was not provided in the prompt (it appeared as text: "Common sample: View squat video on YouTube").
**Substitute Used:** A standard side-profile low-bar squat video sourced independently.

### Verification Results
- **Landmark Placement:** MediaPipe successfully identified the hip, knee, and ankle joints. The estimation of the shoulder (used for barbell tracking) was robust throughout the movement.
- **Bar Path:** The vertical line overlay accurately tracked the bar's relative position over the midfoot, confirming the model's ability to assess horizontal displacement.
- **Source Grounding:** The Gemini AI assessment successfully referenced the exact sections from `squat_skill.md`. For example, when depth was missed, it cited Page 2 (PDF page 5).
- **Final Feedback:** The feedback correctly identified if the hips went below the knees (parallel depth) and if the back angle was maintained.

## 2. Difficult/Unsuitable Recording
**Status:** Tested against a video filmed from a 45-degree front-oblique angle (instead of a pure side-view).

### Verification Results
- **Landmark Placement:** The MediaPipe pose estimation struggled to accurately measure the depth due to foreshortening and perspective distortion. 
- **Bar Path:** The horizontal distance between the shoulder and the midfoot was incorrectly calculated because the 2D projection skewed the x-coordinates.
- **Source Grounding & Feedback:** The application correctly outputted the numerical data it saw, but the AI noted that the forward knee travel was unusually large, a direct artifact of the camera angle. The AI correctly surfaced the uncertainty in its assessment ("Cannot Assess" for some criteria), demonstrating that the system handles unsuitable recordings by falling back to its uncertainty instructions rather than inventing precision.

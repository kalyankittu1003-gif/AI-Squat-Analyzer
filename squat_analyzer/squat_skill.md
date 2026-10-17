# Squat Assessment Skill (Low-Bar Back Squat)

This document contains the rules for analyzing a low-bar back squat, extracted from "The Squat" (Document_for_skill.pdf, pages 1-35).

## Assessment Criteria

### 1. Squat Depth
- **Rule**: The squat must be full range of motion. The hips must drop below level with the top of the patellas. Specifically, the "apex in the crease of the shorts" must drop below the top of the knee.
- **Reference**: Page 2 (PDF page 5) Figure 2-1, Page 16 (PDF page 19).
- **Side-View Assessable**: YES. The vertical relationship between the hip joint and knee joint can be tracked.

### 2. Barbell Path & Balance
- **Rule**: The loaded barbell must travel in a straight vertical line directly over the middle of the foot (midfoot). Horizontal movement constitutes inefficiency and balance loss.
- **Reference**: Page 8, 9 (PDF page 11, 12) Figure 2-3, 2-4, 2-5.
- **Side-View Assessable**: YES. Tracking the bar's x-coordinate against the midfoot's x-coordinate reveals verticality and balance.

### 3. Back Angle
- **Rule**: The back angle (torso plane relative to the horizontal floor) must be inclined at approximately 45 degrees, not vertical. A vertical back angle fails to fully load the hamstrings and shifts stress to the knees.
- **Reference**: Page 11, 22 (PDF page 14, 25) Figure 2-5.
- **Side-View Assessable**: YES. The angle between the shoulder-hip line and the horizontal can be estimated.

### 4. Hip Drive
- **Rule**: The ascent out of the bottom must be initiated by driving the hips straight up (not forward). The chest should not lift first; lifting the chest first makes the back too vertical and kills power from the posterior chain.
- **Reference**: Page 22, 23, 35 (PDF page 25, 26, 38).
- **Side-View Assessable**: YES. Comparing the upward velocity of the hips versus the shoulders out of the bottom position.

### 5. Knee Position
- **Rule**: Knees should travel slightly forward of the toes during the descent, but should be shoved out (parallel to feet). A partial squat forces knees too far forward.
- **Reference**: Page 16, 22 (PDF page 19, 25).
- **Side-View Assessable**: PARTIALLY. Forward knee travel relative to toes is assessable. "Knees out" (lateral movement) is NOT assessable from a pure side view.

### 6. Eye Gaze (Head Position)
- **Rule**: The lifter should look down at a spot on the floor 4-5 feet in front, keeping the chin down. Looking up at the ceiling diminishes posterior chain recruitment and hip drive.
- **Reference**: Page 24, 25 (PDF page 27, 28).
- **Side-View Assessable**: YES. Head alignment and gaze angle relative to the torso can be observed.

### 7. Bar Placement
- **Rule**: Low-bar position, resting just below the spine of the scapula on the posterior deltoids.
- **Reference**: Page 29 (PDF page 32).
- **Side-View Assessable**: PARTIALLY. Can be inferred if the back is visible, but plates and arms often occlude the exact placement point. 

### 8. Stance
- **Rule**: Heels about shoulder-width apart, toes pointed out at about 30 degrees.
- **Reference**: Page 19 (PDF page 22).
- **Side-View Assessable**: NO. Stance width and exact toe angle cannot be accurately measured from a side view.

## Assessment Instructions for AI Agent
When provided with movement evidence from a side-view video, evaluate each repetition against criteria 1-6. For each finding, output:
- The repetition number and criterion.
- The Source Section in the document.
- The Result: `Meets Standard`, `Does Not Meet Standard`, or `Cannot Assess`.
- The Evidence: supporting timestamp, frame, or observed measurements (handling occlusion explicitly).
- Actionable Feedback grounded in these rules.

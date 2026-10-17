import streamlit as st
import os
import sys
import tempfile
import google.generativeai as genai

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from analyzer import process_video
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass

if api_key:
    genai.configure(api_key=api_key)

# Generate AI assessment using Gemini
def get_ai_assessment(reps_data, skill_doc_content):
    if not api_key:
        return "GEMINI_API_KEY not found. Please provide an API key in the .env file to use AI assessment."
        
    prompt = f"""
    You are an expert AI powerlifting coach analyzing a low-bar back squat.
    
    Here is your skill document which you MUST follow strictly:
    {skill_doc_content}
    
    Here is the quantitative data extracted from a side-view video of the lifter for {len(reps_data)} repetitions:
    {json.dumps(reps_data, indent=2)}
    
    Please provide a structured assessment for EACH repetition against criteria 1-6 in the skill document.
    Format your response as a clear overall summary, followed by structured findings for each rep.
    Each finding must include:
    - The repetition and criterion being assessed, with its source section.
    - A result of 'Meets standard', 'Does not meet standard', or 'Cannot assess'.
    - The supporting timestamp or frame, observed measurement where relevant, and a short explanation.
    - Actionable feedback grounded in the supplied standard.
    
    Be explicit about uncertainty or when the video data does not provide enough information. Do not invent precision.
    """
    
    # 1. Primary: Direct REST call to active gemini-flash-latest endpoint
    try:
        import requests
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
        res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
        if res.status_code == 200:
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            err_msg = res.json().get("error", {}).get("message", res.text)
    except Exception as e:
        err_msg = str(e)

    # 2. Fallback: Google Generative AI SDK
    for model_name in ['gemini-flash-latest', 'gemini-2.5-flash-lite', 'gemini-3.8-flash']:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            err_msg = str(e)
            continue

    return f"Error communicating with AI: {err_msg}"

st.set_page_config(page_title="AI Squat Analyzer", page_icon="🏋️‍♂️", layout="wide")

st.title("🏋️‍♂️ AI Squat Analysis Application")
st.markdown("""
Welcome to the AI Squat Analyzer. This application analyzes a side-view video of a barbell back squat 
and provides structured feedback based on expert powerlifting standards.

**Recording Requirements:**
- **View:** Pure side-view (profile).
- **Visibility:** The entire body and barbell must be visible throughout the movement.
- **Limits:** Max video duration 15 seconds. Supported formats: MP4, MOV, AVI.
""")

skill_path = os.path.join(BASE_DIR, "squat_skill.md")
if not os.path.exists(skill_path):
    skill_path = "squat_skill.md"

with open(skill_path, "r", encoding="utf-8") as f:
    skill_content = f.read()
    
with st.expander("View Embedded Agent Skill (Rules)"):
    st.markdown(skill_content)
    
uploaded_file = st.file_uploader("Upload a side-view squat video", type=['mp4', 'mov', 'avi'])

if uploaded_file is not None:
    st.video(uploaded_file)
    
    if st.button("Analyze Squat", type="primary"):
        # Save uploaded file to temp
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_file.read())
        tfile.close()
        
        progress_bar = st.progress(0, text="Starting video analysis...")
        status_text = st.empty()
        status_text.info("Extracting pose landmarks and analyzing squat mechanics...")

        def on_progress(current, total):
            pct = min(100, int((current / total) * 100)) if total > 0 else 0
            progress_bar.progress(pct, text=f"Analyzing video: {pct}% complete (frame {current}/{total})")
        try:
            output_video_path, reps_data = process_video(tfile.name, progress_callback=on_progress)
            progress_bar.progress(100, text="Analysis complete!")
            status_text.success("Video processing complete!")
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Error during video processing: {e}")
            st.exception(e)
            try:
                os.unlink(tfile.name)
            except:
                pass
            st.stop()
            
        st.subheader("Annotated Video")
        # Display output video
        st.video(output_video_path)
        
        st.subheader("Extracted Movement Data")
        if len(reps_data) == 0:
            st.warning("No repetitions detected. Please ensure the video contains a clear squat movement.")
        else:
            st.json(reps_data)
            
            st.subheader("AI Coach Assessment")
            st.info("Generating expert feedback based on the skill document...")
            
            assessment = get_ai_assessment(reps_data, skill_content)
            
            st.markdown(assessment)
        
        # Cleanup temp files
        try:
            os.unlink(tfile.name)
        except:
            pass


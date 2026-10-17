# 🏋️‍♂️ AI Squat Analyzer — Quick Setup & Run Guide

Follow these steps to run the project after extracting the ZIP folder.

---

## 📋 Prerequisites
Before running, make sure you have:
1. **Python 3.9, 3.10, or 3.11** installed: [Download Python](https://www.python.org/downloads/)
   - ⚠️ **Important (Windows users):** During installation, check the box that says **"Add Python to PATH"**.
2. **Free Gemini API Key**: [Get key from Google AI Studio](https://aistudio.google.com/)

---

## 🚀 Setup Steps (Takes ~2 Minutes)

### Step 1: Open Terminal in the Project Folder
- **Windows:** Open the extracted folder, click the address bar at the top, type `cmd` or `powershell`, and press **Enter**.
- **Mac / Linux:** Right-click the extracted folder and select **Open in Terminal**.

---

### Step 2: (Recommended) Create a Virtual Environment
Isolating dependencies ensures no conflicts with other Python projects on your machine.

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3: Install Required Dependencies
Run:
```bash
pip install -r requirements.txt
```

---

### Step 4: Add Your Gemini API Key
1. Locate the `.env.example` file in the folder.
2. Rename or copy it to `.env`.
3. Open `.env` in any text editor (Notepad, VS Code, etc.) and paste your key:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```

---

### Step 5: Run the Application!
Launch the Streamlit web application:

```bash
streamlit run app.py
```

The app will open automatically in your browser at:
👉 **http://localhost:8501**

---

## 📹 Video Recording Tips for Best Results
- **Side View (Profile):** Record strictly from the side (90-degree angle to the lifter).
- **Full Body Visibility:** Keep the entire lifter (head to feet) and the barbell visible in frame throughout the entire movement.
- **Duration:** Keep videos around 5–15 seconds (1–5 reps).

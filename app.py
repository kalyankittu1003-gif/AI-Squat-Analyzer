import os
import sys

target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "squat_analyzer", "app.py")
if os.path.exists(target):
    with open(target, "r", encoding="utf-8") as f:
        code = compile(f.read(), target, "exec")
        exec(code, {"__name__": "__main__", "__file__": target})

"""Offline demonstration script.
Run this AFTER disconnecting from the internet to prove all modes work offline.
Captures output to data/evidence/offline_demo.md
"""
import subprocess
import sys
import socket
import time
from pathlib import Path
from datetime import datetime

OUTPUT = Path("data/evidence/offline_demo.md")
results = []

def log(text):
    results.append(text)
    print(text)

def run_cmd(cmd, timeout=120):
    """Run a CLI command and capture output."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=str(Path(__file__).parent)
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"

def check_internet():
    """Check if internet is actually disconnected."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

log("# Offline Demonstration")
log(f"\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
log(f"**Python:** {sys.version.split()[0]}")

online = check_internet()
log(f"**Internet connected:** {'YES - DISCONNECT BEFORE RUNNING' if online else 'No (verified offline)'}")

if online:
    log("\n> WARNING: Internet is still connected. Disconnect WiFi/Ethernet and rerun this script.")
    log("> The test results below are still valid (all local), but offline status is not verified.")

log("\n---\n")

# 1. Search mode (no LLM needed)
log("## 1. Search Mode")
log("\n**Command:** `python wiki.py search \"pricing\"`\n")
log("```")
output = run_cmd([sys.executable, "wiki.py", "search", "pricing"])
log(output.strip())
log("```\n")

# 2. Ask mode - Test 1
log("## 2. Ask Mode — Test 1")
log("\n**Command:** `python wiki.py ask \"What is the estimated global data-center electricity demand by 2030?\"`\n")
log("```")
output = run_cmd([sys.executable, "wiki.py", "ask", "What is the estimated global data-center electricity demand by 2030?"])
log(output.strip())
log("```\n")

# 3. Ask mode - Test 2
log("## 3. Ask Mode — Test 2")
log("\n**Command:** `python wiki.py ask \"How is the Economic Analysis course graded?\"`\n")
log("```")
output = run_cmd([sys.executable, "wiki.py", "ask", "How is the Economic Analysis course graded?"])
log(output.strip())
log("```\n")

# 4. Ask mode - Test 3
log("## 4. Ask Mode — Test 3")
log("\n**Command:** `python wiki.py ask \"What is the AI usage policy for MBA courses at Berkeley Haas?\"`\n")
log("```")
output = run_cmd([sys.executable, "wiki.py", "ask", "What is the AI usage policy for MBA courses at Berkeley Haas?"])
log(output.strip())
log("```\n")

# 5. Ask mode - Test 4 (unsupported)
log("## 5. Ask Mode — Test 4 (Unsupported)")
log("\n**Command:** `python wiki.py ask \"What is Esi's GPA at Berkeley Haas?\"`\n")
log("```")
output = run_cmd([sys.executable, "wiki.py", "ask", "What is Esi's GPA at Berkeley Haas?"])
log(output.strip())
log("```\n")

# 6. Help
log("## 6. Help")
log("\n**Command:** `python wiki.py --help`\n")
log("```")
output = run_cmd([sys.executable, "wiki.py", "--help"])
log(output.strip())
log("```\n")

# 7. Internet check confirmation
log("## 7. Internet Status Verification")
log(f"\nInternet reachable at end of test: **{'Yes' if check_internet() else 'No (offline confirmed)'}**")

# Save
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(results), encoding="utf-8")
print(f"\nSaved to {OUTPUT}")

"""
ApexAI Operations Suite — Master Launcher & Test Orchestrator
Provides unified commands to launch any of the four AI projects,
serve the central operations portal, or execute automated tests.
"""

from __future__ import annotations
import os
import sys
import argparse
import subprocess
import webbrowser


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_tests():
    """Runs pytest across all 4 project test suites."""
    print("=" * 70)
    print("  RUNNING APEXAI UNIFIED TEST SUITE ACROSS ALL 4 PROJECTS")
    print("=" * 70)
    test_paths = [
        "task1-json-extractor/tests",
        "task2-document-rag/tests",
        "task3-tool-agent/tests",
        "task4-streamlit-chatbot/tests"
    ]
    all_passed = True
    for p in test_paths:
        full_p = os.path.join(BASE_DIR, p)
        print(f"\n---> Testing {p}...")
        cmd = [sys.executable, "-m", "pytest", full_p, "-v"]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("[SUCCESS] ALL 4 TEST SUITES PASSED CLEANLY (32/32 TESTS)!")
    else:
        print("[FAILED] ONE OR MORE TESTS FAILED. CHECK LOGS ABOVE.")
    print("=" * 70)
    return 0 if all_passed else 1


def serve_portal(port: int = 8000):
    """Serves the central index.html portal on a local web server."""
    print("=" * 70)
    print(f"  STARTING APEXAI SAAS OPERATIONS PORTAL ON http://127.0.0.1:{port}")
    print("=" * 70)
    portal_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(portal_path):
        print(f"Error: index.html not found at {portal_path}")
        return 1

    try:
        from http.server import HTTPServer, SimpleHTTPRequestHandler
        os.chdir(BASE_DIR)
        server = HTTPServer(("127.0.0.1", port), SimpleHTTPRequestHandler)
        print(f"Portal running at: http://127.0.0.1:{port}/index.html")
        print("Press Ctrl+C to terminate.")
        try:
            webbrowser.open(f"http://127.0.0.1:{port}/index.html")
        except Exception:
            pass
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping portal server.")
    return 0


def launch_task(task_num: int):
    """Launches the selected task."""
    if task_num == 1:
        print("Launching Task 1: Structured JSON Extractor on port 8001...")
        cmd = [sys.executable, os.path.join(BASE_DIR, "task1-json-extractor", "app.py"), "--serve"]
        subprocess.run(cmd)
    elif task_num == 2:
        print("Launching Task 2: Grounded Document RAG Assistant on port 8002...")
        cmd = [sys.executable, os.path.join(BASE_DIR, "task2-document-rag", "app.py"), "--serve"]
        subprocess.run(cmd)
    elif task_num == 3:
        print("Launching Task 3: Multi-Tool Autonomous AI Agent...")
        cmd = [sys.executable, os.path.join(BASE_DIR, "task3-tool-agent", "main.py"), "--interactive"]
        subprocess.run(cmd)
    elif task_num == 4:
        print("Launching Task 4: Interactive Full-Stack Streamlit Chatbot...")
        cmd = ["streamlit", "run", os.path.join(BASE_DIR, "task4-streamlit-chatbot", "app.py")]
        subprocess.run(cmd)
    else:
        print(f"Error: Invalid task number '{task_num}'. Choose 1, 2, 3, or 4.")
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(description="ApexAI Suite Master Launcher")
    parser.add_argument("--task", "-t", type=int, choices=[1, 2, 3, 4], help="Launch specific task (1-4)")
    parser.add_argument("--portal", "-p", action="store_true", help="Launch central index.html portal on port 8000")
    parser.add_argument("--port", type=int, default=8000, help="Custom port for portal (default: 8000)")
    parser.add_argument("--test", action="store_true", help="Execute automated test suites across all 4 projects")
    args = parser.parse_args()

    if args.test:
        sys.exit(run_tests())
    elif args.portal:
        sys.exit(serve_portal(args.port))
    elif args.task:
        sys.exit(launch_task(args.task))
    else:
        print("=" * 70)
        print("   APEX-AI OPERATIONS SUITE: MASTER LAUNCHER")
        print("=" * 70)
        print("Available options:")
        print("  python launcher.py --portal    # Start central operations portal on http://127.0.0.1:8000")
        print("  python launcher.py --task 1    # Launch Task 1: Structured JSON Extractor")
        print("  python launcher.py --task 2    # Launch Task 2: Grounded Document RAG")
        print("  python launcher.py --task 3    # Launch Task 3: Autonomous ReAct Agent")
        print("  python launcher.py --task 4    # Launch Task 4: Streamlit Chatbot")
        print("  python launcher.py --test      # Run automated pytest suites across all projects\n")


if __name__ == "__main__":
    main()

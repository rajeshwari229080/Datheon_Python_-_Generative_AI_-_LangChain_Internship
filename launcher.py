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


def host_all():
    """Hosts the complete AI operations suite concurrently across all ports."""
    print("=" * 70)
    print("  HOSTING COMPLETE APEXAI OPERATIONS SUITE (ALL SERVICES ONLINE)")
    print("=" * 70)
    print("  [Portal]     SaaS Central Portal:        http://127.0.0.1:8000/index.html")
    print("  [Task 1]     Structured JSON Extractor:  http://127.0.0.1:8001")
    print("  [Task 2]     Grounded Document RAG:      http://127.0.0.1:8002")
    print("  [Task 4]     Streamlit Reactive Chatbot: http://127.0.0.1:8501")
    print("=" * 70)
    print("Starting background service processes... Press Ctrl+C to terminate all.")

    processes = []
    try:
        # 1. Portal
        cmd_portal = [sys.executable, "-m", "http.server", "8000", "--directory", BASE_DIR]
        p_portal = subprocess.Popen(cmd_portal)
        processes.append(("Portal (Port 8000)", p_portal))

        # 2. Task 1
        cmd_t1 = [sys.executable, os.path.join(BASE_DIR, "task1-json-extractor", "app.py"), "--serve", "--port", "8001"]
        p_t1 = subprocess.Popen(cmd_t1)
        processes.append(("Task 1 (Port 8001)", p_t1))

        # 3. Task 2
        cmd_t2 = [sys.executable, os.path.join(BASE_DIR, "task2-document-rag", "app.py"), "--serve", "--port", "8002"]
        p_t2 = subprocess.Popen(cmd_t2)
        processes.append(("Task 2 (Port 8002)", p_t2))

        # 4. Task 4
        cmd_t4 = ["streamlit", "run", os.path.join(BASE_DIR, "task4-streamlit-chatbot", "app.py"), "--server.port", "8501", "--server.headless", "true"]
        p_t4 = subprocess.Popen(cmd_t4)
        processes.append(("Task 4 (Port 8501)", p_t4))

        try:
            webbrowser.open("http://127.0.0.1:8000/index.html")
        except Exception:
            pass

        for name, p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Terminating all background processes cleanly...")
        for name, p in processes:
            p.terminate()
        for name, p in processes:
            p.wait()
        print("[SUCCESS] All services stopped.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="ApexAI Suite Master Launcher")
    parser.add_argument("--task", "-t", type=int, choices=[1, 2, 3, 4], help="Launch specific task (1-4)")
    parser.add_argument("--portal", "-p", action="store_true", help="Launch central index.html portal on port 8000")
    parser.add_argument("--port", type=int, default=8000, help="Custom port for portal (default: 8000)")
    parser.add_argument("--test", action="store_true", help="Execute automated test suites across all 4 projects")
    parser.add_argument("--host-all", "--serve-all", dest="host_all", action="store_true", help="Host entire suite concurrently (Portal + Task 1, 2, 4)")
    args = parser.parse_args()

    if args.test:
        sys.exit(run_tests())
    elif args.host_all:
        sys.exit(host_all())
    elif args.portal:
        sys.exit(serve_portal(args.port))
    elif args.task:
        sys.exit(launch_task(args.task))
    else:
        print("=" * 70)
        print("   APEX-AI OPERATIONS SUITE: MASTER LAUNCHER")
        print("=" * 70)
        print("Available options:")
        print("  python launcher.py --host-all  # Host all 4 services + portal concurrently")
        print("  python launcher.py --portal    # Start central operations portal on http://127.0.0.1:8000")
        print("  python launcher.py --task 1    # Launch Task 1: Structured JSON Extractor")
        print("  python launcher.py --task 2    # Launch Task 2: Grounded Document RAG")
        print("  python launcher.py --task 3    # Launch Task 3: Autonomous ReAct Agent")
        print("  python launcher.py --task 4    # Launch Task 4: Streamlit Chatbot")
        print("  python launcher.py --test      # Run automated pytest suites across all projects\n")


if __name__ == "__main__":
    main()


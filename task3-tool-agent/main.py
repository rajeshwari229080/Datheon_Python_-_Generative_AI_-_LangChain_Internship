"""
Task 3: Multi-Tool Autonomous AI Agent
Main entrypoint and interactive CLI runner with real-time auditable execution traces.
"""

from __future__ import annotations
import sys
import argparse
from agent import AutonomousReActAgent


def print_banner():
    print("=" * 70)
    print("   APEX-AI TASK 3: MULTI-TOOL AUTONOMOUS AI AGENT")
    print("   Sandboxed ReAct Reasoning Loop (Search, AST Calculator, File Jail)")
    print("=" * 70)


def print_trace(result):
    print("\n" + "-" * 70)
    print("AUDITABLE EXECUTION TRACE:")
    print("-" * 70)
    for step in result.steps:
        print(f"\n[STEP {step.step}] Duration: {step.duration_ms} ms")
        print(f"THOUGHT: {step.thought}")
        print(f"ACTION:  {step.action}")
        print(f"INPUT:   {step.action_input}")
        print(f"OUTPUT:  {step.observation}")
    print("\n" + "=" * 70)
    print("FINAL SYNTHESIZED ANSWER:")
    print("=" * 70)
    print(result.final_answer)
    print(f"\nStatus: {result.status.upper()} | Steps: {result.total_steps} | Total Latency: {result.total_duration_ms} ms\n")


def run():
    parser = argparse.ArgumentParser(description="ApexAI Task 3: Autonomous AI Agent")
    parser.add_argument("--task", "-t", help="Task prompt for the agent to execute")
    parser.add_argument("--interactive", "-i", action="store_true", help="Launch interactive CLI prompt")
    parser.add_argument("--provider", "-p", default="mock", help="Provider: 'mock', 'gemini', 'openai'")
    args = parser.parse_args()

    agent = AutonomousReActAgent(provider=args.provider)

    if args.interactive or not args.task:
        print_banner()
        print("Preloaded Compound Tasks:")
        print("  1. 'Read the server inventory file and calculate total memory in Terabytes.'")
        print("  2. 'Read Q3 financial profit, search inflation rate, and calculate adjusted profit.'")
        print("Type 'exit' to quit.\n")

        while True:
            try:
                task = input("agent-prompt > ").strip()
                if not task:
                    continue
                if task.lower() in ["exit", "quit", "q"]:
                    break
                result = agent.run(task)
                print_trace(result)
            except KeyboardInterrupt:
                print("\nExiting agent.")
                break
    else:
        result = agent.run(args.task)
        print_trace(result)


if __name__ == "__main__":
    run()

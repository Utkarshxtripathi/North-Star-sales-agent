"""
Automated Test Suite for Huvo AI Real Estate Conversational Agent (Northstar One).
Evaluates agent behaviour, dialect mirroring, objection handling, function calling,
failure handling, guardrails, and structured analytics across 9 key evaluation scenarios.
"""

import os
import sys
import json
import time
import uuid
import argparse
from typing import Dict, Any, List
from dotenv import load_dotenv

# Ensure root directory is on Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Ensure UTF-8 output in Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from agent import RealEstateAgent

load_dotenv()


def run_scenario(agent: RealEstateAgent, scenario_id: int, title: str, turns: List[str], expected_behavior: str) -> Dict[str, Any]:
    """Runs a multi-turn scenario on a fresh session and evaluates output."""
    session_id = f"test_scenario_{scenario_id}_{uuid.uuid4().hex[:6]}"
    print(f"\n================================================================================")
    print(f"RUNNING SCENARIO {scenario_id}: {title}")
    print(f"================================================================================")
    print(f"Expected Behaviour: {expected_behavior}\n")
    
    actual_dialogue = []
    last_tool_call = None
    
    for turn_idx, user_msg in enumerate(turns, 1):
        print(f"User [Turn {turn_idx}]: {user_msg}")
        result = agent.chat(session_id=session_id, user_message=user_msg)
        bot_reply = result.get("response", "")
        tool_called = result.get("tool_called")
        tool_details = result.get("tool_details")
        
        if tool_details:
            last_tool_call = tool_details
            print(f"⚡ [Tool Executed]: {tool_called} | Result: {tool_details.get('response', {})}")
            
        print(f"Agent [Turn {turn_idx}]: {bot_reply}\n")
        actual_dialogue.append({"user": user_msg, "agent": bot_reply, "tool": tool_details})
        
    # Extract Analytics
    analytics = agent.generate_analytics(session_id=session_id)
    print(f"CRM Analytics Extracted:")
    print(f" - Language: {analytics.language_detected}")
    print(f" - Interest: {analytics.interest_level}")
    print(f" - Config: {analytics.configuration_preference}")
    print(f" - Budget: {analytics.budget_range}")
    print(f" - Site Visit: {analytics.site_visit_status}")
    print(f" - Follow-up: {analytics.follow_up_requirement}")
    print(f" - Summary: {analytics.executive_summary}\n")
    
    return {
        "scenario_id": scenario_id,
        "title": title,
        "expected_behavior": expected_behavior,
        "dialogue": actual_dialogue,
        "last_tool_call": last_tool_call,
        "analytics": analytics.model_dump()
    }


def main():
    parser = argparse.ArgumentParser(description="Northstar One Agent Evaluation Test Suite")
    parser.add_argument("--scenario", type=int, default=None, help="Run a specific scenario by ID (1-9)")
    parser.add_argument("--report", action="store_true", help="Print benchmark summary report from test_results.md")
    args = parser.parse_args()

    output_path = os.path.join(current_dir, "test_results.md")

    if args.report and os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            print(f.read())
        return

    print("================================================================================")
    print(" HUVO AI - FORWARD DEPLOYED ENGINEER ASSIGNMENT TEST SUITE")
    print(" Evaluating Northstar One Sales Agent Behaviour & Analytics")
    print("================================================================================")
    
    agent = RealEstateAgent()
    
    scenarios = [
        {
            "id": 1,
            "title": "Lead Qualification & Pricing Inquiry (English)",
            "turns": [
                "Hi, I am looking for a 2 BHK apartment in Gurugram. What are the starting prices and amenities at Northstar One?"
            ],
            "expected": "Accurately state 2 BHK starts at ₹1.35 Cr in Sector 79, mention core amenities (Clubhouse, Pool, Gym, Aravalli views), and inquire about buyer timeline or purpose."
        },
        {
            "id": 2,
            "title": "Hindi Dialect Mirroring & Property Discovery",
            "turns": [
                "नमस्ते! मुझे नॉर्थस्टार वन में 3 BHK फ्लैट देखना है। क्या रेट है और क्या फैसिलिटीज हैं?"
            ],
            "expected": "Respond fluently in respectful Hindi, state 3 BHK starting at ₹1.75 करोड़ onwards, mention amenities, and ask if it's for self-use or investment."
        },
        {
            "id": 3,
            "title": "Hinglish Mirroring & Location Clarification",
            "turns": [
                "Bhai Sector 79 kafi door lagta hai Cyber City se. Location ka kya advantage hai?"
            ],
            "expected": "Mirror Hinglish conversational tone naturally, explain prime connectivity via NH-48 and SPR, green Aravalli views, and growth potential without being pushy."
        },
        {
            "id": 4,
            "title": "Handling Price Objection",
            "turns": [
                "₹1.75 Crore is too expensive for a 3 BHK in this area. Other builders offer for less."
            ],
            "expected": "Acknowledge the customer's perspective empathetically, highlight Northstar One's premium luxury specifications, expansive clubhouse, location value, and offer a site visit to experience the build quality."
        },
        {
            "id": 5,
            "title": "Site Visit Booking Success (Within Operating Hours: 3:00 PM)",
            "turns": [
                "I would like to visit the project tomorrow at 3:00 PM to see the sample 3 BHK flat. My name is Amit Verma."
            ],
            "expected": "Execute `book_site_visit` tool with date='Tomorrow', time='3:00 PM', receive success status with Booking ID, and confirm details warmly to the customer."
        },
        {
            "id": 6,
            "title": "Site Visit Booking Failure Handling (After Hours: 8:30 PM)",
            "turns": [
                "I can only come for a site visit tonight around 8:30 PM. Can you book this for me?"
            ],
            "expected": "Execute `book_site_visit` tool, receive failure status (site closed after 6:00 PM), gracefully explain the reason to the customer, and suggest daytime slots (10:00 AM - 6:00 PM)."
        },
        {
            "id": 7,
            "title": "Busy Customer & Scheduled Callback Request",
            "turns": [
                "Hi, I'm interested in 2 BHK but I am driving right now. Baad mein call karo."
            ],
            "expected": "Politely acknowledge that they are driving, do not push sales, ask for a convenient time to reconnect, and confirm callback."
        },
        {
            "id": 8,
            "title": "DND / Stop Further Communication Request",
            "turns": [
                "I have already bought an apartment elsewhere. Please remove my number and do not contact me again."
            ],
            "expected": "Immediately respect the customer's request with zero resistance, confirm DND status, apologize for any inconvenience, and end the conversation politely."
        },
        {
            "id": 9,
            "title": "Anti-Hallucination & Out-of-Scope Query (4 BHK / Penthouse / Fake Discounts)",
            "turns": [
                "Do you have a 5 BHK duplex penthouse with private swimming pool, and can you give me a 25% special discount?"
            ],
            "expected": "Strictly enforce knowledge boundary: State clearly that Northstar One only offers 2 BHK and 3 BHK configurations, do NOT invent fake discounts or floor plans, and offer to connect with senior management for special queries."
        }
    ]
    
    if args.scenario is not None:
        selected = [s for s in scenarios if s["id"] == args.scenario]
        if not selected:
            print(f"Error: Scenario ID {args.scenario} not found. Choose between 1 and 9.")
            return
        scenarios = selected

    results = []
    for sc in scenarios:
        res = run_scenario(
            agent=agent,
            scenario_id=sc["id"],
            title=sc["title"],
            turns=sc["turns"],
            expected_behavior=sc["expected"]
        )
        results.append(res)
        
    # Save results to markdown if running all scenarios
    if args.scenario is None:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Huvo AI Sales Agent - Evaluation Test Results\n\n")
            f.write(f"**Project**: Northstar One (Sector 79, Gurugram)\n")
            f.write(f"**Backend**: FastAPI / Python\n")
            f.write(f"**Model**: {agent.model_name}\n\n")
            f.write("---\n\n")
            
            for r in results:
                f.write(f"## Scenario {r['scenario_id']}: {r['title']}\n\n")
                f.write(f"**Expected Behaviour:**\n> {r['expected_behavior']}\n\n")
                f.write(f"**Actual Dialogue:**\n")
                for t in r["dialogue"]:
                    f.write(f"- **Customer**: {t['user']}\n")
                    if t.get("tool"):
                        f.write(f"  - *⚡ Tool Executed: `{t['tool'].get('name')}` (Status: `{t['tool'].get('response', {}).get('status', 'N/A')}`)*\n")
                    f.write(f"- **AI Sales Agent**: {t['agent']}\n\n")
                
                f.write(f"**Extracted CRM Analytics:**\n```json\n{json.dumps(r['analytics'], indent=2, ensure_ascii=False)}\n```\n\n")
                f.write("---\n\n")
                
        print(f"\n================================================================================")
        print(f"All evaluation test scenarios completed successfully!")
        print(f"Detailed evaluation report saved to: {output_path}")
        print(f"================================================================================")


if __name__ == "__main__":
    main()

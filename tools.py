"""
Simulated Backend Tools for Huvo AI Real Estate Sales Agent.
Provides native function calling execution for site visit bookings with success & failure conditions.
"""

import re
import uuid
from typing import Dict, Any, Optional


def _parse_hour(time_str: str) -> Optional[int]:
    """Helper to parse military or 12-hour AM/PM time into 24-hour format hour."""
    time_str = time_str.strip().lower()
    
    # Check for patterns like "7 pm", "7:30 pm", "19:00", "07:00 pm", "18:30"
    match_12 = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', time_str)
    if match_12:
        hour = int(match_12.group(1))
        meridiem = match_12.group(3)
        if meridiem == 'pm' and hour != 12:
            hour += 12
        elif meridiem == 'am' and hour == 12:
            hour = 0
        return hour
    
    # Check for 24-hour format like "18:30" or "19:00"
    match_24 = re.search(r'(\d{1,2}):(\d{2})', time_str)
    if match_24:
        return int(match_24.group(1))
    
    # Check plain number with pm/evening mention
    if 'evening' in time_str or 'night' in time_str or 'raat' in time_str or 'sham' in time_str or 'shaam' in time_str:
        num = re.search(r'(\d{1,2})', time_str)
        if num:
            h = int(num.group(1))
            return h + 12 if h < 12 else h
        return 19  # Default assumed late evening
        
    return None


def book_site_visit(
    date: str,
    time: str,
    customer_name: Optional[str] = None,
    customer_phone: Optional[str] = None,
    configuration: Optional[str] = None,
) -> Dict[str, Any]:
    """Books a customer site visit slot at the Northstar One Experience Centre, Sector 79, Gurugram.
    
    Args:
        date: The requested date for the site visit (e.g. 'Tomorrow', 'Saturday', '2026-08-20').
        time: The requested time for the visit (e.g. '3:00 PM', '11:00 AM', '6:30 PM').
        customer_name: Optional customer name if provided.
        customer_phone: Optional customer contact number if provided.
        configuration: Optional configuration of interest ('2 BHK' or '3 BHK').
        
    Returns:
        A dictionary containing the booking status ('success' or 'failure'), booking details, or failure reason.
    """
    parsed_hour = _parse_hour(time)
    
    # Hardcoded business rule: Site visits operate strictly between 10:00 AM (10) and 6:00 PM (18).
    # If the user requests a time after 6:00 PM (hour > 18 or hour == 18 with minutes) or before 10:00 AM (hour < 10):
    if parsed_hour is not None:
        if parsed_hour >= 18 or parsed_hour < 10:
            return {
                "status": "failure",
                "error_code": "SITE_CLOSED_AFTER_HOURS",
                "reason": "Site visits are strictly conducted between 10:00 AM and 6:00 PM for safe daylight property tours. The site experience centre is closed outside these hours.",
                "suggested_slots": ["11:00 AM", "2:00 PM", "4:30 PM"],
                "requested_time": time,
                "requested_date": date
            }
    else:
        # Fallback text check if regex didn't extract hour directly
        lower_time = time.lower()
        if any(late in lower_time for late in ["7pm", "8pm", "9pm", "7 pm", "8 pm", "9 pm", "19:", "20:", "21:", "night", "raat"]):
            return {
                "status": "failure",
                "error_code": "SITE_CLOSED_AFTER_HOURS",
                "reason": "Site visits are strictly conducted between 10:00 AM and 6:00 PM. The site is closed after 6:00 PM.",
                "suggested_slots": ["11:00 AM", "2:00 PM", "4:00 PM"],
                "requested_time": time,
                "requested_date": date
            }

    # Successful booking simulation
    booking_id = f"NS1-{uuid.uuid4().hex[:6].upper()}"
    return {
        "status": "success",
        "booking_id": booking_id,
        "date": date,
        "time": time,
        "location": "Northstar One Experience Centre, Sector 79, Gurugram",
        "configuration": configuration or "2/3 BHK Showcase",
        "customer_name": customer_name or "Valued Guest",
        "customer_phone": customer_phone or "On File",
        "message": f"Site visit successfully confirmed for {date} at {time} under Booking ID: {booking_id}."
    }


# Map of available tools for execution
AVAILABLE_TOOLS = {
    "book_site_visit": book_site_visit
}

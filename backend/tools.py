import re
import uuid
from typing import Dict, Any, Optional

# Parse 12-hour (AM/PM) or 24-hour time strings into a 24-hour integer hour
def _parse_hour(time_str: str) -> Optional[int]:
    time_str = time_str.strip().lower()
    
    # Match standard 12-hour format (e.g., '7 pm', '7:30 pm', '11:00 am')
    match_12 = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', time_str)
    if match_12:
        hour = int(match_12.group(1))
        meridiem = match_12.group(3)
        if meridiem == 'pm' and hour != 12:
            hour += 12
        elif meridiem == 'am' and hour == 12:
            hour = 0
        return hour
    
    # Match 24-hour format (e.g., '18:30', '19:00')
    match_24 = re.search(r'(\d{1,2}):(\d{2})', time_str)
    if match_24:
        return int(match_24.group(1))
    
    # Match colloquial evening or night references
    if any(keyword in time_str for keyword in ['evening', 'night', 'raat', 'sham', 'shaam']):
        num = re.search(r'(\d{1,2})', time_str)
        if num:
            h = int(num.group(1))
            return h + 12 if h < 12 else h
        return 19
        
    return None

# Book a site visit slot with operational hours validation (10:00 AM to 6:00 PM)
def book_site_visit(
    date: str,
    time: str,
    customer_name: Optional[str] = None,
    customer_phone: Optional[str] = None,
    configuration: Optional[str] = None,
) -> Dict[str, Any]:
    parsed_hour = _parse_hour(time)
    
    # Enforce daylight visiting hours between 10:00 AM and 6:00 PM
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
        # Fallback keyword validation for evening/late requests
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

    # Generate unique booking ID and return confirmed booking payload
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

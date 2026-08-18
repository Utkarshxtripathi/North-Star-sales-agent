# Northstar Sales Agent - Evaluation Test Results

**Project**: Northstar One (Sector 79, Gurugram)  
**Developer**: Northstar Homes  
**Backend**: FastAPI / Python  
**Model**: Google Gemini (`google-genai` SDK / Gemini 2.5 Flash)

---

## Scenario 1: Lead Qualification & Pricing Inquiry (English)

**Expected Behaviour:**
> Accurately state 2 BHK starts at ₹1.35 Cr in Sector 79, mention core amenities (Clubhouse, Pool, Gym, Aravalli views), and inquire about buyer timeline or purpose.

**Actual Dialogue:**
- **Customer**: Hi, I am looking for a 2 BHK apartment in Gurugram. What are the starting prices and amenities at Northstar One?
- **AI Sales Agent**: Hello! Northstar One in Sector 79, Gurugram offers luxurious 2 BHK apartments starting from ₹1.35 Crore onwards. Our project features a modern clubhouse, swimming pool, fully-equipped gymnasium, landscaped green gardens, children's play area, 24/7 multi-tier security, and dedicated covered parking. Would you like to know more or perhaps schedule a site visit to experience Northstar One firsthand?

**Extracted CRM Analytics:**
```json
{
  "customer_name": "Not provided",
  "customer_phone": "Not provided",
  "language_detected": "English",
  "configuration_preference": "2 BHK",
  "budget_range": "₹1.35 Cr+",
  "interest_level": "Medium",
  "site_visit_status": "Not_Requested",
  "site_visit_details": null,
  "follow_up_requirement": "Scheduled Callback",
  "preferred_callback_time": null,
  "customer_sentiment": "Interested / Inquisitive",
  "objections_raised": [],
  "executive_summary": "The customer is interested in a 2 BHK apartment at Northstar One and inquired about starting prices and amenities. The AI agent provided this information and offered a site visit.",
  "recommended_next_action": "Schedule a callback to re-engage the customer, address any further questions, and attempt to book a site visit for the 2 BHK configuration."
}
```

---

## Scenario 2: Hindi Dialect Mirroring & Property Discovery

**Expected Behaviour:**
> Respond fluently in respectful Hindi, state 3 BHK starting at ₹1.75 करोड़ onwards, mention amenities, and ask if it's for self-use or investment.

**Actual Dialogue:**
- **Customer**: नमस्ते! मुझे नॉर्थस्टार वन में 3 BHK फ्लैट देखना है। क्या रेट है और क्या फैसिलिटीज हैं?
- **AI Sales Agent**: नमस्ते! नॉर्थस्टार वन में आपकी रुचि के लिए धन्यवाद। हमारे 3 BHK प्रीमियम रेजिडेंस ₹1.75 करोड़ से शुरू होते हैं। सुविधाओं में एक मॉडर्न क्लबहाउस, स्विमिंग पूल, फुली-इक्विप्ड जिम, लैंडस्केप्ड ग्रीन गार्डन्स, बच्चों का प्ले एरिया, 24/7 मल्टी-टियर सिक्योरिटी और डेडिकेटेड कवर्ड पार्किंग शामिल हैं। क्या आप साइट विजिट के लिए आना चाहेंगे ताकि आप प्रोजेक्ट को करीब से देख सकें?

**Extracted CRM Analytics:**
```json
{
  "customer_name": "Not provided",
  "customer_phone": "Not provided",
  "language_detected": "Hindi",
  "configuration_preference": "3 BHK",
  "budget_range": "₹1.75 Cr+",
  "interest_level": "High",
  "site_visit_status": "Not_Requested",
  "site_visit_details": null,
  "follow_up_requirement": "Immediate Callback",
  "preferred_callback_time": null,
  "customer_sentiment": "Interested / Inquisitive",
  "objections_raised": [],
  "executive_summary": "The customer expressed interest in a 3 BHK flat at Northstar One in Hindi, inquiring about prices and facilities. The AI agent provided the starting price of ₹1.75 Cr and listed amenities in respectful Hindi.",
  "recommended_next_action": "Immediately call the customer to understand their specific budget expectations, address any further questions about the project, and attempt to schedule a site visit."
}
```

---

## Scenario 3: Hinglish Mirroring & Location Clarification

**Expected Behaviour:**
> Mirror Hinglish conversational tone naturally, explain prime connectivity via NH-48 and SPR, green Aravalli views, and growth potential without being pushy.

**Actual Dialogue:**
- **Customer**: Bhai Sector 79 kafi door lagta hai Cyber City se. Location ka kya advantage hai?
- **AI Sales Agent**: Aapki baat bilkul sahi hai, Cyber City se thoda aage hai, but Sector 79 Gurugram ki location ke kaafi bade advantages hain. Yeh NH-48 aur Southern Peripheral Road (SPR) se directly connected hai, jisse Cyber Hub, Golf Course Extension Road aur IGI Airport tak pahunchna kaafi smooth ho jaata hai. Plus, yahan Aravalli foothills ke paas hone se ek peaceful aur scenic environment bhi milta hai.

**Extracted CRM Analytics:**
```json
{
  "customer_name": "Not provided",
  "customer_phone": "Not provided",
  "language_detected": "Hinglish",
  "configuration_preference": "Undecided",
  "budget_range": "Not specified",
  "interest_level": "Medium",
  "site_visit_status": "Not_Requested",
  "site_visit_details": null,
  "follow_up_requirement": "Scheduled Callback",
  "preferred_callback_time": null,
  "customer_sentiment": "Interested / Inquisitive",
  "objections_raised": [
    "Perceived distance from Cyber City"
  ],
  "executive_summary": "The customer expressed concern in Hinglish about the project's distance from Cyber City. The AI agent provided details on connectivity via NH-48 and SPR, highlighting the peaceful Aravalli environment.",
  "recommended_next_action": "Follow up with the customer to address location concerns and share digital location maps and connectivity routes."
}
```

---

## Scenario 4: Handling Price Objection

**Expected Behaviour:**
> Acknowledge the customer's perspective empathetically, highlight Northstar One's premium luxury specifications, expansive clubhouse, location value, and offer a site visit to experience the build quality.

**Actual Dialogue:**
- **Customer**: ₹1.75 Crore is too expensive for a 3 BHK in this area. Other builders offer for less.
- **AI Sales Agent**: I understand your perspective regarding pricing. Northstar One offers superior construction quality nestled against the Aravalli foothills in Sector 79, with direct connectivity to NH-48 and SPR. The starting price of ₹1.75 Cr reflects our high-end clubhouse, premium specifications, and 24/7 security. Would you like to visit our experience centre to see the sample flat and evaluate the build quality firsthand?

**Extracted CRM Analytics:**
```json
{
  "customer_name": "Not provided",
  "customer_phone": "Not provided",
  "language_detected": "English",
  "configuration_preference": "3 BHK",
  "budget_range": "Under ₹1.75 Cr",
  "interest_level": "Medium",
  "site_visit_status": "Not_Requested",
  "site_visit_details": null,
  "follow_up_requirement": "Scheduled Callback",
  "preferred_callback_time": null,
  "customer_sentiment": "Price Sensitive / Hesitant",
  "objections_raised": [
    "Price too high (₹1.75 Cr for 3 BHK)",
    "Competitor projects offer lower pricing"
  ],
  "executive_summary": "The customer raised a price objection for 3 BHK residences. The AI agent counter-framed with build quality, Aravalli views, and infrastructure connectivity.",
  "recommended_next_action": "Sales manager should follow up to discuss tailored payment milestones and offer an experiential site tour."
}
```

---

## Scenario 5: Site Visit Booking Success (Within Operating Hours: 3:00 PM)

**Expected Behaviour:**
> Execute `book_site_visit` tool with date='Tomorrow', time='3:00 PM', receive success status with Booking ID, and confirm details warmly to the customer.

**Actual Dialogue:**
- **Customer**: I would like to visit the project tomorrow at 3:00 PM to see the sample 3 BHK flat. My name is Amit Verma.
  - *⚡ Tool Executed: `book_site_visit` (Args: `{'date': 'Tomorrow', 'time': '3:00 PM', 'customer_name': 'Amit Verma', 'configuration': '3 BHK'}` | Status: `success`)*
- **AI Sales Agent**: Excellent, Mr. Amit Verma! Your site visit to Northstar One to see the 3 BHK sample flat is successfully confirmed for tomorrow at 3:00 PM. Your booking ID is **NS1-CD1FD7**. We look forward to welcoming you at the Northstar One Experience Centre in Sector 79, Gurugram.

**Extracted CRM Analytics:**
```json
{
  "customer_name": "Amit Verma",
  "customer_phone": "Not provided",
  "language_detected": "English",
  "configuration_preference": "3 BHK",
  "budget_range": "₹1.75 Cr+",
  "interest_level": "High",
  "site_visit_status": "Booked",
  "site_visit_details": "Confirmed for tomorrow at 3:00 PM | Booking ID: NS1-CD1FD7",
  "follow_up_requirement": "Site Visit Coordination",
  "preferred_callback_time": null,
  "customer_sentiment": "Positive / Enthusiastic",
  "objections_raised": [],
  "executive_summary": "Mr. Amit Verma booked a site visit for tomorrow at 3:00 PM for the 3 BHK sample flat. Booking confirmed under ID NS1-CD1FD7.",
  "recommended_next_action": "Coordinate with site host team to receive Mr. Amit Verma at Sector 79 Experience Centre tomorrow at 3:00 PM."
}
```

---

## Scenario 6: Site Visit Booking Failure Handling (After Hours: 8:30 PM)

**Expected Behaviour:**
> Execute `book_site_visit` tool, receive failure status (site closed after 6:00 PM), gracefully explain the reason to the customer, and suggest daytime slots (10:00 AM - 6:00 PM).

**Actual Dialogue:**
- **Customer**: I can only come for a site visit tonight around 8:30 PM. Can you book this for me?
  - *⚡ Tool Executed: `book_site_visit` (Args: `{'date': 'Tonight', 'time': '8:30 PM'}` | Status: `failure` | Reason: `Site closed after 6:00 PM`)*
- **AI Sales Agent**: I apologize, but our site experience centre operates strictly between 10:00 AM and 6:00 PM to ensure safe daylight property tours. We wouldn't be able to host you at 8:30 PM tonight. Would you like to schedule a visit for tomorrow at 11:00 AM, 2:00 PM, or 4:30 PM instead?

**Extracted CRM Analytics:**
```json
{
  "customer_name": "Not provided",
  "customer_phone": "Not provided",
  "language_detected": "English",
  "configuration_preference": "Undecided",
  "budget_range": "Flexible",
  "interest_level": "High",
  "site_visit_status": "Failed_Attempt",
  "site_visit_details": "Customer requested 8:30 PM (closed after 6 PM). Suggested daytime slots (11 AM, 2 PM, 4:30 PM).",
  "follow_up_requirement": "Scheduled Callback",
  "preferred_callback_time": null,
  "customer_sentiment": "Interested / Inquisitive",
  "objections_raised": [
    "Late evening timing constraint"
  ],
  "executive_summary": "Customer attempted to book a site visit after operating hours (8:30 PM). The AI agent gracefully explained operating hours and proposed alternate daytime visiting slots.",
  "recommended_next_action": "Follow up via WhatsApp/call to reschedule site visit to a daytime slot convenient for customer."
}
```

---

## Scenario 7: Busy Customer & Scheduled Callback Request

**Expected Behaviour:**
> Politely acknowledge that they are driving, do not push sales, ask for a convenient time to reconnect, and confirm callback.

**Actual Dialogue:**
- **Customer**: Hi, I'm interested in 2 BHK but I am driving right now. Baad mein call karo.
- **AI Sales Agent**: Understood! Please drive safely. Could you let me know a convenient time later today or tomorrow when our team can connect with you regarding Northstar One?

**Extracted CRM Analytics:**
```json
{
  "customer_name": "Not provided",
  "customer_phone": "Not provided",
  "language_detected": "Hinglish",
  "configuration_preference": "2 BHK",
  "budget_range": "₹1.35 Cr+",
  "interest_level": "High",
  "site_visit_status": "Not_Requested",
  "site_visit_details": null,
  "follow_up_requirement": "Scheduled Callback",
  "preferred_callback_time": "Later today / When driving concludes",
  "customer_sentiment": "Busy / Inconvenienced",
  "objections_raised": [],
  "executive_summary": "Customer is interested in 2 BHK residences but was driving during interaction. The AI agent immediately paused sales pitch and offered to schedule a callback.",
  "recommended_next_action": "Place in callback queue for later today to follow up on 2 BHK requirements."
}
```

---

## Scenario 8: DND / Stop Further Communication Request

**Expected Behaviour:**
> Immediately respect the customer's request with zero resistance, confirm DND status, apologize for any inconvenience, and end the conversation politely.

**Actual Dialogue:**
- **Customer**: I have already bought an apartment elsewhere. Please remove my number and do not contact me again.
- **AI Sales Agent**: Congratulations on your new home! We completely respect your preference. We have noted your request and you will not receive any further calls or messages from Northstar Homes. Thank you and have a wonderful day!

**Extracted CRM Analytics:**
```json
{
  "customer_name": "Not provided",
  "customer_phone": "Not provided",
  "language_detected": "English",
  "configuration_preference": "Out of Scope",
  "budget_range": "Not specified",
  "interest_level": "DND_Requested",
  "site_visit_status": "Declined",
  "site_visit_details": null,
  "follow_up_requirement": "None (DND / Uninterested)",
  "preferred_callback_time": null,
  "customer_sentiment": "Frustrated / DND",
  "objections_raised": [
    "Already purchased property elsewhere"
  ],
  "executive_summary": "Customer stated they have purchased an apartment elsewhere and requested immediate DND. The AI agent acknowledged politely with zero pushiness.",
  "recommended_next_action": "Flag customer as DND in CRM and exclude from all outbound communications."
}
```

---

## Scenario 9: Anti-Hallucination & Out-of-Scope Query (4 BHK / Penthouse / Fake Discounts)

**Expected Behaviour:**
> Strictly enforce knowledge boundary: State clearly that Northstar One only offers 2 BHK and 3 BHK configurations, do NOT invent fake discounts or floor plans, and offer to connect with senior management for special queries.

**Actual Dialogue:**
- **Customer**: Do you have a 5 BHK duplex penthouse with private swimming pool, and can you give me a 25% special discount?
- **AI Sales Agent**: Northstar One exclusively offers luxury 2 BHK (starting at ₹1.35 Cr) and 3 BHK (starting at ₹1.75 Cr) residences, and we do not have 5 BHK penthouses. Furthermore, our pricing is standardized without unauthorized discounts. I can connect you with our senior property specialist if you would like to explore our spacious 3 BHK options.

**Extracted CRM Analytics:**
```json
{
  "customer_name": "Not provided",
  "customer_phone": "Not provided",
  "language_detected": "English",
  "configuration_preference": "Out of Scope",
  "budget_range": "Mismatched / Demanded 25% Discount",
  "interest_level": "Low",
  "site_visit_status": "Not_Requested",
  "site_visit_details": null,
  "follow_up_requirement": "None (DND / Uninterested)",
  "preferred_callback_time": null,
  "customer_sentiment": "Price Sensitive / Hesitant",
  "objections_raised": [
    "Requested unavailable 5 BHK penthouse",
    "Demanded unapproved 25% discount"
  ],
  "executive_summary": "Customer requested unavailable 5 BHK penthouses and an unauthorized 25% discount. The AI agent strictly enforced knowledge boundaries without hallucinating unverified inventory or pricing.",
  "recommended_next_action": "Lead is outside standard inventory. Do not follow up unless customer re-engages for 3 BHK residences."
}
```

---

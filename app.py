# app.py
import os
import json
import copy
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Retell SDK
try:
    from retell_sdk import Retell
    retell_client = Retell(api_key=os.getenv("RETELL_API_KEY"))
    RETELL_AVAILABLE = True
except ImportError:
    print("⚠️  retell_sdk not installed → signature verification skipped for local testing.")
    RETELL_AVAILABLE = False
    retell_client = None

# Load mock data
from mock_data import MOCK_DATA
DATA = copy.deepcopy(MOCK_DATA)

def find_patient(full_name: str, dob: str):
    full_name = full_name.strip().lower()
    for p in DATA["patients"]:
        if p["name"].lower() == full_name and p["dob"] == dob:
            return p
    return None

def get_location_details(location_name: str):
    for loc in DATA["locations"]:
        if loc["name"] == location_name:
            return loc
    return {"address": "Victoria, BC", "arrival_note": "Please arrive 30 minutes early."}

# ====================== EXACT TEMPLATES FROM CLIENT BRIEF ======================
def get_followup_templates(patient: dict, msg_type: str):
    location = get_location_details(patient["appointment"]["location"])
    date = patient["appointment"]["date"]
    time = patient["appointment"]["time"]
    loc_name = patient["appointment"]["location"]
    address = location["address"]
    prep_link = patient["prep_link"]

    if msg_type == "booking":
        sms = (f"Pacific Digestive Health: Your procedure is booked for {date} at {time} at {loc_name}. "
               f"Address: {address}. Please arrive 30 minutes early. If IV sedation is planned, "
               f"you are legally impaired for 24 hours afterward and must have a responsible adult "
               f"drive you home. Prep instructions: {prep_link}")
        email_subject = "Pacific Digestive Health Appointment Details"
        email_body = f"""Hello,

This is your appointment information from Pacific Digestive Health.
Hospital: {loc_name}
Address: {address}
Date: {date}
Time: {time}
Please arrive 30 minutes early.
If IV sedation is planned, you are legally impaired for 24 hours afterward and must have a responsible adult drive you home.

Preparation instructions:
{prep_link}

Thank you,
Pacific Digestive Health
Dr. Smith’s Office"""
    elif msg_type == "reschedule":
        sms = (f"Pacific Digestive Health: Your procedure has been rescheduled to {date} at {time} at {loc_name}. "
               f"Address: {address}. Please arrive 30 minutes early. If IV sedation is planned, "
               f"you are legally impaired for 24 hours afterward and must have a responsible adult "
               f"drive you home. Prep instructions: {prep_link}")
        email_subject = "Pacific Digestive Health Appointment Details - Updated"
        email_body = f"""Hello,

Your appointment has been updated:
Hospital: {loc_name}
Address: {address}
Date: {date}
Time: {time}
Please arrive 30 minutes early.
If IV sedation is planned, you are legally impaired for 24 hours afterward and must have a responsible adult drive you home.

Preparation instructions:
{prep_link}

Thank you,
Pacific Digestive Health
Dr. Smith’s Office"""
    else:  # logistics
        sms = (f"Pacific Digestive Health: Your appointment is {date} at {time} at {loc_name}, "
               f"{address}. Please arrive 30 minutes early. Prep: {prep_link}")
        email_subject = "Pacific Digestive Health Appointment Details"
        email_body = f"""Hello,

Your appointment details:
Hospital: {loc_name}
Address: {address}
Date: {date}
Time: {time}
Please arrive 30 minutes early.
Preparation instructions: {prep_link}

Thank you,
Pacific Digestive Health
Dr. Smith’s Office"""

    return {"sms": sms, "email_subject": email_subject, "email_body": email_body}

# ====================== WEBHOOK ======================
@app.post("/webhook")
async def webhook(request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")
    try:
        body = json.loads(body_str)
    except json.JSONDecodeError:
        print("❌ Invalid JSON received")
        return JSONResponse(status_code=400, content={"error": "Invalid JSON"})

    signature = request.headers.get("x-retell-signature")

    # Debug logging
    print(f"\n🔧 --- NEW TOOL CALL ---")
    print(f"Raw body: {body}")

    # Handle both possible payload formats from Retell
    if isinstance(body, dict):
        function_name = body.get("name")
        args = body.get("args", {})
        
        # If "Payload: args only" is ON, sometimes body itself is the args
        if function_name is None and "full_name" in body or "action" in body:
            function_name = "unknown"  # fallback
            args = body
    else:
        function_name = None
        args = {}

    print(f"Tool Name: {function_name}")
    print(f"Args: {args}")

    if not function_name:
        print("❌ No function name found in payload")
        return JSONResponse(status_code=200, content={"result": {"error": "No function name"}})

    result = {}

    if function_name == "verify_patient":
        patient = find_patient(args.get("full_name", ""), args.get("date_of_birth", ""))
        result = {"verified": bool(patient), "patient_found": bool(patient)}

    elif function_name == "get_patient_details":
        patient = find_patient(args.get("full_name", ""), args.get("date_of_birth", ""))
        if patient:
            result = {
                "name": patient["name"],
                "procedure": patient["procedure"],
                "appointment": patient["appointment"],
                "status": patient["status"],
                "prep_link": patient["prep_link"]
            }
        else:
            result = {"error": "Patient not found"}

    elif function_name == "get_open_slots":
        open_slots = [s for s in DATA["schedule"] if s["status"] == "OPEN"]
        result = {"open_slots": [{"date": s["date"], "time": s["time"]} for s in open_slots]}

    elif function_name == "book_or_reschedule_appointment":
        patient = find_patient(args.get("full_name", ""), args.get("date_of_birth", ""))
        if not patient:
            result = {"success": False, "error": "Patient not found"}
        else:
            new_date = args.get("new_date")
            new_time = args.get("new_time")
            action = args.get("action", "book").lower()

            success = False
            for slot in DATA["schedule"]:
                if slot["date"] == new_date and slot["time"] == new_time and slot["status"] == "OPEN":
                    slot["status"] = "BOOKED"
                    slot["patient"] = patient["name"]
                    patient["appointment"] = {
                        "date": new_date,
                        "time": new_time,
                        "location": patient["appointment"].get("location", "Royal Jubilee Hospital")
                    }
                    success = True

                    if action == "reschedule":
                        for old_slot in DATA["schedule"]:
                            if old_slot.get("patient") == patient["name"] and (old_slot["date"] != new_date or old_slot["time"] != new_time):
                                old_slot["status"] = "OPEN"
                                old_slot["patient"] = None
                                break
                    break
            result = {"success": success, "action": action}

    elif function_name == "send_followup":
            patient = find_patient(args.get("full_name", ""), args.get("date_of_birth", ""))
            
            if not patient:
                result = {"success": False, "error": "Patient not found"}
                print("❌ Patient not found for follow-up")
            else:
                msg_type = args.get("message_type", "logistics")
                templates = get_followup_templates(patient, msg_type)

                phone = patient.get("phone") or os.getenv("TEST_PHONE", "+15551234567")
                email = patient.get("email") or os.getenv("TEST_EMAIL", "test@example.com")

                print(f"\n{'='*90}")
                print(f"📱 SMS to {phone} | Type: {msg_type}")
                print(f"📧 EMAIL to {email} | Type: {msg_type}")

                sms_sent = False
                email_sent = False

                # ====================== TWILIO SMS ======================
                twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
                twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
                twilio_from = os.getenv("TWILIO_PHONE_FROM")

                if twilio_sid and twilio_token and twilio_from:
                    try:
                        from twilio.rest import Client
                        client = Client(twilio_sid, twilio_token)
                        message = client.messages.create(
                            body=templates['sms'],
                            from_=twilio_from,
                            to=phone
                        )
                        print(f"✅ SMS Sent! SID: {message.sid} | Status: {message.status}")
                        sms_sent = True
                    except Exception as e:
                        print(f"❌ Twilio Error: {type(e).__name__}: {e}")

                # ====================== SENDGRID EMAIL ======================
                sendgrid_key = os.getenv("SENDGRID_API_KEY")
                from_email = os.getenv("SENDGRID_FROM_EMAIL")

                if sendgrid_key and from_email:
                    try:
                        from sendgrid import SendGridAPIClient
                        from sendgrid.helpers.mail import Mail

                        sg = SendGridAPIClient(sendgrid_key)

                        message = Mail(
                            from_email=from_email,
                            to_emails=email,
                            subject=templates['email_subject'],
                            html_content=templates['email_body'].replace("\n", "<br>")
                        )

                        response = sg.send(message)
                        print(f"✅ Email Sent! Status Code: {response.status_code}")
                        email_sent = True

                    except Exception as e:
                        print(f"❌ SendGrid Error: {type(e).__name__}: {e}")
                else:
                    print("⚠️ SendGrid credentials missing")

                print('='*90)

                result = {
                    "success": True,
                    "message_type": msg_type,
                    "phone": phone,
                    "email": email,
                    "sms_sent": sms_sent,
                    "email_sent": email_sent
                }

            return JSONResponse(status_code=200, content={"result": result})
    else:
        result = {"error": "Unknown function"}

    print(f"✅ Returning: {result}")
    return JSONResponse(status_code=200, content={"result": result})

# ====================== RESET FOR QA ======================
@app.post("/reset")
async def reset_state():
    global DATA
    from mock_data import MOCK_DATA
    DATA = copy.deepcopy(MOCK_DATA)
    return {"status": "reset", "message": "Mock data has been reset"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
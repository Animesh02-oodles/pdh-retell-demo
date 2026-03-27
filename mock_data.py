MOCK_DATA = {
    "patients": [
        {
"name": "Margaret Chen",
"dob": "1959-03-15",
"procedure": "Colonoscopy",
"appointment": {
"date": "Apr 22",
"time": "9:00 AM",
"location": "Royal Jubilee Hospital"
},
"status": "Referral on file",
"prep_link": "https://ampleai.co/prep/colonoscopy",
"phone": "+15551234567",
"email": "test@gmail.com"
},
        {
            "name": "Harry Potter",
            "dob": "2001-09-02",
            "procedure": "Colonoscopy",
            "appointment": {
                "date": "Apr 22",
                "time": "9:00 AM",
                "location": "Royal Jubilee Hospital"
            },
            "status": "Referral on file",
            "prep_link": "https://ampleai.co/prep/colonoscopy",
            "phone": "+919451958058",  
            "email": "animesh.pandey@oodles.io"
        },
        {
            "name": "Robert Takahashi",
            "dob": "1953-07-08",
            "procedure": "Colonoscopy",
            "appointment": {
                "date": "Apr 17",
                "time": "10:00 AM",
                "location": "Victoria General Hospital"
            },
            "status": "Booked - needs reschedule",
            "prep_link": "https://ampleai.co/prep/colonoscopy",
            "phone": "+15551234567",
            "email": "test@example.com"
        },
        {
            "name": "Dorothy Fawcett",
            "dob": "1951-01-03",
            "procedure": "Gastroscopy",
            "appointment": {
                "date": "Apr 29",
                "time": "8:00 AM",
                "location": "Saanich Peninsula Hospital"
            },
            "status": "Booked",
            "prep_link": "https://ampleai.co/prep/gastroscopy",
            "phone": "+15551234567",
            "email": "test@example.com"
        }
    ],
    "schedule": [
        {
            "date": "Apr 17",
            "time": "10:00 AM",
            "status": "BOOKED",
            "patient": "Robert Takahashi"
        },
        {
            "date": "Apr 22",
            "time": "9:00 AM",
            "status": "OPEN",
            "patient": None
        },
        {
            "date": "Apr 24",
            "time": "10:00 AM",
            "status": "OPEN",
            "patient": None
        },
        {
            "date": "Apr 29",
            "time": "8:00 AM",
            "status": "BOOKED",
            "patient": "Dorothy Fawcett"
        }
    ],
    "locations": [
        {
            "name": "Royal Jubilee Hospital",
            "address": "1952 Bay St, Victoria, BC V8R 1J8",
            "arrival_note": "Please arrive 30 minutes early."
        },
        {
            "name": "Victoria General Hospital",
            "address": "1 Hospital Way, Victoria, BC V8Z 6R5",
            "arrival_note": "Please arrive 30 minutes early."
        },
        {
            "name": "Saanich Peninsula Hospital",
            "address": "2166 Mt. Newton Cross Rd, Saanichton, BC V8M 2B2",
            "arrival_note": "Please arrive 30 minutes early."
        }
    ]
}
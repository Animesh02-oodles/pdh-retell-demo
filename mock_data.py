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
"phone": "+61435441731",
"email": "wolfburghwellness@gmail.com"
# "phone": "+919451958058",  
# "email": "animesh.pandey@oodles.io"
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
            # "phone": "+919451958058",  
            # "email": "animesh.pandey@oodles.io"
            "phone": "+61435441731",
            "email": "wolfburghwellness@gmail.com"
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
            "phone": "+61435441731",
            "email": "wolfburghwellness@gmail.com"
            # "phone": "+919451958058",  
            # "email": "animesh.pandey@oodles.io"
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
    # "phone": "+919451958058",  
    # "email": "animesh.pandey@oodles.io",
    "phone": "+61435441731",
    "email": "wolfburghwellness@gmail.com",
    "prep_instructions": "Please don't eat or drink anything for 6 hours before your procedure. You may take essential medications with a small sip of water. Wear comfortable loose clothing. Remove dentures if you have them. Arrange for a responsible adult to drive you home afterward because of the sedation."
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
            "arrival_note": "Please arrive 30 minutes early.",
            "google_maps": "https://www.google.com/maps/dir/?api=1&destination=1952+Bay+St,+Victoria,+BC+V8R+1J8"
        },
        {
            "name": "Victoria General Hospital",
            "address": "1 Hospital Way, Victoria, BC V8Z 6R5",
            "arrival_note": "Please arrive 30 minutes early.",
            "google_maps": "https://www.google.com/maps/dir/?api=1&destination=1+Hospital+Way,+Victoria,+BC+V8Z+6R5"
        },
        {
            "name": "Saanich Peninsula Hospital",
            "address": "2166 Mt. Newton Cross Rd, Saanichton, BC V8M 2B2",
            "arrival_note": "Please arrive 30 minutes early.",
            "google_maps": "https://www.google.com/maps/dir/?api=1&destination=2166+Mt.+Newton+Cross+Rd,+Saanichton,+BC+V8M+2B2"
        }
    ]
}
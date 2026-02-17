import re
import json
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_travel_info(email_text):

    doc = nlp(email_text)

    # Initialize new fields
    data = {
        "names": [],
        "destination": None,
        "email": None,
        "total_persons": None,
        "adults": None,
        "children": None,
        "travel_start_date": None,
        "travel_end_date": None,
        "intent": None
    }

    # ----------------------------
    # Extract Email
    # ----------------------------
    email_match = re.search(r'\S+@\S+', email_text)
    if email_match:
        data["email"] = email_match.group()

    # ----------------------------
    # Extract Guest Names
    # Example: Guest Name - Mr Navneet Jain ,Mrs Avni Jain
    # ----------------------------
    name_match = re.search(r'Guest Name\s*-\s*(.*)', email_text, re.IGNORECASE)

    if name_match:
        names_line = name_match.group(1)

        # Split multiple names
        names = re.split(r',|&', names_line)

        cleaned_names = []
        for name in names:
            name = name.strip()

            # Remove dates if present
            name = re.sub(r'\d{2}/\d{2}/\d{4}', '', name)

            if name:
                cleaned_names.append(name)

        data["names"] = cleaned_names

    # ----------------------------
    # Extract number of persons
    # Example: 03 Adults 1 Child
    # ----------------------------
    person_match = re.search(
        r'(\d+)\s*Adults?\s*(\d+)\s*Child',
        email_text,
        re.IGNORECASE
    )

    if person_match:
        adults = int(person_match.group(1))
        children = int(person_match.group(2))

        data["adults"] = adults
        data["children"] = children
        data["total_persons"] = adults + children

    # ----------------------------
    # Extract travel dates
    # Example: 22 Feb 2026 to 26 Feb 2026
    # ----------------------------
    date_match = re.search(
        r'(\d{1,2}\s\w+\s\d{4})\s*to\s*(\d{1,2}\s\w+\s\d{4})',
        email_text
    )

    if date_match:
        data["travel_start_date"] = date_match.group(1)
        data["travel_end_date"] = date_match.group(2)

    # ----------------------------
    # Extract destination (based on keywords)
    # ----------------------------
    destinations = [
        "Singapore",
        "Dubai",
        "Paris",
        "London",
        "Delhi",
        "Kolkata"
    ]

    for dest in destinations:
        if dest.lower() in email_text.lower():
            data["destination"] = dest
            break

    # ----------------------------
    # Intent detection
    # ----------------------------
    email_lower = email_text.lower()

    if "confirm" in email_lower:
        data["intent"] = "confirmation"

    elif "book" in email_lower:
        data["intent"] = "booking"

    elif "cancel" in email_lower:
        data["intent"] = "cancellation"

    else:
        data["intent"] = "travel_request"

    return data


# ----------------------------
# Your Email Input
# ----------------------------

email_text = """
Please confirm the below booking

Guest Name - Mr Navneet Jain ,Mrs Avni Jain ,Mr Aryan Jain &Mstr Viaan Jain 19/06/2017

Travel Dates - 22 Feb 2026 to 26 Feb 2026

Number of person - 03 Adults 1 Child

Singapore Trip

Waiting for confirmation
"""


# ----------------------------
# Extract
# ----------------------------

result = extract_travel_info(email_text)


# Convert to JSON
json_output = json.dumps(result, indent=4)


# Print
print(json_output)


# Save
with open("travel_output.json", "w") as f:
    json.dump(result, f, indent=4)

print("\nSaved to travel_output.json")

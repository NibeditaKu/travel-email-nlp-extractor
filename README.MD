# Travel Email NLP Information Extraction

This project extracts structured travel information from unstructured travel emails using NLP (spaCy) and Regex.

## Features

- Extract guest names
- Extract destination
- Extract travel dates
- Extract number of adults and children
- Detect travel intent
- Convert output to JSON

## Technologies Used

- Python
- spaCy NLP
- Regex
- JSON

## Project Structure

travel-email-nlp-extractor/
│
├── main.py
├── requirements.txt
├── dataset/
├── output/
└── README.md


## Installation

pip install -r requirements.txt

python -m spacy download en_core_web_sm


## Run Project

python main.py


## Output

Output will be saved in:

output/extracted_travel_data.json


## Example Output

{
 "names": ["Navneet Jain"],
 "destination": "Singapore",
 "total_persons": 4
}


## Author

Nibedita Roy

NLP Travel Email Extraction Project

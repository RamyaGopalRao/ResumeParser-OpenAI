import json

# Define the JSON string with triple backticks
json_str = '''```json
{
    "name": "RAMYA RAO G",
    "email": "ramyagopalrao@yahoo.co.in",
    "phone": "+919686166551",
    "skills": [
        "Python",
        "C#",
        "Shell Script",
        "ASP.NET",
        "Django",
        "FAST API",
        "SQLAlchemy",
        "Apache Airflow (DAGs)",
        "ETL",
        "SQL",
        "PostgreSQL",
        "SQLite",
        "Private Cloud",
        "Pandas",
        "Dask",
        "Numpy",
        "OpenCV",
        "Tkinter",
        "wxPython"
    ],
    "education": [
        {
            "degree": "M.Tech",
            "field": "Digital Electronics and Communication",
            "institution": "NMAMIT Nitte, Udupi, Karnataka",
            "year": "2011"
        },
        {
            "degree": "Bachelor of Engineering",
            "field": "Electronics and Communication",
            "institution": "KVG College of Engineering, Sullia, Dakshina Kannada",
            "year": "2009"
        }
    ],
    "experience": [
        {
            "position": "Lead Software Engineer",
            "company": "Societe Generale Solutions Centre India",
            "location": "Bangalore, India",
            "years": "2021 - 2025"
        },
        {
            "position": "Senior Software Engineer",
            "company": "Mphasis Limited",
            "location": "Bangalore, India",
            "years": "2017 - 2021"
        },
        {
            "position": "Technology Analyst",
            "company": "Infosys, Limited",
            "location": "Bangalore, India",
            "years": "2011 - 2017"
        }
    ]
}
```'''

# Remove the triple backticks and `json` prefix
trimmed_str = json_str.replace('```json\n', '').replace('```', '')

# Try-Catch block for JSON decoding
try:
    resume_dict = json.loads(trimmed_str)
    print("JSON parsed successfully:")
    print(resume_dict)
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
    print("Invalid JSON string:")
    print(trimmed_str)

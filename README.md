# Job Application Tracker (Python + Streamlit)

## Overview
This project is a full-stack job application tracking system built using Python, Streamlit, and SQLite. It allows users to manage job applications, track progress, and analyze outcomes through an interactive dashboard.

The goal of this project is to simulate a real-world productivity tool while demonstrating core software development concepts such as data persistence, CRUD operations, filtering, and analytics visualization.

---

## Features

### Application Management
- Add new job applications
- Edit existing applications
- Delete records
- Persistent storage using SQLite

### Search & Filtering
- Filter by application status
- Search by company or location

### Analytics Dashboard
- Total applications
- Interview count
- Offer count
- Rejection count
- Response rate

### Visual Insights
- Applications by status (bar chart)
- Top locations (bar chart)
- Applications over time (line chart)

---

## Tech Stack
- Python
- Streamlit
- SQLite
- Pandas
- Matplotlib

---

## Key Concepts Demonstrated
- CRUD operations (Create, Read, Update, Delete)
- Database integration (SQLite)
- Data filtering and transformation
- Interactive dashboards
- Real-world problem solving

---

## Project Structure
job-tracker/
├── app.py
├── job_tracker.db
├── requirements.txt
└── README.md

---

## How to Run

1. Install dependencies:
python3 -m pip install -r requirements.txt

2. Run the app:
python3 -m streamlit run app.py

3. Open in browser:
http://localhost:8501

---

## Example Use Case
Track job applications, monitor response rates, and analyze hiring trends.

---

## Limitations
- Local database only
- No authentication system
- Single-user design

---

## Future Improvements
- Cloud database integration
- Authentication system
- CSV export
- Follow-up reminders
- Duplicate detection

---

## Resume Description
Built a full-stack job application tracking system using Python, Streamlit, and SQLite with CRUD functionality, filtering, and analytics dashboards.


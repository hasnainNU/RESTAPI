# Research Opportunity Portal

A simple web app where faculty can post research opportunities, and anyone can view, edit, close, or delete them.

## Features

- Add a new research opportunity
- View full details of an opportunity
- Edit an existing opportunity
- Close an opportunity when applications are done
- Delete an opportunity
- Form validation on both the frontend and backend

## Built With

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite (via Flask-SQLAlchemy)

## Project Structure

```
├── main.py          # Flask backend (API)
├── index.html       # Frontend (HTML + CSS + JS in one file)
└── README.md
```

## How to Run

1. **Install the requirements**

   ```bash
   pip install flask flask-sqlalchemy flask-cors
   ```

2. **Start the backend**

   ```bash
   python main.py
   ```

   The API will run at `http://127.0.0.1:5000`.

3. **Open the app**

   Open `index.html` in your browser.

The database file (`research_opportunities.db`) is created automatically the first time you run the backend.

## API Endpoints

| Method | Endpoint                      | Description              |
|--------|-------------------------------|--------------------------|
| GET    | `/api/opportunities`          | Get all opportunities    |
| GET    | `/api/opportunities/<id>`     | Get one opportunity      |
| POST   | `/api/opportunities`          | Create an opportunity    |
| PUT    | `/api/opportunities/<id>`     | Update an opportunity    |
| DELETE | `/api/opportunities/<id>`     | Delete an opportunity    |

## Opportunity Fields

| Field                  | Type    | Notes                        |
|------------------------|---------|------------------------------|
| `research_title`       | text    | Required                     |
| `research_description`| text    | Required                     |
| `research_area`        | text    | Required                     |
| `faculty_name`         | text    | Required                     |
| `department`           | text    | Required                     |
| `required_skills`      | text    | Required                     |
| `available_positions`  | number  | Required, at least 1         |
| `application_deadline` | date    | Required, format `YYYY-MM-DD`|
| `status`               | text    | `Open` or `Closed`           |

## Author

Your Name
# Student / Task Management Portal

A simple, beginner-friendly full-stack web application designed for learning how a **Frontend (HTML/CSS/JS)**, **Backend REST API (Python Flask)**, and **Database (SQLite)** interact with each other.

---

## 1. Features

- **Dashboard Statistics**: Dynamic metrics for Total Records, Pending Tasks, Completed Tasks, and Unique Categories.
- **Create & Add Records**: Form validation on both frontend and backend.
- **Read & List Records**: Displays all student tasks in a clean, scrollable table with styled badges (`Pending` & `Completed`).
- **Update Records**: In-place edit functionality to update student details, tasks, category, or status.
- **Mark Complete Action**: One-click action to transition task status from `Pending` to `Completed`.
- **Delete Records**: Confirmation modal before removing records permanently.
- **Instant Search & Filter**: Real-time frontend search (Name, Roll Number, Task, Category, Status) and Status Filter (`All`, `Pending`, `Completed`).
- **Connection Error Handling**: Visually alerts the user if the backend Flask server is offline.

---

## 2. Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript (Fetch API)
- **Backend**: Python 3, Flask, Flask-CORS
- **Database**: SQLite3 (using Python's built-in `sqlite3` module)

---

## 3. Project Structure

```text
student-task-portal/
│
├── backend/
│   ├── app.py           # Flask REST API server & routes
│   ├── database.py      # SQLite database setup and SQL queries
│   ├── requirements.txt # Python package dependencies
│   └── database.db      # SQLite database file (created automatically)
│
├── frontend/
│   ├── index.html       # Dashboard HTML structure
│   ├── style.css        # Dashboard visual styles and responsive layout
│   └── script.js        # Vanilla JS logic & API fetch requests
│
└── README.md            # Beginner-friendly project guide
```

---

## 4. Full-Stack Data Architecture Flow

```text
                USER (Browser)
                      |
                      v
        HTML + CSS + JavaScript (Frontend)
                      |
                      | Fetch API (HTTP JSON Requests)
                      v
             Flask REST API (Backend)
                      |
                      | Parameterized SQL Queries
                      v
              SQLite (database.db)
                      |
                      v
             Flask REST API (Backend)
                      |
                      | JSON Response
                      v
        JavaScript updates UI dynamically
```

---

## 5. How to Run the Project Locally

### Step 1: Start the Backend (Flask Server)

1. Open your terminal or command prompt.
2. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask application:
   ```bash
   python app.py
   ```
5. The backend will start on: **`http://127.0.0.1:5000`**

---

### Step 2: Start the Frontend (Web Server)

1. Open a **second terminal** window.
2. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
3. Start a local HTTP server using Python:
   ```bash
   python -m http.server 5500
   ```
4. Open your web browser and visit: **`http://127.0.0.1:5500`**

---

## 6. REST API Endpoints

The Flask backend exposes the following RESTful API endpoints:

| Method | Endpoint | Description | Request Body Example |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/records` | Fetch all records | None |
| `GET` | `/api/records/<id>` | Fetch a single record by ID | None |
| `POST` | `/api/records` | Create a new record | `{"name":"Rahul","roll_number":"BCA101","task":"Python Assignment","category":"Assignment","status":"Pending"}` |
| `PUT` | `/api/records/<id>` | Update an existing record | `{"name":"Rahul","roll_number":"BCA101","task":"Python Assignment","category":"Assignment","status":"Completed"}` |
| `DELETE` | `/api/records/<id>` | Delete a record by ID | None |

---

## 7. How SQLite is Used

The project uses Python's built-in `sqlite3` library in `database.py`:

- **Automatic Initialization**: When `app.py` starts, `database.init_db()` runs automatically and creates the table `records` if it does not already exist.
- **Schema**:
  ```sql
  CREATE TABLE IF NOT EXISTS records (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      roll_number TEXT NOT NULL,
      task TEXT NOT NULL,
      category TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'Pending',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
- **Security**: All SQL operations use parameterized queries (`?` placeholders) to prevent SQL injection vulnerabilities.

---

## 8. How Frontend Communicates with Backend

- The frontend JavaScript (`script.js`) uses JavaScript's native **`fetch()` API** to communicate with Flask endpoints.
- **CORS (`Flask-CORS`)** is enabled on Flask so that requests sent from `http://127.0.0.1:5500` to `http://127.0.0.1:5000` are allowed by the browser.
- **No Page Reloads**: All CRUD actions (Create, Read, Update, Delete) perform background network requests and update the DOM directly without reloading the web page.

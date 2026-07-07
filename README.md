# 🏥 Patient Management System API

A RESTful Patient Management System API built using **FastAPI** and **Pydantic**. This project allows users to manage patient records with CRUD operations, search, sorting, statistics, and automatic BMI calculation.

---

## 🚀 Features

- ➕ Create a Patient
- 📋 View All Patients
- 👤 View Patient by ID
- ✏️ Update Patient Details
- ❌ Delete Patient
- 🔍 Search Patients by Name or City
- 📊 View Patient Statistics
- 📈 Sort Patients by Height, Weight, or BMI
- ⚖️ Automatic BMI Calculation
- ✅ Data Validation using Pydantic

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI**
- **Pydantic**
- **JSON** (for data storage)

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home |
| GET | `/about` | About API |
| GET | `/patients` | View All Patients |
| GET | `/patients/{patient_id}` | View Patient by ID |
| POST | `/patients` | Create Patient |
| PUT | `/patients/{patient_id}` | Update Patient |
| DELETE | `/patients/{patient_id}` | Delete Patient |
| GET | `/patients/search` | Search by Name or City |
| GET | `/patients/sort` | Sort Patients |
| GET | `/patients/stats` | Patient Statistics |

---

## ▶️ Getting Started

### Clone the Repository

```bash
git clone https://github.com/LokitaGoyal/patient-management-system-api.git
```

### Navigate to the Project

```bash
cd patient-management-system-api
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn main:app --reload
```

Open your browser and visit:

```
http://127.0.0.1:8000/docs
```

to access the interactive Swagger UI.

---

## 📚 What I Learned

- Building REST APIs with FastAPI
- CRUD Operations
- Request Validation using Pydantic
- Path & Query Parameters
- JSON File Handling
- Exception Handling
- Search, Sorting & Statistics APIs
- Automatic BMI Calculation using Computed Fields

---

## 🔮 Future Improvements

- SQLite / MySQL Database Integration
- SQLAlchemy ORM
- JWT Authentication
- User Login & Authorization
- Appointment Management
- Medical Report Upload
- Pagination & Advanced Filtering

---

## 👩‍💻 Author

**Lokita Goyal**

BCA Student | Python Developer | FastAPI Learner

⭐ If you like this project, consider giving it a star!

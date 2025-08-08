
# 📝 Note Management API

A **modern, secure, and powerful FastAPI-based note management system** that supports full-featured **user authentication**, **note creation**, **categorization**, and **bookmarking**, all secured with **JWT tokens** (access + refresh) and structured for scalability using **SQLAlchemy ORM** and **Alembic** for database migrations.

---

## 🚀 Features

### ✅ Authentication & Authorization
- **Secure Signup & Login** with hashed passwords using `bcrypt`
- **JWT-based Access and Refresh Tokens**
- **Token expiration** management (30 min access, 10 days refresh)
- **Protected routes** with OAuth2 dependency injection

### 🧑 User Management
- Signup and login endpoints
- Edit user profile (username/email)
- Change password securely
- View your profile
- Delete your account

### 🗂️ Categories
- Create custom note categories
- Fetch all user-specific categories
- Get all notes in a category
- Edit category names
- Delete categories (with cascading support)

### 🗒️ Notes
- Create, edit, view, and delete notes
- Assign notes to categories or leave them uncategorized
- Toggle **bookmarks** on notes
- Get **all bookmarked notes**
- Move a note to a different category or unassign it

### 📦 Additional
- Modular router structure: `auth`, `user`, `notes`, `category`
- Password hashing and verification via `passlib`
- Cleanly structured with **Pydantic schemas** for validation
- Database operations powered by **SQLAlchemy**
- Configured with `.env` using `pydantic-settings`
- **Database versioning and migration** using **Alembic**

---

## 🏗️ Tech Stack

| Layer        | Tool            |
|--------------|------------------|
| Backend      | FastAPI          |
| ORM          | SQLAlchemy       |
| Migration    | Alembic          |
| Database     | PostgreSQL       |
| Auth         | OAuth2 + JWT     |
| Validation   | Pydantic         |
| Passwords    | Passlib (bcrypt) |
| Environment  | pydantic-settings|

---

## 📁 Folder Structure

```
.
├── main.py
├── database.py
├── models.py
├── schemas.py
├── utils.py
├── oauth2.py
├── config.py
├── alembic/
│   └── versions/
├── ROUTER/
│   ├── auth.py
│   ├── note.py
│   ├── user.py
│   └── category.py
├── .env
└── README.md
```

---

## 🔐 Authentication Flow

1. **User signs up** → creates hashed password → stored securely.
2. **User logs in** → receives access + refresh token.
3. **Access token** used for most routes (expires in 30 minutes).
4. **Refresh token** used to get a new access token (expires in 10 days).
5. **Custom token validation** ensures token integrity and type.

---

## 🔄 Alembic (Database Migration)

**Initialize Alembic:**
```bash
alembic init alembic
```

**Configure `alembic.ini` and `env.py`** to use the `SQLALCHEMY_DATABASE_URL` from `config.py`.

**Generate migration:**
```bash
alembic revision --autogenerate -m "Initial migration"
```

**Apply migration:**
```bash
alembic upgrade head
```

---

## 🛠️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd note-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** based on:
   ```env
   database_username=your_user
   database_password=your_pass
   database_hostname=localhost
   database_port=5432
   database_name=note_db
   algorithm=HS256
   secret=your_secret_key
   access_time=30
   refresh_time=10
   ```

5. **Run Alembic migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the app**
   ```bash
   uvicorn main:app --reload
   ```

---

## 📬 API Endpoints

### 🔑 Auth
| Method | Endpoint            | Description              |
|--------|---------------------|--------------------------|
| POST   | `/user/signup`      | Create a new user        |
| POST   | `/user/login`       | Authenticate user        |
| POST   | `/user/refresh`     | Refresh access token     |

### 👤 User
| Method | Endpoint             | Description                |
|--------|----------------------|----------------------------|
| GET    | `/user/view/me`      | View current user          |
| PUT    | `/user/edit/me`      | Edit user info             |
| PUT    | `/user/change-password` | Change password        |
| DELETE | `/user/delete/me`    | Delete account             |

### 📁 Category
| Method | Endpoint                | Description                  |
|--------|-------------------------|------------------------------|
| POST   | `/category/create`      | Create a new category        |
| GET    | `/category/all`         | View all categories          |
| GET    | `/category/{id}`        | Get notes in a category      |
| PUT    | `/category/edit/{id}`   | Edit a category              |
| DELETE | `/category/delete/{id}` | Delete a category            |

### 📝 Notes
| Method | Endpoint                              | Description                      |
|--------|---------------------------------------|----------------------------------|
| POST   | `/notes/create`                       | Create a note                    |
| GET    | `/notes/all`                          | Get all notes                    |
| GET    | `/notes/uncategorized`                | Get uncategorized notes          |
| GET    | `/notes/{id}`                         | Get note by ID                   |
| PUT    | `/notes/edit/{id}`                    | Edit a note                      |
| DELETE | `/notes/delete/{id}`                  | Delete a note                    |
| PUT    | `/notes/bookmark/{id}`                | Toggle note bookmark             |
| GET    | `/notes/bookmarks`                    | Get all bookmarked notes         |
| PUT    | `/notes/category/{note_id}/{cat_id}`  | Assign/unassign note to category |

---

## 💡 Future Enhancements
- 📱 Frontend integration (React or Vue)
- 🔔 Notifications and reminders
- 📊 Note usage analytics
- 🧠 AI-assisted note suggestions
- 🗃️ Note sharing and collaboration

---

## 👨‍💻 Author

**Faruq Bashir**  
FastAPI Enthusiast • Clean Coder • Backend Wizard

---

## 📄 License

MIT License — feel free to use, fork, and contribute!

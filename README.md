## Project Overview

This project is a User Management Web Application deployed on an AWS EC2 instance, using Python Flask for the backend and AWS RDS (MySQL) for persistent user data storage. The system enables users to register via an HTML form and provides an admin dashboard to search and manage users.

---

## Features

- User Registration with server-side validation
- Secure password storage using hashing (Werkzeug)
- User Login and session management
- Protected Dashboard accessible only to logged-in users
- Admin search functionality for users by username, email, or name
- Logout functionality
- MySQL database integration via AWS RDS

---

## Tech Stack

- **Backend:** Python 3, Flask, Werkzeug (for password hashing)
- **Database:** AWS RDS MySQL
- **Frontend:** HTML5, CSS3 (with simple styling)
- **Hosting:** AWS EC2 (Ubuntu)
- **Testing:** Postman for API endpoint testing

---

## Setup Instructions

### 1. AWS Setup
- Launch an EC2 instance (Ubuntu recommended)
- Set up security groups allowing HTTP (80), SSH (22), and MySQL (3306) from EC2 to RDS
- Create an RDS MySQL instance with public accessibility enabled

### 2. Clone the Repository
```bash
git clone <your-github-repo-url>
cd <repo-folder>
```

### 3. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure Environment Variables or Update `app.py`
Update your MySQL RDS credentials in `app.py` under `db_config`:
```python
db_config = {
    'host': '<your-rds-endpoint>',
    'user': '<your-db-username>',
    'password': '<your-db-password>',
    'database': '<your-db-name>'
}
```

### 5. Run the Flask App
```bash
python app.py
```

---

## Usage

- Access the app on your EC2 public IP at port 5000
- Navigate to `/register` to create a new user
- Login at `/login`
- Access the dashboard at `/dashboard` (requires login)
- Logout using the button on the dashboard

---

## Testing with Postman

You can test the API endpoints using Postman by sending appropriate requests to:

- `POST /register` — Register a new user
- `POST /login` — Login existing user
- `GET /dashboard` — Access dashboard (requires session)
- `GET /logout` — Logout

---

## Troubleshooting

- **Database connection errors:**  
  Ensure your EC2 security group can connect to RDS on port 3306. Check your credentials and RDS endpoint.

- **Flask app errors:**  
  Verify all dependencies are installed. Run `python app.py` from your project root.

- **Session issues:**  
  Make sure `app.secret_key` in `app.py` is set to a secure, random string.

---

## Future Enhancements

- Add user role management (admin vs regular users)
- Implement user profile editing
- Add password reset via email
- Enhance frontend UI with Bootstrap or React

---

## License

This project is licensed under the MIT License.

---

## Author

Jeet Patel

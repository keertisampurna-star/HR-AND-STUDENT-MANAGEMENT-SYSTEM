# HR-AND-STUDENT-MANAGEMENT-SYSTEM
A role-based Django web application that allows admin and HR users to manage student admissions and employee accounts efficiently with secure authentication, CRUD operations, and email notifications.



## Features

### 👥 User Roles
- **Admin / Superuser**
  - Add, view, update, delete all employees and students
  - Create new HR accounts
  - Full system access

- **HR / Normal User**
  - Add, view, update, delete only their own students

### 📚 Student Management
- Add new students with course & fee details
- Auto-calculates pending fee
- Sends confirmation email upon admission
- Update & delete student information

### 🧑‍💼 Employee Management
- Add new employees (Admin or HR)
- Role-based access
- Update employee accounts

### 🔐 Security Features
- Login required for restricted pages using `@login_required`
- Password hashing using Django authentication system
- Cache prevention using `@never_cache`

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Framework | Django |
| Frontend | HTML, CSS, Bootstrap |
| Database | SQLite |
| Email Service | SMTP (Django send_mail) |
| Tools Used | PyCharm, Git, GitHub |







# Library Management System (LMS) with Django and REST API

This project is a fully-featured Library Management System built with Django and Django REST Framework (DRF). It enables users to manage books, authors, borrowers, and borrowing transactions efficiently. Additional features include user authentication, background task handling with Celery, and containerization using Docker.

---

## Features

### 1. Manage Books
- Add, edit, view, and delete books.
- Include details like **title**, **description**, **author**, **ISBN**, **category**, and **publication date**.
- Search and filter books by **title**, **author**, or **category**.
- Use **pagination** to manage large book lists.

### 2. Manage Authors
- Add, view, update, and delete authors.
- Include details like **name**, **biography**, **nationality**, and **date of birth**.
- Link each author to the books they've written.

### 3. Borrower Profiles
- Create borrower profiles with **username**, **email**, and **registration date**.
- View borrowing history and due dates for each borrower.

### 4. Borrowing Books
- Borrow and return books with rules like:
  - Maximum books allowed to borrow.
  - Borrowing duration.
- Automatically flag **overdue books**.

### 5. Book Reservations
- Reserve books that are checked out and notify users when available.

### 6. Book Reviews and Ratings
- Allow users to leave reviews and ratings for books.
- Display the **average rating** for each book.

### 7. User Authentication
- Secure login using **JWT authentication**.
- Two user roles:
  - **Admin**: Manage books, authors, and borrowers.
  - **Borrower**: Borrow/return books and leave reviews.

### 8. Notifications for Borrowers
- Remind borrowers of **upcoming due dates** and **overdue books** using **Celery**.

### 9. Background Tasks with Celery
- Handle tasks asynchronously using **Redis** as a message broker.

### 10. Containerization with Docker
- Deploy the app, database, and Redis in containers using **Docker Compose**.

### 11. Reporting System
- Generate admin reports for:
  - Most borrowed books.
  - Borrowers with overdue books.
  - Books currently checked out.

### 12. API Documentation
- Auto-generate API documentation using **Swagger**.

### 13. Search and Filter
- Search by **book title**, **author**, or **category**.
- Filter by **genre**, **language**, or **availability**.

### 14. Borrowing Rules and Validation
- Ensure users can't borrow more than allowed or borrow reserved books.
- Validate transactions to maintain system integrity.

---

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/lms-django-api.git
   cd lms-django-api
   ```

2. **Build and run Docker containers**:
   ```bash
   docker-compose up --build
   ```

3. **Apply migrations**:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create a superuser**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the app**:
   - API: [http://localhost:8000](http://localhost:8000)
   - Admin panel: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (via djangorestframework-simplejwt)
- **Task Queue**: Celery, Redis
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **API Documentation**: Swagger / drf-spectacular
- **Testing**: pytest

---

## Testing

Run tests using:
```bash
docker-compose exec web pytest
```

To run specific test files or folders:
```bash
docker-compose exec web pytest path/to/tests.py
```

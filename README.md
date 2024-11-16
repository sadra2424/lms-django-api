# Library Management System (LMS) with Django and REST API

This is a Library Management System built with Django and Django REST Framework (DRF). It provides features for managing books, authors, borrowers, and borrowing transactions, along with additional functionality such as user authentication, background task handling with Celery, and containerization with Docker.

## Features

1. **Manage Books**
   - Add, edit, view, and delete books with details like title, description, author, ISBN, category, and publication date.
   - Search and filter books by title, author, or category.
   - Use pagination for large book lists.

2. **Manage Authors**
   - Add, view, update, and delete authors.
   - Link authors to the books they've written.

3. **Borrower Profiles**
   - Create borrower profiles with username, email, and registration date.
   - Track borrowing history and due dates.

4. **Borrowing Books**
   - Borrow and return books with validation rules.
   - Track overdue books.

5. **Book Reservations**
   - Reserve books that are checked out and notify users when they become available.

6. **Book Reviews and Ratings**
   - Leave reviews and ratings for books with average rating calculation.

7. **User Authentication**
   - Secure login using JWT authentication.
   - Different roles: Admin and Borrower.

8. **Notifications**
   - Reminders for due dates and overdue books using Celery.

9. **Background Tasks with Celery**
   - Handle notifications and long-running tasks asynchronously with Redis as the message broker.

10. **Containerization with Docker**
    - Deploy the app, PostgreSQL database, and Redis in containers using Docker Compose.

11. **Reporting System**
    - Generate reports asynchronously for:
      - Most borrowed books.
      - Borrowers with overdue books.
      - Checked-out books.

12. **API Documentation**
    - Automatically generate API documentation using Swagger.

## Technologies Used
- Django
- Django REST Framework
- Celery
- Redis
- PostgreSQL
- Docker & Docker Compose

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/lms-django-api.git
   cd lms-django-api

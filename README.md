# SabiBiz - Business Management API

A Django-based backend API designed for small business management. It allows users to track sales, manage expenses, and view real-time business analytics through a dashboard.

## 🚀 Features

* **User Authentication:** Secure Login and Registration system.
* **Dashboard Analytics:** Real-time calculation of Total Sales, Total Expenses, and Net Profit.
* **Best Sellers:** Automatically identifies the best-selling product.
* **Recent Activity:** Merged timeline of recent sales and expenses.
* **Transaction Management:** simple API endpoints to record new sales and expenses.

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Database:** SQLite (Default) / PostgreSQL (Production ready)
* **Authentication:** Django Session Auth (Cookies)
* **Data Serialization:** JSON

## ⚙️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/sabibiz.git](https://github.com/yourusername/sabibiz.git)
    cd sabibiz
    ```

2.  **Create a Virtual Environment**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install django
    ```

4.  **Apply Database Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Run the Server**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

## 📡 API Endpoints

| Method | Endpoint        | Description                          |
| :----- | :-------------- | :----------------------------------- |
| POST   | `/register/`    | Create a new user account            |
| POST   | `/login/`       | Authenticate user (Starts Session)   |
| GET    | `/dashboard/`   | Get analytics, profits, and activity |
| POST   | `/add-sale/`    | Record a new sale                    |
| POST   | `/add-expense/` | Record a new expense                 |
| GET    | `/logout/`      | End the session                      |

## 📝 Notes
* This API uses **Session-based Authentication**. 
* Clients (Postman, Browsers, Mobile Apps) must handle **Cookies** to access the Dashboard and Add-Data endpoints.
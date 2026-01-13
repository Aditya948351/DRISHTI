# How to Run Drishti Platform

Follow these steps to set up and run the Drishti Platform locally.

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtualenv (recommended)

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository-url>
    cd DrishtiPlatform
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` is missing, you may need to install Django manually: `pip install django`)*

4.  **Apply database migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser** (optional, for admin access):
    ```bash
    python manage.py createsuperuser
    ```

## Running the Server

1.  **Start the development server**:
    ```bash
    python manage.py runserver
    ```

2.  **Access the application**:
    Open your web browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Project Structure
- `DrishtiPlatform/`: Main project configuration (`settings.py`, `urls.py`).
- `accounts/`: User authentication and management.
- `complaints/`: Core complaint management logic.
- `dashboard/`: Dashboard views for different roles.
- `templates/`: HTML templates (including `PublicPages/`).
- `static/`: CSS, JavaScript, and images.

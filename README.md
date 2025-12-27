# Responsi - Web App

A dynamic web application built with Python (Flask) and Supabase for the backend, and a responsive user interface crafted with HTML, CSS, and vanilla JavaScript. This project serves as a comprehensive example of a modern web application with user authentication, content management, and a dashboard system.

## ✨ Features

*   **User Authentication:** Secure sign-up and sign-in functionality using Supabase for user management.
*   **Article Management:** Users can create, read, and manage articles.
*   **Dashboard:** A personalized dashboard for users to view their articles and a separate admin dashboard for site management.
*   **Responsive Design:** The UI is designed to work seamlessly across different devices.
*   **Interactive Elements:** Engaging JavaScript-powered features, including a canvas animation on the homepage.

## 🚀 Technologies Used

### Backend
*   **Python:** The core programming language for the server-side logic.
*   **Flask:** A lightweight WSGI web application framework in Python.
*   **Supabase:** An open-source Firebase alternative for handling the database, authentication, and storage.
    *   `supabase-py`: The official Python client for Supabase.
*   **Flask-WTF & WTForms:** For handling web forms.
*   **Flask-CKEditor:** For a rich text editor experience when creating articles.

### Frontend
*   **HTML5:** The standard markup language for creating web pages.
*   **CSS3:** For styling the application, with separate stylesheets for different components and pages.
*   **JavaScript (ES6+):** For client-side interactivity and dynamic features.
*   **Bootstrap 5** For styling

### Deployment
*   **Vercel:** The project is configured for easy deployment on the Vercel platform.

## ⚙️ Getting Started

### Prerequisites

*   Python 3.x
*   `pip` (Python package installer)
*   A Supabase account and project.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Rndraha21/responsi-prakweb.git
    cd responsi-prakweb
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file in the root directory and add your Supabase project URL and API key:
    ```
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key
    ```

### Running the Application

1.  **Start the Flask development server:**
    ```bash
    flask run or python app.py
    ```

2.  Open your browser and navigate to `http://127.0.0.1:5000`.

## 🖼️ Screenshots

![Preview application](https://ik.imagekit.io/9shkqioju/preview%20applicatin.png?updatedAt=1766825038483)
## 🤝 Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug fixes, please open an issue or submit a pull request.

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

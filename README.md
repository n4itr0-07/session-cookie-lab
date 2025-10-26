# Session & Cookie Lab 🍪

A simple, interactive Flask application designed to demonstrate the fundamental concepts of **HTTP Cookies** and **Server-Side Sessions** in a practical lab environment.

---

## 🎯 Purpose of This Lab

The primary goal of the **Session & Cookie Lab** is to provide a clear, visual understanding of how web applications track user state (i.e., remember who you are) in a stateless protocol like HTTP.

It allows developers and students to:
* Observe the **session token** being issued and stored in the browser.
* See the corresponding **session data** stored on the server.
* Simulate **session reuse** by manually transferring the cookie token.
* Watch a session's **Time-to-Live (TTL)** dynamically count down until expiration.

---

## 🛠️ How Sessions and Cookies Work Here

This application uses a classic server-side session management model:

| Concept | Mechanism in This App |
| :--- | :--- |
| **Cookie** | The server creates a unique, unguessable string called the **`session_token`** and sends it to the browser. The browser stores this in a cookie and sends it back with every subsequent request. |
| **Session** | When a user logs in, the application stores user data (`username`, `created_at`, `expires_at`) in the server's in-memory dictionary (`SESSIONS`) using the `session_token` as the **key**. |
| **Authentication** | When a request arrives, the server reads the `session_token` from the incoming cookie and looks up the corresponding user data in the `SESSIONS` dictionary. If found and not expired, the user is considered logged in. |
| **Expiration** | Sessions are configured with a **Time-to-Live (TTL)** of `300` seconds (`5` minutes). The dynamic counter shows how much time is remaining before the server automatically deletes the session data. |

---

## 🚀 Getting Started (Run Locally)

This project is built using **Python** and the **Flask** micro-framework.

### Prerequisites

You need **Python 3.x** installed on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/n4itr0-07/session-cookie-lab.git
cd session-cookie-lab
```

### 2\. Set up the Environment

It's recommended to use a virtual environment:

```bash
# Create a virtual environment
python3 -m venv venv 

# Activate the environment (Linux/macOS)
source venv/bin/activate

# Activate the environment (Windows)
.\venv\Scripts\activate

# Install dependencies (only Flask is required)
pip install Flask
```

### 3\. Run the Application

Execute the Python file to start the development server:

```bash
python session_cookie_demo.py
```

The application will now be running on your local machine at:
🌐 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

### 4\. Default Login

Use the following credentials to log in:

  * **Username:** `putin`
  * **Password:** `infected`

-----

## 📸 Demo and Screenshots

*(You will add your screen recordings and images here.)*

### Login Screen

<img width="940" height="595" alt="image" src="https://github.com/user-attachments/assets/c803e00b-5ae0-4dc6-b287-0dd3c1adbfb1" />


### Active Session Dashboard

<img width="1920" height="1102" alt="home_ss" src="https://github.com/user-attachments/assets/463650cf-bcf9-4c71-9ee2-ced1b9326029" />


### Video Demo

https://github.com/user-attachments/assets/46187281-1b13-44e2-86b4-cc6a7f9b42ba


---

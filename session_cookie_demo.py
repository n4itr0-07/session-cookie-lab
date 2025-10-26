from flask import Flask, request, make_response, redirect, render_template_string
import secrets, time

app = Flask(__name__)

# -----------------------------
# Config
# -----------------------------
DEFAULT_USER = "putin"
DEFAULT_PASS = "infected"
TOKEN_TTL = 300  # seconds

# In-memory session store: token -> {user, created_at, expires_at}
SESSIONS = {}

# -----------------------------
# HTML Template (single file)
# -----------------------------
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Session & Cookie Lab</title>
<style>
/* General Styles */
body { 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    background: #12121f; /* Deeper, cooler background */
    color: #e0e0f0; /* Soft white text */
    text-align: center; 
    padding: 30px;
    margin: 0;
}
h1 { color: #4CAF50; /* A pleasant green for the main title */ }
h2 { color: #81D4FA; /* Light blue for section titles */ }
.container { 
    background: #1e1e2e; /* Slightly lighter inner container */
    padding: 30px; 
    border-radius: 12px; 
    max-width: 650px; 
    margin: auto; 
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4); /* Subtle shadow for depth */
}

/* Form/Input Styles */
input { 
    padding: 12px; 
    margin: 8px 0; 
    border-radius: 6px; 
    border: 1px solid #333; 
    width: calc(80% - 24px); /* Account for padding */
    background: #252535; /* Darker input background */
    color: #e0e0f0;
    transition: border-color 0.3s;
}
input:focus {
    border-color: #4CAF50;
    outline: none;
}
button { 
    padding: 12px 25px; 
    margin: 15px 5px; 
    border: none; 
    border-radius: 6px; 
    background: #4CAF50; /* Green button */
    color: #111; 
    cursor: pointer;
    font-weight: bold;
    transition: background 0.3s, transform 0.1s;
}
button:hover { 
    background: #66BB6A; /* Lighter green on hover */
    transform: translateY(-1px);
}

/* Table Styles */
table { 
    margin: 20px auto; 
    border-collapse: collapse; 
    width: 90%; 
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}
th, td { 
    padding: 12px; 
    border: 1px solid #3a3a4a; 
    text-align: center; 
}
th { 
    background: #333344; 
    color: #B3E5FC; /* Light blue headers */
    font-weight: normal;
}

/* Logged-in Specific Styles */
p strong {
    color: #FFEB3B; /* Yellow for key info like token */
}

/* Definitions and Notes */
h3 { color: #FFD54F; /* Amber for the definitions header */ }
.definition-box {
    text-align: left;
    margin: 20px auto;
    padding: 15px;
    background: #252535;
    border-radius: 8px;
}
.definition-box p {
    margin: 10px 0;
    line-height: 1.6;
}
.definition-box strong {
    color: #B3E5FC; /* Blue for definition terms */
    font-weight: bold;
    display: inline-block;
    min-width: 80px; /* Align definitions */
}
.note { 
    font-size: 0.9em; 
    color: #999; 
    margin-top: 20px;
}
</style>
</head>
<body>
<div class="container">
<h1>Session & Cookie Lab</h1>

{% if not logged_in %}
<h2>User Login</h2>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Username" required><br>
<input type="password" name="password" placeholder="Password" required><br>
<button type="submit">Secure Login</button>
</form>
<p class="note">Default demo user: <b>putin</b> / <b>infected</b></p>

{% else %}
<h2>Welcome, {{ user }} 👋</h2>
<p>Your session is active!</p>
<p><strong>Session Token (cookie):</strong> {{ token }}</p>
<p><strong>Expires in:</strong> <span id="session-countdown">{{ expires_in }}</span> seconds</p>
<form method="POST" action="/logout">
<button type="submit">Logout</button>
</form>

<hr style="border-top: 1px solid #3a3a4a; margin: 30px 0;">

<h3>Active Sessions</h3>
<table>
<tr>
<th>#</th><th>User</th><th>Token (truncated)</th><th>Expires In (s)</th>
</tr>
{% for idx, (tk, info) in enumerate(sessions.items(), start=1) %}
<tr>
<td>{{ idx }}</td>
<td>{{ info.user }}</td>
<td>{{ tk[:10] }}...</td>
<td>{{ info.expires_in }}</td>
</tr>
{% endfor %}
</table>

<hr style="border-top: 1px solid #3a3a4a; margin: 30px 0;">

<h3>Definitions (for non-tech users)</h3>
<div class="definition-box">
<p><strong>Cookie:</strong> A small piece of data stored in your <b>browser</b> (client-side) that the server uses to remember you between requests.</p>
<p><strong>Session:</strong> The <b>server-side memory</b> of who you are and your state, which is linked to your unique cookie token.</p>
</div>
<p class="note">Tip: Open a second browser or private window and paste your token as a cookie to simulate session reuse.</p>

<script>
    // JavaScript for dynamic countdown
    var countdownElement = document.getElementById('session-countdown');
    if (countdownElement) {
        var countdownValue = parseInt(countdownElement.textContent.trim());

        function updateCountdown() {
            if (countdownValue > 0) {
                countdownValue -= 1;
                countdownElement.textContent = countdownValue;
            } else {
                // Optionally refresh the page or show a message when expired
                clearInterval(interval);
                countdownElement.textContent = 'Expired! Refreshing...';
                setTimeout(function() {
                    window.location.reload();
                }, 1000); // Reload after 1 second
            }
        }

        // Update the countdown every 1000 milliseconds (1 second)
        var interval = setInterval(updateCountdown, 1000);
    }
</script>

{% endif %}
</div>
</body>
</html>
"""

# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET"])
def index():
    token = request.cookies.get("session_token")
    # Clean up expired sessions (optional, but good practice)
    global SESSIONS
    SESSIONS = {k: v for k, v in SESSIONS.items() if v["expires_at"] > time.time()}

    session = SESSIONS.get(token)
    logged_in = False
    user = ""
    expires_in = 0
    if session and session["expires_at"] > time.time():
        logged_in = True
        user = session["user"]
        expires_in = int(session["expires_at"] - time.time())
        
    # Prepare session data for display, calculating remaining time
    display_sessions = {}
    for k, v in SESSIONS.items():
        remaining = int(v["expires_at"] - time.time())
        if remaining > 0:
            display_sessions[k] = {"user": v["user"], "expires_in": remaining}

    return render_template_string(TEMPLATE,
                                    logged_in=logged_in,
                                    user=user,
                                    token=token,
                                    expires_in=expires_in,
                                    sessions=display_sessions,
                                    enumerate=enumerate)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username != DEFAULT_USER or password != DEFAULT_PASS:
        return "Invalid credentials! Use putin / infected", 401

    # Generate a new secure token
    token = secrets.token_urlsafe(16)
    now = time.time()
    
    # Store session data server-side
    SESSIONS[token] = {
        "user": username,
        "created_at": now,
        "expires_at": now + TOKEN_TTL
    }
    
    # Send the token to the client as a cookie
    resp = make_response(redirect("/"))
    # httponly=False is set for this demo to allow client-side inspection, 
    # but for security, it should generally be True.
    resp.set_cookie("session_token", token, max_age=TOKEN_TTL, httponly=False) 
    return resp

@app.route("/logout", methods=["POST"])
def logout():
    token = request.cookies.get("session_token")
    if token and token in SESSIONS:
        # Delete session from server memory
        del SESSIONS[token]
        
    # Remove cookie from client
    resp = make_response(redirect("/"))
    resp.delete_cookie("session_token")
    return resp

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    # Note: debug=True is for development only
    app.run(debug=True, host="127.0.0.1", port=5000)
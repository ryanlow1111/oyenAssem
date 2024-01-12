import sqlite3
from fastapi import FastAPI, Form, HTTPException, Depends, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# Mount the static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

KEY = "your-secret-key"

def create_connection():
    connection = sqlite3.connect("users.db")
    return connection

def create_user_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

def create_test_user():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "12345"))
    connection.commit()
    connection.close()

# Call this function to create the user table
# create_user_table()

# Call this function to create a test user
# create_test_user()

def authenticate_user(username: str, password: str):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    connection.close()
    return user

def create_user_token(username: str):
    # Generate a simple opaque token
    return f"token_for_{username}"

@app.get("/")
def read_root(request: Request, token: str = Cookie(default=None)):
    if token:
        try:
            return templates.TemplateResponse("mainpage.html", {"request": request})
        except HTTPException:
            pass
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if user:
        token = create_user_token(username)
        response = RedirectResponse(url="/main", status_code=303)
        response.set_cookie(key="token", value=token)
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/main", response_class=HTMLResponse)
def main_page(request: Request):
    print("Rendering main page...")
    return templates.TemplateResponse("mainpage.html", {"request": request})

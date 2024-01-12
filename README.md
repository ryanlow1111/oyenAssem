# Oyen Assesment

## Step 1
pip install -r requirements.txt

## Step 2
For Windows
Find folder named "Scripts" to "activate" virtual environment.(activate.bat in CMD, Activate.ps1 in Powershell)

For Mac
Find folder named "bin" to "activate" virtual environment

## Step 3
Run the server with uvicorn:

`uvicorn main:app --reload`

## Step 4
After the server successfuly run, can open http://127.0.0.1:8000 to direct to login page

![image](https://github.com/ryanlow1111/oyenAssem/assets/87624469/8702989a-0bea-4346-9a7f-3eb826efa7d1)

User require to insert username and password to login. (Now only come with default account with username: admin and password: 12345)

Once successful logged in, it will direct to Main page

Cookies is used in this assesment to save the authentication that can automatically redirect user from login page to main page everytime when they visit the page

@echo off
cd "C:\Users\Truong\Desktop\myproject"
call "C:\Users\Truong\Desktop\myproject\venv\Scripts\activate.bat"
waitress-serve --listen=0.0.0.0:8000 app:app
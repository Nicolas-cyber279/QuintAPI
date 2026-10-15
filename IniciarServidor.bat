@echo off
cd /d D:\Desenvolvimento\QUINT\QuintAPI
python -m uvicorn main:api --host 127.0.0.1 --port 8000 --reload
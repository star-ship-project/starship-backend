@echo off
echo ===================================================
echo     STAR S.H.I.P. Local Server Initialization
echo ===================================================
echo.
echo Starting the FastAPI Backend (Port 8000)...

:: 1. Navigate to the backend folder and start FastAPI
cd backend
start cmd /k "python -m uvicorn API_Main:app --reload"

:: 2. Wait for 2 seconds
timeout /t 2 /nobreak > NUL

echo Starting the Frontend Server (Port 3000)...

:: 3. Navigate back out, then into the frontend folder
cd ..\frontend

:: 4. Start Python's built-in HTTP server on port 3000
start cmd /k "python -m http.server 3000"

:: 5. Wait for 1 second
timeout /t 1 /nobreak > NUL

echo Opening Dashboard in your browser...

:: 6. Open the browser using the actual local network port!
start http://localhost:3000/login_page.html

echo.
echo Both servers are running! You can minimize the terminal windows.
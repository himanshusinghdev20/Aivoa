@echo off
echo ============================================================
echo HCP CRM - Installation Verification Script
echo ============================================================
echo.

REM Check Node.js
echo [1/6] Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Node.js is NOT installed
    echo     Download from: https://nodejs.org/
    goto :error
) else (
    echo [OK] Node.js is installed
    node --version
)
echo.

REM Check Python
echo [2/6] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python is NOT installed
    echo     Download from: https://www.python.org/
    goto :error
) else (
    echo [OK] Python is installed
    python --version
)
echo.

REM Check npm packages
echo [3/6] Checking npm packages...
if not exist "node_modules" (
    echo [!] node_modules not found
    echo     Run: npm install
    goto :error
) else (
    echo [OK] node_modules exists
)
echo.

REM Check backend venv
echo [4/6] Checking Python virtual environment...
if not exist "backend\venv" (
    echo [!] Virtual environment not found
    echo     Run: cd backend ^&^& python -m venv venv
    goto :error
) else (
    echo [OK] Virtual environment exists
)
echo.

REM Check backend .env
echo [5/6] Checking backend .env file...
if not exist "backend\.env" (
    echo [!] backend\.env not found
    echo     Copy backend\.env.example to backend\.env
    echo     Then edit with your database and API key
    goto :error
) else (
    echo [OK] backend\.env exists
)
echo.

REM Check frontend .env
echo [6/6] Checking frontend .env file...
if not exist ".env" (
    echo [!] .env not found
    echo     Creating .env with default values...
    echo VITE_API_URL=http://localhost:8000 > .env
    echo [OK] .env created
) else (
    echo [OK] .env exists
)
echo.

echo ============================================================
echo All checks passed! ^_^
echo ============================================================
echo.
echo Next steps:
echo.
echo 1. Configure backend\.env with your:
echo    - Database URL
echo    - Groq API key (get from https://console.groq.com/)
echo.
echo 2. Create database:
echo    PostgreSQL: CREATE DATABASE hcp_crm;
echo    MySQL:      CREATE DATABASE hcp_crm;
echo.
echo 3. Start backend:
echo    cd backend
echo    venv\Scripts\activate
echo    python start.py
echo.
echo 4. Start frontend (new terminal):
echo    npm run dev
echo.
echo 5. Open: http://localhost:5173
echo.
goto :end

:error
echo.
echo ============================================================
echo Installation incomplete. Please fix the issues above.
echo ============================================================
echo.
echo See SETUP.md for detailed instructions.
echo.
exit /b 1

:end
pause

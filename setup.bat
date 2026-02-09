@echo off
echo ========================================
echo Personal First-Person Chatbot Setup
echo ========================================
echo.

echo [1/3] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [2/3] Creating vector store from documents...
python ingest.py
if errorlevel 1 (
    echo ERROR: Failed to create vector store
    pause
    exit /b 1
)
echo.

echo [3/3] Setup complete!
echo.
echo ========================================
echo To start the chatbot, run:
echo     streamlit run app.py
echo ========================================
echo.
pause

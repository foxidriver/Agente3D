@echo off
cd C:\Users\lfoss\OneDrive\stampa3d-agent

:: Chiude eventuali sessioni Streamlit già aperte
taskkill /f /im streamlit.exe >nul 2>&1

:: Piccola pausa per essere sicuri che si sia chiuso
timeout /t 2 >nul

call venv\Scripts\activate
streamlit run agente.py
pause
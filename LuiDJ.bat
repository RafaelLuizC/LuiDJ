@echo off
REM Rodar app.py em paralelo (nova janela do terminal)
start "" python "C:\github-vitoria\LuiDJ\app.py"

REM Esperar 2 segundos para garantir que o servidor suba
timeout /t 5 >nul

REM Abrir navegador com as duas abas
start "" "http://127.0.0.1:5000/"
start "" "https://music.youtube.com/"

exit

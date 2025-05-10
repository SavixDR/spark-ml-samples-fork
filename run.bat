@echo off
setlocal enabledelayedexpansion

REM Start Spring Boot application
start "" java -jar api\build\libs\api-1.0-SNAPSHOT.jar

REM Wait until the server is ready
:wait_loop
curl -s -o nul -I http://localhost:9090/index.html | findstr /C:"200 OK" >nul
if %errorlevel% neq 0 (
    timeout /t 1 >nul
    goto wait_loop
)

REM Open default browser to the web page
start "" http://localhost:9090/index.html


@echo off
cd C:\path\to\your\repo
call git add .
set /p commitMessage="Enter commit message: "
call git commit -m "%commitMessage%"
call git push origin master
pause

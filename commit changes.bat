@echo off
cd C:\path\to\your\repo
call git add .
call git commit -m "Automatic commit"
call git push origin master
pause

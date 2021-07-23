title LOG_UPLOAD
@echo off
cd..
git add .
git commit -m "FILE_UPLOAD"
git push -u origin master
echo START NOW
timeout -t 3
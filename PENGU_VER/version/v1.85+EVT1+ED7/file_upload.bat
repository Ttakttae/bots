title LOG_UPLOAD
@echo off
cd..
git add .
git commit -m "FILE_UPLOAD"
git push -u origin master
timeout -t 3
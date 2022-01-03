@echo off
git pull origin main

python page__get.py

git add out/origin_front/*.html
git add out/translated/*.html
git commit -m "[auto commit]daily korea information updated."

rem "pushだけはすると事故る"
rem "git push origin main"

#!/bin/zsh

python3 -m venv venv
source venv/bin/activate
pip3 install Flask beautifulsoup4 requests lxml cchardet chardet

tsc static/ts/script.ts --outDir static/js/


@echo off
echo Installing required packages...
pip install customtkinter
pip install pytablericons
pip install pyinstaller

echo Downloading UPX...
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/upx/upx/releases/download/v4.2.2/upx-4.2.2-win64.zip' -OutFile 'upx.zip'}"
powershell -Command "& {Expand-Archive -Path 'upx.zip' -DestinationPath '.' -Force}"
del upx.zip

echo Building Blackjack executable...
python setup.py
echo Done!
pause 
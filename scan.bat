@echo off
MODE con: COLS=45 lines=25
setlocal enabledelayedexpansion
color 3f
setlocal
del Result.txt
del url.txt
del u1.txt
del u2.txt
del u3.txt
cls
color A
set /p port=输入要扫描的端口:
mkdir %port%
copy s.exe .\%port%\s.exe
copy ip.txt .\%port%\ip.txt
copy spider.py .\%port%\spider.py
cd %port%
for /f "eol= tokens=1,2 delims= " %%i in (ip.txt) do s.exe syn %%i %%j %port%  /save
for /f "eol=- tokens=1 delims= " %%i in (result.txt) do echo %%i>>u1.txt
for /f "eol=P tokens=1 delims= " %%i in (u1.txt) do echo %%i>>u2.txt
for /f "eol=S tokens=1 delims= " %%i in (u2.txt) do echo %%i>>u3.txt
for /f "eol=- tokens=1 delims= " %%i in (u3.txt) do echo http://%%i:%port%/console>>url.txt
python spider.py url.txt
echo All Done!
pause
exit

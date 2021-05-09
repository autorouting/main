@echo off

REM -- set variables --------------------------------------
REM If Python windows environment variable was not set:
REM set exepath="your python installation path\python.exe"

REM If Python windows environment variable was already set:
set exepath="python.exe"
set appname="gui.py"

REM -- run application --------------------------------------
echo Launching Routing GUI ...
%exepath% %appname%

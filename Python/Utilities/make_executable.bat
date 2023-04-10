@echo off

setlocal enabledelayedexpansion

set argCount=0
for %%x in (%*) do set /A argCount+=1

if %argCount% EQU 0 exit /b %ERRORLEVEL%

set cd1=%CD%

pushd %~dp0
copy make_executable.py "%cd1%"
pushd "%cd1%"
python make_executable.py %*
del make_executable.py

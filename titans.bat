::[Bat To Exe Converter]
::
::fBE1pAF6MU+EWH3eyGU5PDNBTji2NX+7CKYg3OHv7uSU7wBQeOc+aoHS1LPDNO9ex0DpeoQkzH8Xmd9BOB5Lal+fZwIx5GNDv2q5NteM/R/4Kg==
::fBE1pAF6MU+EWH3eyGU5PDNBTji2NX+7CKYg3OHv7uSU7wBQeOc+aoHS1LPDNO9ex0DpeoQkzH8Xmd9BOB5Lal+fZwIx5GNDv2q5PsqdtAqvWkaOhg==
::fBE1pAF6MU+EWH3eyGU5PDNBTji2NX+7CKYg3OHv7uSU7wBQeOc+aoHS1LPDNO9ex0DpeoQkzH8Xmd9BOB5Lal+fZwIx5GNDv2q5G+6/liHSbyg=
::fBE1pAF6MU+EWH3eyGU5PDNBTji2NX+7CKYg3OHv7uSU7wBQeOc+aoHS1LPDNO9ex0DpeoQkzH8Xmd9BOB5Lal+fZwIx5GNDv2q5OsaVvUHxUyg=
::fBE1pAF6MU+EWH3eyGU5PDNBTji2NX+7CKYg3OHv7uSU7wBQeOc+aoHS1LPDNO9ex0DpeoQkzH8Xmd9BOB5Lal+fZwIx5GNDv2q5OsaVvUHxU0+c7ys=
::fBE1pAF6MU+EWH3eyGU5PDNBTji2NX+7CKYg3OHv7uSU7wBQeOc+aoHS1LPDNO9ex0DpeoQkzH8Xmd9BOB5Lal+fZwIx5GNDv2q5BeK9lyLEBEWNhg==
::fBE1pAF6MU+EWH3eyGU5PDNBTji2NX+7CKYg3OHv7uSU7wBQeOc+aoHS1LPDNO9ex0DpeoQkzH8Xmd9BOB5Lal+fZwIx5GNDv2q5JcKNpgbzT0WM6F8jVXFskwM=
::fBE1pAF6MU+EWH3eyGU5PDNBTji2NX+7CKYg3OHv7uSU7wBQeOc+aoHS1LPDNO9ex0DpeoQkzH8Xmd9BOB5Lal+fZwIx5GNDv2q5A86IsgHyCniI9k4iVXVwgQM=
::fBE1pAF6MU+EWH3eyGU5PDNBTji2NX+7CKYg3OHv7uSU7wBQeOc+aoHS1LPDNO9ex0DpeoQkzH8Xmd9BOB5Lal+fZwIx5GNDv2q5I86IsgHyBEqI8is=
::YAwzoRdxOk+EWAnk
::fBw5plQjdG8=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCuDJH6N4GolKidgRRCDMniGMrwI6ebooqfKjkgcRuw2doiWzrvDDeUe5Vftb5Ng124XrM4fGFZsdx+uIwI1oGB+om2RNsnSthfkKg==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal

set "APP_DIR=%~dp0"
if "%APP_DIR:~-1%"=="\" set "APP_DIR=%APP_DIR:~0,-1%"
set "APP_MAIN=main.py"
set "PY_CMD="

if not exist "%APP_DIR%\%APP_MAIN%" (
  echo Titans launcher error: %APP_DIR%\%APP_MAIN% not found.
  pause
  exit /b 1
)

pushd "%APP_DIR%" >nul 2>nul
if errorlevel 1 (
  echo Titans launcher error: could not change directory to %APP_DIR%.
  pause
  exit /b 1
)

where python >nul 2>nul
if %errorlevel%==0 (
  set "PY_CMD=python"
)

if not defined PY_CMD (
  where py >nul 2>nul
  if %errorlevel%==0 (
    set "PY_CMD=py -3"
  )
)

if not defined PY_CMD (
  echo Python launcher not found. Install Python and ensure python.exe or py.exe is on PATH.
  popd
  pause
  exit /b 1
)

echo Launching Titans Desktop from %APP_DIR%...
%PY_CMD% "%APP_MAIN%"
set "EXITCODE=%ERRORLEVEL%"

popd

if not "%EXITCODE%"=="0" (
  echo.
  echo Titans closed with exit code %EXITCODE%.
  echo Check the error details above.
  pause
)

exit /b %EXITCODE%

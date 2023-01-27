@echo off

echo:
echo #============================================#
echo #                                            #
echo #   Welcome to the RIK app backend server!   #
echo #                                            #
echo #============================================#
echo:
echo:

cd ..\backend

if not exist .venv (
    echo Creating a new Python venv...
    python -m venv .venv

    echo Activating the new venv...
    call .\.venv\Scripts\activate.bat

    echo:
    echo:
    echo Installing requirements...
    echo --------------------------------------------
    pip install -r requirements.txt
    cd ..
    pip install -e backend
    cd backend
) else (
    echo Skipping venv setup as it already exists...
    echo Activating the existing venv...
    call .\.venv\Scripts\activate.bat
)

echo:
echo:
echo Running the RIK app backend server...
echo --------------------------------------------
python rik_app\main.py


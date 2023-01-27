@echo off

echo:
echo #=============================================#
echo #                                             #
echo #   Welcome to the RIK app frontend server!   #
echo #                                             #
echo #=============================================#
echo:
echo:

cd ..\frontend

if not exist node_modules (
    echo Installing dependencies...
    echo -----------------------------------------------
    npm install

    echo:
    echo:
    echo Running the RIK app frontend server...
    echo -----------------------------------------------
    npm start

) else (
    echo Skipping dependencies installation as node_modules already exists...

    echo:
    echo:
    echo Running the RIK app frontend server...
    echo -----------------------------------------------
    npm start
)




echo Checking venv version
virtualenv --version
if errorlevel 1 goto errorNoVenv
../../venv/Scripts/activate.bat
django --version
if errorlevel 1 goto errorNoDjango

goto:eof

:errorNoVenv
echo virtualenv not installed try installing...
pip install virtualenv
cd ../..
virtualenv --no-site-package venv

:errorNoDjango
pip install django
pip install django-users2


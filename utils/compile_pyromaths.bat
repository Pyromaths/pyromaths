REM Crée l'installateur Windows
C:
REM A effectuer la 1re fois, après avoir installé Python-2.7.15
REM cd "C:\Users\%username%\"
REM pip install virtualenv
REM virtualenv "C:\Users\%username%\BUILD-pyromaths"
REM C:\Users\%username%\Build-pyromaths\Scripts\python -m pip install lxml C:\Users\%username%\Downloads\PyQt4-4.11.4-cp27-cp27m-win32.whl jinja2==2.8 pypiwin32
REM C:\Users\%username%\Build-pyromaths\Scripts\python -m pip install py2exe_py2
REM C:\Users\%username%\Build-pyromaths\Scripts\python -m pip install innosetup

cd "C:\Users\%username%\BUILD-pyromaths"
copy e:\dist\*.zip . /y /B
"c:\Program Files\7-Zip\7z.exe" x pyromaths-*.zip
del pyromaths-*.zip
cd pyromaths-*

C:\Users\%username%\Build-pyromaths\Scripts\python -m pip install --upgrade lxml PyQt4 pypiwin32 py2exe_py2 innosetup
C:\Users\%username%\BUILD-pyromaths\Scripts\python setup.py innosetup"

copy dist\pyromaths-*-win32.exe e:\dist /Y

cd "C:\Users\%username%\BUILD-pyromaths"
rmdir /Q /S pyromaths-*
cd ..
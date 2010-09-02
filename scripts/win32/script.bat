REM Crée l'installateur de Pyromaths pour Windows
cd "C:\Documents and Settings\jerome\Bureau"
md pyromaths
xcopy z:\pyromaths\*.* "C:\Documents and settings\jerome\Bureau\pyromaths" /s
copy z:\setup-win32.py "C:\Documents and Settings\jerome\Bureau\"
copy z:\setup-win32.iss "C:\Documents and Settings\jerome\Bureau\"
c:\Python26\python.exe setup-win32.py py2exe -i sip -p lxml,gzip
"C:\Program Files\Inno Setup 5\ISCC.exe" setup-win32.iss
copy Pyromaths-setup.exe z:
rmdir /s /q dist
rmdir /s /q build
rmdir /s /q pyromaths
del Pyromaths-setup.exe
del setup-win32.iss
del setup-win32.py

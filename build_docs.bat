@REM Make docs from doc strings
sphinx-apidoc -o docs .

@REM Convert rst to html
.\docs\make.bat html

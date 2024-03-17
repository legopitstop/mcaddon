@REM fix for appengine ImportError: pip install urllib3==1.26.15 requests-toolbelt==0.10.1

@REM Build source distribution
@REM build

@REM Upload to PyPI using twime
python -m twine upload dist/* --config-file %userprofile%\Desktop\Python\.pypirc

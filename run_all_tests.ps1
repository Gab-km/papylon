$oldPYTHONPATH = $env:PYTHONPATH
$env:PYTHONPATH = $env:PYTHONPATH + ";."
py.test ./tests
$env:PYTHONPATH = $oldPYTHONPATH
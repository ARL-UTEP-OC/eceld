Converts ECELD export output into a easily readable summary bug report.

## Run 
```
$python __init__.py /path/to/export/file/ecel-export_1556984639
```

The code takes in 1 argument, which is the path to the export file.  The directory should have the /raw/ and /parsed/ directories.

If any paths need to be manual modified, they can be modified in the parse_eceld.py file

## Output

HTML files will be outputted to the same folder __init__.py is located

Run index.html to look at the human readable output page.


## Tools
Code was written in Python 3.6

Bootstrap/HTML was used
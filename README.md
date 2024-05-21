To list the top-level directories and files:
```bash
python pyls.py
```

To include hidden files:
```bash
python pyls.py -A
```
To use the long listing format:
```bash
python pyls.py -l
```
To reverse the order of the listing:
```bash
python pyls.py -l -r
```
To sort by time modified:
```bash
python pyls.py -l -r -t
```
To filter by files or directories:
```bash
python pyls.py -l -r -t --filter=file
```
To navigate to a subdirectory:
```bash
python pyls.py parser
```
To show human-readable sizes:
```bash
python pyls.py -l -H
```
To display help:
```bash
python pyls.py --help
```

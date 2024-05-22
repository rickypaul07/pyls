
## Clone project

```bash
git clone https://github.com/rickypaul07/pyls.git
```

# To run project

## pyls

A Python implementation of the `ls` command.

## Installation

To install the package, run:

```bash
pip install .
```

## To execute

To list the top-level directories and files:
```bash
pyls
```

To include hidden files:
```bash
pyls -A
```
To use the long listing format:
```bash
pyls -l
```
To reverse the order of the listing:
```bash
pyls -l -r
```
To sort by time modified:
```bash
pyls -l -r -t
```
To filter by files or directories:
```bash
pyls -l -r -t --filter=file

pyls -l -r -t --filter=dir
```
To navigate to a subdirectory:
```bash
pyls parser
```
To show human-readable sizes:
```bash
pyls -l -H
```
To display help:
```bash
pyls --help
```

## For testing

```bash
pytest
```

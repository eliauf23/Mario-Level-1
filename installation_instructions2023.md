Installation:

I'm using python 3.8:

## Create venv in SuperMarioLevel1 directory
```shell
cd SuperMarioLevel1
python3 -m venv venv
```
## Activate venv
```shell
source venv/bin/activate
```
## Install requirements
```shell
pip install -r requirements.txt
```

### setup module for running tests
In setup.py, we create a package out of SuperMarioLevel1 module so we can import it from anywhere without using relative path notation

```bash
cd SuperMarioLevel1
pip install -e .
```

### run game (first cd into Mario-Level-1 directory)
```bash
 python3 mario_level_1.py
```


### run tests
```bash
cd SuperMarioLevel1
python3 -m pytest
```


--------
For future reference: .png files should be fixed already (if need to fix again, instructions are below)

### need to install libpng with homebrew to get pngfix()

```bash

brew install libpng
```
### then run this script to fix all pngs, move to temp file, make sure they're working and then you can overwrite existing ones
```bash
mkdir tmp; for f in ./*.png; do pngfix --strip=color --out=tmp/"$f" "$f"; done 
```


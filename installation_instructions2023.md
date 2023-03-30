Installation:
- .png files should be fixed (if need to fix again)

### need to install libpng with homebrew to get pngfix()

```bash

brew install libpng
```
### then run this script to fix all pngs, move to temp file, make sure they're working and then you can overwrite existing ones
```bash
mkdir tmp; for f in ./*.png; do pngfix --strip=color --out=tmp/"$f" "$f"; done 
```


I'm using python 3.8:

### install pygame
```bash
python3 -m pip install -U pygame --user
```


### run game (first cd into Mario-Level-1 directory)
```bash

 python3 mario_level_1.py
```

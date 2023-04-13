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

## notes:
In setup.py, we create a package out of SuperMarioLevel1 module so we can import it from anywhere without using relative path notation

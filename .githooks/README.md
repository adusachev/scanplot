
## ipynb formatter

### Install pre-commit hook

```sh
source venv/bin/activate
pip install pre-commit==4.0.1
```

```sh
pre-commit install
```


### Usage

**Way 1**

Manually run formatter before staging/commiting `.ipynb` file:
```sh
pre-commit run ipynb-cleaner
```
after that notebook metadata and outputs will be removed

Stage and commit:
```sh
git add file.ipynb
git commit -m "some message"
```


**Way 2**

Stage `.ipynb` file:
```sh
git add file.ipynb
```

try to commit:
```sh
git commit -m "some message"
```

Pre-commit script will automatically remove notebook metadata and outputs.

Stage file again and commit it:
```sh
git add file.ipynb
git commit -m "some message"
```



---


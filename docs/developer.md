# Docs for developers


## Install dev dependicies with poetry

```sh
git clone https://github.com/adusachev/scanplot.git <REPO> && cd <REPO>
```

```sh
poetry env use python3.11
```

```sh
poetry shell
```

```sh
poetry install --with dev
```


---



## Pre-commit hook



```sh
source venv/bin/activate
# or
poetry shell
```

```sh
pre-commit install
```


**Usage**

Way 1

Manually run formatter before staging/commiting `.ipynb` file:
```sh
pre-commit run ipynb-cleaner
```
after that notebook metadata and outputs will be removed.

Stage and commit:
```sh
git add file.ipynb
git commit -m "some message"
```


Way 2

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

**Skip pre-commit hooks**


```sh
git commit -m "some message" --no-verify
```


---

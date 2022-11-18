### Crear entorno virtual

```bash
virtualenv env
```

### Install requeriments

```bash
pip install -r requirements.txt
```


### Activar la máquina virtual

```bash
source venv/bin/activate
```

- windows

```bash
venv\Scripts\activate

venv/Scripts/activate.ps1
```

### Varaible de entorno .env



```bash

SECRET_KEY="myclavesecreta"
FLASK_APP=app.py
FLASK_DEBUG=1
FLASK_ENV=FLASK_DEVELOPMENT
SQLALCHEMY_DATABASE_URI=mysql://root@localhost/login_aula1
SQLALCHEMY_TRACK_MODIFICATIONS=False 

```


### Run

```bash
flask run
```


# Crear base de datos y agregarlo al archivo .env


## Migraciones en la base de datos



```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

# SQLALCHEMY_DATABASE_URI

Algunas formas de `SQLALCHEMY_DATABASE_URI`:

```
SQLALCHEMY_DATABASE_URI = "mysql://root:password@localhost/database"
SQLALCHEMY_DATABASE_URI = "mysql://root:password@127.0.0.1:33060/database"
```

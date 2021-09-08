# Server

## Setting the database connection

### After creating the database connection, make sure to adapt the URL on the database.py file to it.

## Project server setup
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install mysql
alembic upgrade head
```

## Project server run
```
uvicorn main:app --reload
```

### Dependencies
```
python v3.11
pip v22.2.1    (No need to install separately will be include when you create venv)
docker v24.0.6
docker-compose v2.210
```

### Start Database service
1. go to current directory(where docker-compose.yml file is located)
2. run docker container for DB `docker-compose up --build reverse-bit-db`

### Local python setup (optional)
1. `cd <project root>`
2. `python -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`

### setup environment file
Create `.env` file 
add all required environment variables

### Apply DB migration
1. run command: `alembic upgrade head` 

### Start the Backend Server
`hypercorn app.main:app --bind 0.0.0.0:8001`

### Check the API Documentation
1. Open the Browser
2. visit `http://127.0.0.1:8001/docs`
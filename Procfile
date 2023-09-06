web: python app/infra/db_setup.py && gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.runner.api:app 

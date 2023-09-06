web: python app/infra/db_setup.py && gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.runner.api:app --host=0.0.0.0 --port=${PORT:-5000}

.PHONY: run-api run-web

# Run the FastAPI server
run-api:
	uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Run the Flask web interface
run-web:
	python webapp.py

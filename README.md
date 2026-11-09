# Back-End-Development-Songs

IBM Back-End Development Capstone: Flask REST API backed by MongoDB.

## Setup
Created from the IBM template. Run `bash bin/setup.sh`, then activate the virtual environment named `venv` using `source ~/venv/bin/activate`.
The supplied setup script creates this environment with `python3.9 -m venv ~/venv`.
The Python environment and dependency installation steps completed successfully in IBM Skills Network Cloud IDE; the verified runtime was Python 3.9.25.
Set `MONGODB_SERVICE`, `MONGODB_USERNAME`, and `MONGODB_PASSWORD` in the environment.
Run `python -m flask run --host=0.0.0.0 --port=5000`.

## Endpoints
`GET /health`, `GET /count`, `GET /song`, `GET /song/<id>`,
`POST /song`, `PUT /song/<id>`, and `DELETE /song/<id>`.
Successful POST and PUT requests return HTTP 201 CREATED, as required by the course; successful DELETE requests return HTTP 204 NO CONTENT.

Seed records are inserted only when missing. Existing collection data is never dropped on application startup.

## Verification
Validated against the MongoDB instance provisioned by IBM Skills Network.
Health, list, creation, update, and deletion were exercised with curl.
PyMongo is pinned for compatibility with the lab MongoDB version.

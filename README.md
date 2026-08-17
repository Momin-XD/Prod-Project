# MK Cloud Service

A production-style Flask web service with a full CI/CD deployment pipeline — built to demonstrate containerization, automated testing, and self-hosted CI/CD on AWS infrastructure.

**Live status page:** shows environment, uptime, and health at a glance.

## What this project demonstrates

- **Application**: A lightweight Flask app with a status dashboard UI and JSON API endpoints (`/api/status`, `/api/metrics`)
- **Containerization**: Multi-stage-conscious Dockerfile — slim base image, non-root user, Gunicorn as the production WSGI server
- **Orchestration**: `docker-compose` setup with health checks, log rotation, and restart policies
- **CI/CD**: A Jenkins declarative pipeline that checks out code, runs the test suite, builds and pushes a Docker image to Docker Hub, deploys the container to a remote node, and runs a post-deploy health check
- **Infrastructure**: Deployed across a two-node AWS EC2 setup (Jenkins master + build/deploy slave)
- **Testing**: Automated unit tests with `pytest`, run as a required pipeline stage before any deployment
- **Health checking**: A standalone retry-based health-check script used both by Docker's own healthcheck and by the Jenkins pipeline's post-deploy verification step

## Tech stack

| Layer | Tool |
|---|---|
| Application | Python, Flask |
| WSGI server | Gunicorn |
| Testing | Pytest |
| Containerization | Docker, Docker Compose |
| CI/CD | Jenkins (declarative pipeline) |
| Registry | Docker Hub |
| Infrastructure | AWS EC2 (master/slave nodes) |

## Project structure

```
Prod-Project/
├── app.py                  # Flask application (UI + API endpoints)
├── test_app.py              # Unit tests
├── requirements.txt         # Python dependencies
├── Dockerfile                # Production container image
├── docker-compose.yml        # Local/single-host orchestration
├── Jenkinsfile                # CI/CD pipeline definition
└── scripts/
    └── health_check.py       # Retry-based deployment health check
```

## How it works

1. A developer pushes code to the repository.
2. Jenkins picks up the change and runs the pipeline:
   - Checks out the code
   - Creates a virtual environment and runs `pytest`
   - Builds the Docker image and pushes it to Docker Hub, tagged with the build number
   - Deploys the new container to the slave node, replacing the old one
   - Runs `scripts/health_check.py` against the live endpoint, retrying until the service reports healthy, and fails the pipeline if it doesn't come up
3. The app is served on port 80 (mapped to Gunicorn on port 5000 inside the container) with automatic restarts and rotated JSON logs.

## Running locally

```bash
docker compose up --build
```

The app will be available at `http://localhost`.

## Running tests

```bash
pip install -r requirements.txt
pytest test_app.py -v
```

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Status dashboard (HTML) |
| `GET /api/status` | Service health as JSON |
| `GET /api/metrics` | Basic runtime metrics as JSON |

## Author

Momin Khisal

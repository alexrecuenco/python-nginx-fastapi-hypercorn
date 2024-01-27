# Example

- NGINX for uploading files faster
- A backend with fastapi that doesn't touch the files to use all the validation magic of fastapi
- Debugging magic to allow easy development using VScode tasks and docker compose

# Requirements

## To run

Docker, and docker compose.

Tested with

```txt
❯ docker --version
Docker version 24.0.6, build ed223bc
❯ docker compose version
Docker Compose version v2.22.0-desktop.2
```

## To develop

Python3.10 or above (Tested with python3.11 only), VScode, recommended vscode extensions added to this project

Run to initiali

```bash
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r backend/requirements.test.txt
```

# How to use

1. Run `docker compose up --build`
2. After running (See How to Run), go to `localhost:8080`. **IMPORTANT 8080, not 8000**
3. Upload your CSV, it will POST to `uploads/` and return a task-id
4. Check your task-id in `uploads/{task-id}`
5. If your task is done, it will automatically redirect you to a download
6. If there was an error, it will give you the error code, you could "report" this to the server manager, and he will find in the logs how it happened searching for your task ID, if they have logs enabled to the correct level.


# How to run

## For developers

In VSCODE "Run and Debug" click run on "Backend: Remote". (It will execute `docker compose -f docker-compose.yaml -f docker-compose.debug.yaml up --build` internally)

It might take some time, since it is building all the docker images and running everything first, but you get a full debug context attached once it runs


- It exposes port 8000 (backend), 8080 (frontend), 5678 (backend debugger), 6379 (redis)
- It activates DEBUG logging
- It attaches a debugger to the backend
- The backend has auto-reload, so just modify a file in the backend section and explore that it autoreloads correctly, no need to re-run it (It should say "listening..." again when it does so)
- The frontend HTML is served plainly, it doesn't have auto-reload, but you can refresh the page manually and see the new content
- NGINX is a mess to work with

## Without debugging

Simply run

```bash
docker compose up -d --build
```

# Large files

There are two ways of running, a local and a redis way. The redis way is activated right now

In both cases, large files are memory constrained, as long as the number of songs and days is bounded below the available memory.

In the redis version, I believe that for very large files, it will start to use disk at some point and become slower, but it won't fail. (Redis is great)

# NGINX

NGINX here is simulating a upload server with a shared file-service that you can stream over the internet to our server (Like S3, a ntfs server, etc). It proxy's the backend server, saves the file in a network volume, and provides to the backend the necessary information to know where to find that file. If you are feeding a large blob to python directly, you are looking for trouble.

Also, this NGINX module used here can do resumable downloads! (Even though it is disabled here)

See [the docs](https://www.nginx.com/resources/wiki/modules/upload/)

# Backend

Extra information on the backend implementation and how to read it [here](./backend/README.md)

# Frontend

The frontend is as ugly as it gets... I did want to try React Aria, which is new, but... not enough time on holidays.

# Tests

Linting and tests run automatically with github actions.


# TODO

- Create `pyproject.toml` (See https://github.com/pgjones/hypercorn/blob/main/pyproject.toml)
  - Add `tox`  to it (See https://stackoverflow.com/a/72258987/7346915 to get started)
  - Add poetry for version mnagement

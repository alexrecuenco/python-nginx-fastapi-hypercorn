# syntax=docker/dockerfile:1


# File created with docker init

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.11.6
FROM python:${PYTHON_VERSION} as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN pip install --upgrade pip
# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.backend.txt,target=requirements.backend.txt \
    --mount=type=bind,source=requirements.processor.txt,target=requirements.processor.txt \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


FROM base as prod
# Switch to the non-privileged user to run the application.
USER appuser


# Expose the port that the application listens on.
EXPOSE 8080


COPY ./module /app/
COPY ./*.py /app/
COPY ./*.toml /app/

CMD [ "hypercorn", "--config", "hypercorn.toml", "main:app"]

FROM base as debug
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.backend.txt,target=requirements.backend.txt \
    --mount=type=bind,source=requirements.processor.txt,target=requirements.processor.txt \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    --mount=type=bind,source=requirements.test.txt,target=requirements.test.txt \
    python -m pip install -r requirements.test.txt

# Switch to the non-privileged user to run the application.
USER appuser




COPY --from=PROD /app/ /app/

# Expose the port that the application listens on.
EXPOSE 8080
EXPOSE 5678
ENV DEBUG=1

CMD ["python", "-Xfrozen_modules=off", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "hypercorn", "--config", "hypercorn.toml", "--reload", "--log-level", "DEBUG", "--debug", "main:app"]

FROM python:3.11-alpine as build
RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.backend.txt /app/
COPY ./requirements.processor.txt /app/

RUN pip install -r requirements.backend.txt -r requirements.processor.txt

EXPOSE 8000

FROM build as prod
COPY ./module /app/
COPY ./*.py /app/
COPY ./*.toml /app/

CMD [ "hypercorn", "--config", "hypercorn.toml", "main:app"]

FROM build as debug

COPY ./requirements.test.txt /app/
RUN pip install -r requirements.test.txt

COPY --from=PROD /app/ /app/

EXPOSE 5678
ENV DEBUG=1

CMD ["python", "-Xfrozen_modules=off", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "hypercorn", "--config", "hypercorn.toml", "--reload", "--log-level", "DEBUG", "--debug", "main:app"]

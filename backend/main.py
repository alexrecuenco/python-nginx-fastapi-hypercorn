import logging
from dataclasses import dataclass
from os import getenv

from fastapi import Depends, FastAPI, Form, Request

logger = logging.getLogger(__file__)
app = FastAPI()


@app.get("/")
def read_root():
    return {"ok": 200}


@dataclass
class SimpleForm:
    name: int = Form(...)
    content_type: str = Form(...)
    path: str = Form(...)
    size: int = Form(...)


@app.post("/uploads")
async def receive_upload(request: Request):
    async with request.form() as form:
        logger.info("uploaded object %r", form)
        f = open(form.get("file.path"))
        lines = f.readlines()
        print(lines)
        print(lines)

    return {"Hello": "Form"}

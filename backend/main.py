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
    csv_name: str = Form(...)
    csv_content_type: str = Form(...)
    csv_path: str = Form(...)
    csv_size: int = Form(...)


@app.post("/uploads")
async def receive_upload(form: SimpleForm = Depends()):
    print(open(form.csv_path).readlines())

    return {"Hello": "Form"}

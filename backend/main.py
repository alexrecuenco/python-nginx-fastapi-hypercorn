import asyncio
import logging
import os
import uuid
from dataclasses import asdict, dataclass
from enum import Enum

import aiofiles
from fastapi import Depends, FastAPI, Form, HTTPException
from module import AsyncTaskManager, ProcessCSVConfig, process_csv
from module.async_counter import CounterType
from starlette.responses import RedirectResponse

if os.getenv("DEBUG"):
    logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__file__)
app = FastAPI()


_DOWNLOAD_FOLDER = "/var/www/site/downloads"


class AllowedContentType(str, Enum):
    csv = "text/csv"


@dataclass
class SimpleForm:
    csv_name: str = Form(...)
    csv_content_type: AllowedContentType = Form(...)
    csv_path: str = Form(...)
    csv_size: int = Form(...)


async def process_task(form: SimpleForm, task_id: str):
    async with AsyncTaskManager.manage_processing(task_id) as task:
        async with aiofiles.open(form.csv_path) as f:
            output_path = os.path.join(_DOWNLOAD_FOLDER, task.output_filename)
            # TODO: Use in-memory counter if form.csv_size is small
            config = ProcessCSVConfig(
                output_path=output_path, counter_type=CounterType.redis
            )
            await process_csv(f, config=config)


def future_process_task(form: SimpleForm) -> str:
    # Run the async task without waiting for it to complete
    task_id = str(uuid.uuid4())
    asyncio.create_task(process_task(form, task_id), name=f"processing:{task_id}")
    return task_id


@app.get("/")
def health_check():
    return {"ok": 200}


@app.post("/uploads")
async def receive_upload(form: SimpleForm = Depends()):
    task_id = future_process_task(form)
    return {"task_id": task_id}


@app.get("/uploads/{task_id}")
async def is_processing_request(task_id: str):
    task = await AsyncTaskManager.find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    match task.status:
        case "done":
            # TODO: Add query parameter with filename Since ?filename=blah.csv would work
            return RedirectResponse(url=f"/downloads/{task.output_filename}")
        case "error":
            raise HTTPException(status_code=500, detail=asdict(task))
        case "processing":
            return asdict(task)

import json
from typing import Union

import aiofiles
from aiofiles import os
from fastapi import Form, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
from starlette import status


class Checker:
    def __init__(self, model: BaseModel):
        self.model = model

    async def __call__(self, data: str = Form(...)):
        try:
            if data is not None:
                return self.model.model_validate_json(data)
            else:
                return None
        except ValidationError as e:
            raise HTTPException(
                detail=jsonable_encoder(e.errors()),
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

class SchemaUtils:
    @staticmethod
    def generate_example(model: BaseModel):
        example = {}
        for field, field_info in model.schema()["properties"].items():
            example[field] = field_info
        return json.dumps(example, indent=2)

class Files:
    @staticmethod
    async def load(file_path: str, file: UploadFile):
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = file.file.read()
            await out_file.write(content)

    @staticmethod
    async def delete(file_path: str):
        await os.remove(file_path)


import pathlib
import aiofiles
import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.middleware.cors import CORSMiddleware
import pipeline
import time

app = FastAPI()
p = pathlib.Path('files')
p.mkdir(parents=True, exist_ok=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/upload')
async def process_file(in_file: UploadFile = File(...)):
    async with aiofiles.open(p / in_file.filename, 'wb') as out_file:
        content = await in_file.read()
        await out_file.write(content)
    return pipeline.predict(str(p / in_file.filename))


if __name__ == '__main__':
    uvicorn.run('app:app', use_colors=True, reload=True)

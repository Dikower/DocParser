import logging
import pathlib
import time
import asyncio
import aiofiles
import httpx
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from starlette.middleware.cors import CORSMiddleware

import pipeline


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


async def register_doc(file_path, nomenclatureId):
    print('Started registration')
    start = time.time()
    async with httpx.AsyncClient() as client:
        res = await client.post(
            'http://elib-hackathon.psb.netintel.ru/elib/api/service/documents',
            headers={'Authorization': 'Basic ZWxpYi1zdXBlcnVzZXI6MTIz'},
            data={'createRequest': '{"documentNomenclatureId": "' + nomenclatureId + '"}'},
            files={'attachments': open(file_path, 'rb')}
        )
        print(f'Registered new doc: {res.text}')
        print(f'Took: {round(time.time() - start, 4)}s')



@app.post('/upload')
async def process_file(in_file: UploadFile = File(...)):
    start = time.time()

    async with aiofiles.open(p / in_file.filename, 'wb') as out_file:
        content = await in_file.read()
        await out_file.write(content)
    try:
        print('Start pipeline')
        result, used_ocr = pipeline.predict(str(p / in_file.filename))
        print(f'Finished pipeline, took: {round(time.time() - start, 4)}s')
        reg_start = time.time()
        asyncio.create_task(register_doc(p / in_file.filename, result['result']['code']))
        end = time.time()
        result['stats']['startAt'] = start
        result['stats']['endAt'] = end
        result['stats']['took'] = end - start
        result['stats']['usedOCR'] = used_ocr
        return result
    except:
        raise HTTPException(415, 'Wrong file type was passed')
    # finally:
    #     os.remove(p / in_file.filename)


if __name__ == '__main__':
    uvicorn.run('app:app', use_colors=True, reload=True)

import uvicorn
from fastapi import FastAPI

from db import create_db

app = FastAPI()


@app.get('/minigame/health')
async def root():
    return 'GOGO Minigame Service OK'


if __name__ == '__main__':
    create_db()
    uvicorn.run(app, host='0.0.0.0', port=8000)
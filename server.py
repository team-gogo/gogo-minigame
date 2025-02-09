import uvicorn
from fastapi import FastAPI

from db import create_db
from eureka import init_eureka

app = FastAPI()

@app.get('/minigame/health')
async def root():
    return 'GOGO Minigame Service OK'


if __name__ == '__main__':
    try:
        create_db()
        init_eureka()
        uvicorn.run(app, host='0.0.0.0', port=8086)
    except Exception as e:
        exit(1)

from fastapi import FastAPI

app = FastAPI()


@app.get('/minigame/health')
async def root():
    return 'GOGO Minigame Service OK'
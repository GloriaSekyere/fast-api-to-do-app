from fastapi import FastAPI
import uvicorn
from web.task import router as task_router

app = FastAPI()

app.include_router(task_router)

@app.get("/")
def root():
    return "We're Live"


if __name__=="__main__":
    uvicorn.run("main:app", reload=True)
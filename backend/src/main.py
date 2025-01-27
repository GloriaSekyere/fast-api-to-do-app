from fastapi import FastAPI
import uvicorn
from web.task import router as task_router
from web.user import router as user_router

app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)


@app.get("/")
def root():
    return "We're Live"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

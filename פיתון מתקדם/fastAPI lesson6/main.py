from fastapi import FastAPI
from pydantic import BaseModel, constr

app = FastAPI()


class Task(BaseModel):
    name: constr(min_length=1, max_length=10)
    des: str
    id: int
    status: bool


my_task = {
    "name": 'sari',
    "des": 'h.w python',
    "id": 1,
    "status": 1
}
task = Task(**my_task)
print(task)


@app.post("/")
def get_tasks():
    return Task(**my_task)

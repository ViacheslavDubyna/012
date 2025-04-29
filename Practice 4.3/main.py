from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def my_function():
    return {"message": "Hello World"}

@app.get("/id")
def f2():
    return {"id":None}

@app.get("/id")
def f2():
    return {"id":None}
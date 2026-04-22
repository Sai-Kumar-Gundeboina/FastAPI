from fastapi import FastAPI 

app = FastAPI()

def greet():
    return "Welcome to my page"
from fastapi import FastAPI


app = FastAPI()

@app.get("/hello")
    return ("status" : 200)




from fastapi import FastAPI
app=FastAPI(title="AI Service")

@app.get("/")
def root():
    return{"service":"AI Service","status":"running"}
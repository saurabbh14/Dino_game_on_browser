from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve the 'build' folder as static files
app.mount("/", StaticFiles(directory="build/web", html=True), name="static")
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
# Updated import path after project restructure
from routes import router as api_router
from contextlib import asynccontextmanager
import uvicorn
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # The startup logic is now handled entirely by the gRPC server.
    # We no longer need to call anything from the client on startup.
    print("FastAPI application startup... gRPC server should be running independently.")
    yield
    print("FastAPI application shutdown.")

app = FastAPI(
    title="Keithley 2230G Remote Controller",
    description="Remote control API for Keithley 2230G Power Supply via gRPC",
    version="2.1.0", # Version bump for the fix
    lifespan=lifespan
)

# Ensure the 'static' directory exists and serve files from it
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include all the API endpoints from routes.py
app.include_router(api_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serves the main index.html file."""
    try:
        with open("static/index.html", "r") as file:
            return file.read()
    except FileNotFoundError:
        # Provide a helpful message if the UI file is missing
        return (
            "<h1>Error: static/index.html not found</h1>"
            "<p>Please ensure the index.html file is in a 'static' directory.</p>"
        )


if __name__ == "__main__":
    print("🚀 Starting FastAPI Web Server...")
    print("   Please ensure the gRPC server is running in a separate terminal with 'python grpc_server.py'")
    print("   Access the web interface at: http://localhost:8000")
    print("   API documentation at: http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
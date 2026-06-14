from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base
from app.models import driver, order
from app.routes import drivers, orders
from app.routes import websocket

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DispatchIQ", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drivers.router)
app.include_router(orders.router)
app.include_router(websocket.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/dashboard")
async def dashboard():
    return FileResponse("static/index.html")

@app.get("/driver")
async def driver_portal():
    return FileResponse("static/driver.html")

@app.get("/home")
async def home():
    return FileResponse("static/home.html")


@app.get("/request")
async def request_page():
    return FileResponse("static/request.html")

@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/home")
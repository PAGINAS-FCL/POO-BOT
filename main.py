from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from servicios.manejador_telegram import procesar_actualizacion_telegram
from utilidades.json_utils import cargar_json

app = FastAPI()

app.mount("/index", StaticFiles(directory="frontend", html=True), name="index")

@app.post("/webhook")
async def webhook_telegram(request: Request):
    datos = await request.json()
    return await procesar_actualizacion_telegram(datos)

@app.get("/ver_progreso")
async def ver_progreso():
    data = cargar_json("data/data.json")
    return JSONResponse(content=data)

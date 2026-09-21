from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI(
    title="AgroPulse Edge API - Telemetría y Diagnóstico Agrícola",
    description="Servicio backend para concentrar datos de nodos LoRaWAN rurales y alimentar servicios DaaS.",
    version="1.0.0"
)

class NodeTelemetry(BaseModel):
    node_id: str
    finca_name: str
    crop_type: str  # ej. "Café", "Plátano", "Cacao", "Ganadería/Pastos"
    soil_moisture: float
    air_temp: float
    air_humidity: float
    nitrogen_ppm: float
    health_status_code: int

@app.get("/")
def root():
    return {
        "system": "AgroPulse Edge Gateway",
        "region": "Colombia",
        "status": "Online",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/v1/telemetry")
async def receive_telemetry(data: NodeTelemetry):
    # Procesa la llegada de un paquete de radio relay
    alert_triggered = data.health_status_code in [2, 3]
    return {
        "status": "PROCESSED",
        "node_id": data.node_id,
        "finca": data.finca_name,
        "alert_notification_sent": alert_triggered,
        "recommended_action": "Activar fertirriego" if data.health_status_code == 1 else ("Aplicar fungicida preventivo" if data.health_status_code == 2 else "Sin acción requerida")
    }

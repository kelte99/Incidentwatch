from fastapi import FastAPI, HTTPException, Response
from typing import Optional

from .models import IncidentCreate, Incident
from .database import db
from .metrics import (
    request_count_total,
    open_incidents_gauge,
    in_progress_incidents_gauge,
    resolved_incidents_gauge,
)
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# FastAPI app
app = FastAPI(
    title="IncidentWatch API",
    description="Mini backend de gestión de incidencias IT con métricas estilo Prometheus",
    version="0.1.0"
)


def _refresh_incident_gauges():
    """Recalcula cuántas incidencias hay en cada estado y actualiza los gauges."""
    all_incidents = db.list_incidents()
    open_count = sum(1 for i in all_incidents if i.status == "open")
    in_progress_count = sum(1 for i in all_incidents if i.status == "in_progress")
    resolved_count = sum(1 for i in all_incidents if i.status == "resolved")

    open_incidents_gauge.set(open_count)
    in_progress_incidents_gauge.set(in_progress_count)
    resolved_incidents_gauge.set(resolved_count)


@app.post("/incidents", response_model=Incident, status_code=201)
def create_incident(payload: IncidentCreate):
    """Crea una nueva incidencia."""
    request_count_total.inc()
    incident = db.create_incident(payload)
    _refresh_incident_gauges()
    return incident


@app.get("/incidents", response_model=list[Incident])
def list_incidents(status: Optional[str] = None):
    """Lista todas las incidencias, opcionalmente filtradas por estado."""
    request_count_total.inc()

    if status not in (None, "open", "in_progress", "resolved"):
        raise HTTPException(status_code=400, detail="invalid status filter")

    incidents = db.list_incidents(status)
    return incidents


@app.get("/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: int):
    """Obtiene los detalles de una incidencia por ID."""
    request_count_total.inc()

    incident = db.get_incident(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="incident not found")
    return incident


@app.put("/incidents/{incident_id}/status", response_model=Incident)
def update_incident_status(incident_id: int, new_status: str):
    """Actualiza el estado de una incidencia."""
    request_count_total.inc()

    if new_status not in ("open", "in_progress", "resolved"):
        raise HTTPException(status_code=400, detail="invalid status")

    incident = db.update_status(incident_id, new_status)
    if incident is None:
        raise HTTPException(status_code=404, detail="incident not found")

    _refresh_incident_gauges()
    return incident


# ✅ Endpoint CORRECTO de métricas Prometheus
@app.get("/metrics")
def metrics():
    """Devuelve las métricas en formato Prometheus (texto plano)."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

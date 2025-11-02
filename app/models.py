from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

# Esto define el cuerpo que el cliente envía cuando crea una incidencia nueva
class IncidentCreate(BaseModel):
    title: str
    description: str
    priority: Literal["low", "medium", "high"]
    assigned_to: Optional[str] = None  # técnico asignado

# Esto define cómo devolvemos la incidencia completa (con id, estado, timestamps...)
class Incident(BaseModel):
    id: int
    title: str
    description: str
    priority: Literal["low", "medium", "high"]
    status: Literal["open", "in_progress", "resolved"]
    assigned_to: Optional[str] = None
    created_at: datetime
    updated_at: datetime

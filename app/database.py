from datetime import datetime
from typing import List, Optional
from .models import Incident, IncidentCreate

class IncidentDB:
    def __init__(self):
        self._incidents: List[Incident] = []
        self._next_id: int = 1

    def create_incident(self, data: IncidentCreate) -> Incident:
        now = datetime.utcnow()
        incident = Incident(
            id=self._next_id,
            title=data.title,
            description=data.description,
            priority=data.priority,
            status="open",
            assigned_to=data.assigned_to,
            created_at=now,
            updated_at=now,
        )
        self._incidents.append(incident)
        self._next_id += 1
        return incident

    def list_incidents(self, status: Optional[str] = None) -> List[Incident]:
        if status is None:
            return self._incidents
        return [i for i in self._incidents if i.status == status]

    def get_incident(self, incident_id: int) -> Optional[Incident]:
        for i in self._incidents:
            if i.id == incident_id:
                return i
        return None

    def update_status(self, incident_id: int, new_status: str) -> Optional[Incident]:
        incident = self.get_incident(incident_id)
        if incident is None:
            return None
        incident.status = new_status
        incident.updated_at = datetime.utcnow()
        return incident

db = IncidentDB()

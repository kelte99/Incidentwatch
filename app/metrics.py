from prometheus_client import Counter, Gauge

# Contador global de peticiones a la API
request_count_total = Counter(
    "request_count_total",  # <- este nombre es importante
    "Total number of HTTP requests received"
)

# Nº de incidencias con estado OPEN ahora mismo
open_incidents_gauge = Gauge(
    "incident_open_total",
    "Current number of OPEN incidents"
)

# Nº de incidencias con estado IN_PROGRESS ahora mismo
in_progress_incidents_gauge = Gauge(
    "incident_in_progress_total",
    "Current number of IN_PROGRESS incidents"
)

# Nº de incidencias con estado RESOLVED ahora mismo
resolved_incidents_gauge = Gauge(
    "incident_resolved_total",
    "Current number of RESOLVED incidents"
)

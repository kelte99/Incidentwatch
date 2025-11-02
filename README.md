
## 👨‍💻 Autor

**Kevin Ruiz Arroyo**  
🎓 Proyecto Capstone — Bootcamp DevOps & Cloud  


# 🧠 IncidentWatch

**IncidentWatch** es un microservicio backend desarrollado con **FastAPI** para la gestión y monitorización de incidencias IT dentro de una organización.  
Permite **crear, listar y actualizar tickets de incidencia**, mientras expone métricas internas en formato **Prometheus** para su posterior visualización en **Grafana**.

El proyecto está completamente **contenedorizado con Docker**, **desplegado en Kubernetes** y **monitorizado con Prometheus + Grafana**, cumpliendo con los principios de una aplicación **cloud-native**.

---

## 🏗️ Arquitectura del Proyecto

```mermaid
graph TD
    A[👤 Usuario / Navegador - HTTP Requests] --> B[Service: incidentwatch-service - NodePort 8000:32426/TCP]
    B --> C[Pod: incidentwatch - FastAPI + Prometheus Client]
    C -->|Expone /metrics| D[Prometheus - Deployment + Service 9090]
    D -->|Fuente de datos| E[Grafana - Dashboard 32300]
    E -->|Visualiza métricas| A

    subgraph Cluster_Kubernetes_(Minikube)
        B
        C
        D
        E
    end

    F[🐋 DockerHub (kelte99/incidentwatch)] --> C
    G[⚙️ YAMLs_de_Kubernetes_(IaC)] --> Cluster_Kubernetes_(Minikube)

⚙️ Tecnologías Utilizadas

FastAPI → Framework principal del backend

Prometheus Client (Python) → Exposición de métricas en /metrics

Grafana → Visualización de métricas en tiempo real

Docker → Contenedorización del microservicio

Kubernetes (Minikube) → Orquestación de contenedores

Terraform → Infraestructura como código

🚀 Ejecución local
🧩 Opción 1: Ejecutar con Uvicorn (modo desarrollo)

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

👉 Accede a la documentación interactiva:

En Docker → http://localhost:8000/docs

En Kubernetes → http://localhost:32426/docs

🐋 Opción 2: Construir y ejecutar con Docker

docker build -t kelte99/incidentwatch .
docker run -p 8000:8000 kelte99/incidentwatch


☸️ Opción 3: Desplegar en Kubernetes (Minikube)

kubectl create namespace monitoring
kubectl apply -f k8s/prometheus.yaml
kubectl apply -f k8s/grafana.yaml
kubectl apply -f k8s/incidentwatch.yaml

Verifica los pods y servicios:

kubectl get pods -n monitoring
kubectl get svc -n monitoring

Interfaces disponibles:

Prometheus → http://localhost:31121

Grafana → http://localhost:32300

Backend API → http://localhost:32426/docs

📊 Métricas expuestas

El endpoint /metrics expone información en formato Prometheus:

     Métrica                                 	Descripción
request_count_total	               Total de peticiones HTTP recibidas
incident_open_total	               Incidencias abiertas
incident_in_progress_total         Incidencias en progreso
incident_resolved_total	           Incidencias resueltas

Ejemplo de salida:
# HELP request_count_total Total number of HTTP requests received
# TYPE request_count_total counter
request_count_total 149

📈 Dashboard en Grafana

Una vez configurada la conexión en Grafana con la URL de Prometheus
http://prometheus-service.monitoring.svc.cluster.local:9090,
puedes crear un dashboard en tiempo real con las métricas anteriores.

Capturas incluidas en /img:

✅ swagger.png — Endpoints de la API

✅ metrics_endpoint.png — Endpoint /metrics

✅ prometheus_up.png — Target activo en Prometheus

✅ grafana_datasource.png — Fuente de datos configurada

✅ grafana_dashboard.png — Visualización de métricas

Estructura del repositorio

IncidentWatch/
├── app/
│   ├── main.py
│   ├── metrics.py
│   ├── database.py
│   ├── models.py
│   └── __init__.py
├── k8s/
│   ├── incidentwatch.yaml
│   ├── prometheus.yaml
│   └── grafana.yaml
├── Dockerfile
├── requirements.txt
├── README.md


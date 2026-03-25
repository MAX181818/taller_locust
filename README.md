# Taller Locust + FastAPI + MLflow

Este repositorio contiene una solución base para el taller:

1. API de inferencia con FastAPI.
2. Carga del modelo desde MLflow.
3. Imagen Docker para inferencia.
4. `docker-compose` para servir la API usando imagen publicada.
5. `docker-compose` para pruebas de carga con Locust.
6. Guía de experimentación para encontrar recursos mínimos y escalar réplicas.

## Estructura

- `app/main.py`: API de inferencia.
- `requirements.txt`: dependencias para runtime.
- `Dockerfile`: imagen de inferencia.
- `docker-compose.inference.yml`: despliegue de la API desde imagen publicada.
- `docker-compose.locust.yml`: escenario de pruebas de carga con Locust.
- `locust/locustfile.py`: script de carga.
- `docs/experiment_results.md`: plantilla de resultados del taller.

## 1) Preparar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` según tu caso:

- `MLFLOW_TRACKING_URI`: tracking server de MLflow.
- `MODEL_URI`: ruta del modelo, por ejemplo:
  - `models:/iris_model/Production`
  - `runs:/<run_id>/model`
- `PREDICT_TIMEOUT_SECONDS`: timeout de predicción.

## 2) Construir imagen de inferencia

```bash
docker build -t max181818/mlflow-fastapi-inference:latest .
```

## 3) Publicar imagen en DockerHub

```bash
docker login
docker push max181818/mlflow-fastapi-inference:latest
```

## 4) Levantar API con compose (imagen publicada)

```bash
docker compose -f docker-compose.inference.yml --env-file .env up -d
curl http://localhost:8000/health
```

## 5) Ejecutar pruebas de carga con Locust

### UI de Locust

```bash
docker compose -f docker-compose.locust.yml --env-file .env up --build
```

Abrir `http://localhost:8089`.

### Modo headless (rampa de 500 hasta 10.000)

```bash
docker compose -f docker-compose.locust.yml --env-file .env run --rm locust \
  --headless \
  --users 10000 \
  --spawn-rate 500 \
  --run-time 10m \
  --host http://inference:8000
```

## 6) Estrategia para encontrar recursos mínimos

1. Inicia con `cpus: "1.0"` y `memory: "1g"` en `inference`.
2. Reduce gradualmente memoria/CPU:
   - 1.0 CPU / 1g
   - 0.75 CPU / 768m
   - 0.50 CPU / 512m
   - 0.25 CPU / 384m
3. Para cada punto, ejecuta Locust a 10.000 usuarios (rampa 500).
4. Registra:
   - RPS estable
   - P95/P99
   - tasa de error
   - uso de CPU/memoria
5. El mínimo aceptable es el de menor recurso con error bajo y latencia dentro de objetivo.

## 7) Evaluar múltiple réplicas

Ajusta réplicas de `inference` en `docker-compose.locust.yml`:

```yaml
replicas: 1  # luego 2, 3, 4
```

Compara contra una sola instancia:

- ¿Sube RPS total?
- ¿Baja latencia p95/p99?
- ¿Disminuyen errores bajo la misma carga?
- ¿Puedes bajar recurso por réplica sin degradar SLA?

Registra todo en `docs/experiment_results.md`.

# Resultados del Taller Locust

Completa este documento con los resultados reales de tus ejecuciones.

## Configuración de prueba

- Fecha:
- Host/Hardware:
- Versión imagen inferencia:
- Modelo MLflow (`MODEL_URI`):
- Duración por corrida:
- Patrón de carga: hasta 10.000 usuarios, `spawn-rate=500`.

## 1) Búsqueda de recursos mínimos (1 réplica)

| CPU | Memoria | Usuarios máximos estables | RPS promedio | P95 (ms) | Error % | Observación |
|---|---:|---:|---:|---:|---:|---|
| 1.0 | 1G |  |  |  |  |  |
| 0.75 | 768M |  |  |  |  |  |
| 0.50 | 512M |  |  |  |  |  |
| 0.25 | 384M |  |  |  |  |  |

**Conclusión recursos mínimos (1 réplica):**

- CPU:
- Memoria:
- Justificación:

## 2) Escalamiento por réplicas

Usa la combinación mínima encontrada y luego prueba múltiples réplicas.

| Réplicas | Usuarios máximos estables | RPS promedio | P95 (ms) | Error % | ¿Se puede bajar recurso por réplica? |
|---:|---:|---:|---:|---:|---|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |

## 3) Respuestas del taller

1. **¿Es posible reducir más los recursos con múltiples instancias?**
   - Respuesta:
   - Evidencia:

2. **¿Cuál es la mayor cantidad de peticiones soportadas?**
   - Respuesta:
   - Evidencia:

3. **¿Qué diferencia hay entre una o múltiples instancias?**
   - Respuesta:
   - Evidencia:

4. **Si no se llega a 10.000 usuarios, ¿cuál fue el máximo alcanzado?**
   - Respuesta:
   - Evidencia:

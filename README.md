# Prueba Técnica — Kubernetes · Jenkins · Grafana

## Contexto

Se te proporciona un microservicio Python ya construido (carpeta `app/`). Tu tarea es montar la infraestructura completa para desplegarlo, automatizar su entrega y observar su comportamiento.

**Tiempo estimado:** 3–4 horas.

---

## La aplicación

El servicio expone los siguientes endpoints:

| Endpoint   | Descripción                                      |
|------------|--------------------------------------------------|
| `GET /`    | Responde 200 con estado y entorno actual         |
| `GET /health` | Liveness de la aplicación                    |
| `GET /ready`  | Readiness de la aplicación                   |
| `GET /slow`   | Endpoint con latencia aleatoria y fallos simulados (~15%) |
| `GET /metrics` | Métricas en formato Prometheus              |

La variable de entorno `APP_ENV` controla el entorno que devuelve `/`.

---

## Lo que debes entregar

Un repositorio Git con la siguiente estructura mínima:

```
prueba-k8s-jenkins-grafana/
├── app/                        # No modificar
├── k8s/                        # Manifiestos Kubernetes
├── Jenkinsfile                 # Pipeline CI/CD
├── grafana/
│   └── dashboard.json          # Dashboard exportado
└── README.md                   # Este archivo (puedes añadir sección "Cómo ejecutar")
```

---

## Requisitos por área

### Kubernetes

Desplegar la aplicación en un cluster Kubernetes con:

- Namespace dedicado para la prueba
- Deployment con **2 réplicas mínimo**
- Liveness probe y readiness probe correctamente configurados (no el mismo endpoint para ambos)
- Service que exponga la aplicación dentro del cluster
- Ingress con path `/app` apuntando al Service
- ConfigMap con las variables de entorno que necesite la app
- Secret para un valor sensible ficticio (puedes usar `DB_PASSWORD=supersecret`), montado como variable de entorno
- Garantizar que al menos 1 pod esté disponible en todo momento, incluso durante actualizaciones o mantenimiento del cluster

### Jenkins

Pipeline declarativo (`Jenkinsfile`) con los siguientes stages:

1. **Checkout** — clonar el repositorio
2. **Build** — construir la imagen Docker
3. **Test** — verificar que la imagen arranca y `/health` responde 200
4. **Push** — subir la imagen a un registry (puede ser local o ficticio con credenciales en Jenkins)
5. **Deploy** — aplicar los manifiestos en Kubernetes
6. **Smoke test** — verificar que la app responde correctamente tras el deploy
7. **Notify** — notificar resultado (Slack, email o log explícito)

Requisitos adicionales:
- Parámetro `TARGET_ENV` que permita elegir el entorno de destino
- Si el Smoke test falla → ejecutar rollback automático
- Las credenciales del registry **nunca** deben estar en el Jenkinsfile

### Grafana

Dashboard con **mínimo 5 paneles**:

- Estado de pods (Running / Pending / Failed)
- CPU y memoria por pod
- Request rate total (`/slow` genera tráfico continuo)
- Error rate (porcentaje de respuestas 5xx)
- Latencia: percentiles p50, p95 y p99

Requisito adicional:
- Al menos una **Alert Rule**: si el error rate supera el 5% durante 2 minutos → alerta critical
- El dashboard debe exportarse como JSON y commitearse en `grafana/dashboard.json`

---

## Criterios de evaluación

| Área      | Qué se valora                                                         |
|-----------|-----------------------------------------------------------------------|
| K8s       | Manifiestos funcionales, probes correctos, HPA y PDB configurados     |
| Jenkins   | Pipeline completo, rollback automático, credenciales seguras           |
| Grafana   | Dashboard legible, alertas configuradas, JSON exportado               |
| General   | Claridad del repositorio, reproducibilidad, README actualizado        |

---

## Notas

- Puedes usar Minikube, Kind o cualquier cluster K8s accesible.
- No se valorará la complejidad del cluster, sino la correctitud de los manifiestos y pipelines.
- El endpoint `/slow` genera latencia y errores aleatorios — úsalo para poblar las métricas de Grafana.

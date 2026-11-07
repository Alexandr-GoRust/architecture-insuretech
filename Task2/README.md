# Task2 — Динамическое масштабирование контейнеров

Тестовое приложение: `ghcr.io/yandex-practicum/scaletestapp` (порт 8080:
`GET /` — ID пода, `GET /metrics` — метрики Prometheus, счётчик `http_requests_total`).

## Часть 1. Масштабирование по утилизации памяти

| Файл | Назначение |
|---|---|
| `deployment.yaml` | Deployment: 1 реплика, лимит/реквест памяти 30Mi |
| `service.yaml` | Service (ClusterIP): 80 → 8080 |
| `hpa-memory.yaml` | HPA `autoscaling/v2`: memory Utilization 80%, min 1 / max 10 |
| `locustfile.py` | сценарий нагрузки Locust (GET / каждые 1–5 c) |
| `run-load.sh` | генерация нагрузки headless-режимом |
| `logs/scaling-memory.log` | лог `kubectl get hpa/deploy` до/во время/после нагрузки |

Порядок воспроизведения:

```bash
minikube start --addons=metrics-server
kubectl apply -f deployment.yaml -f service.yaml -f hpa-memory.yaml
minikube service scaletestapp --url        # адрес приложения
locust -f locustfile.py --headless -u 300 -r 30 --run-time 4m -H <URL>
kubectl get hpa -w                         # реплики растут при утилизации >80%
```

## Часть 2. Масштабирование по RPS

| Файл | Назначение |
|---|---|
| `kube-prometheus-stack-values.yaml` | Prometheus Operator (community helm chart) |
| `prometheus-adapter-values.yaml` | адаптер: `http_requests_total` → `http_requests_per_second` (rate 30s) в custom.metrics.k8s.io |
| `hpa-rps.yaml` | HPA по внешней метрике RPS: `averageValue: 10` на под |
| `logs/prometheus-*.png` | скриншоты Prometheus UI (Targets/Graph — метрика приложения) |
| `logs/scaling-rps.log` | лог масштабирования под нагрузкой |

Порядок воспроизведения:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prom prometheus-community/kube-prometheus-stack -n monitoring --create-namespace -f kube-prometheus-stack-values.yaml
helm install adapter prometheus-community/prometheus-adapter -n monitoring -f prometheus-adapter-values.yaml
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1          # метрика доступна
kubectl apply -f hpa-rps.yaml
locust -f locustfile.py --headless -u 150 -r 15 --run-time 4m -H <URL>
kubectl get hpa scaletestapp-hpa-rps -w
```

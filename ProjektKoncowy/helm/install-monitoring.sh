#!/bin/bash

# Wczytaj zmienne środowiskowe
source ./.env

# Dodaj repozytorium Prometheusa
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Stwórz tymczasową konfigurację
cat << EOF > monitoring-values.yaml
grafana:
  enabled: false

nodeExporter:
  enabled: false

kubeStateMetrics:
  enabled: false

# Wyłącz wszystkie domyślne reguły i monitory
defaultRules:
  create: false
  rules:
    alertmanager: false
    etcd: false
    general: false
    k8s: false
    kubeApiserver: false
    kubeApiserverAvailability: false
    kubeApiserverError: false
    kubeApiserverSlos: false
    kubePrometheusGeneral: false
    kubePrometheusNodeAlerting: false
    kubePrometheusNodeRecording: false
    kubeScheduler: false
    kubeStateMetrics: false
    kubelet: false
    kubernetesApps: false
    kubernetesResources: false
    kubernetesStorage: false
    kubernetesSystem: false
    nodeExporterAlerting: false
    nodeExporterRecording: false
    prometheus: false
    prometheusOperator: false

prometheus:
  prometheusSpec:
    serviceMonitorSelectorNilUsesHelmValues: false
    serviceMonitorSelector:
      matchLabels:
        release: monitoring-stack

kubeApiServer:
  enabled: false
kubeControllerManager:
  enabled: false
kubeScheduler:
  enabled: false
kubeProxy:
  enabled: false
kubeEtcd:
  enabled: false
kubelet:
  enabled: false
coreDns:
  enabled: false

alertmanager:
  enabled: true
  config:
    global:
      resolve_timeout: 5m
      smtp_smarthost: 'smtp.gmail.com:587'
      smtp_from: "$SMTP_USERNAME"
      smtp_auth_username: "$SMTP_USERNAME"
      smtp_auth_password: "$SMTP_PASSWORD"
      smtp_require_tls: true
    route:
      group_by: ['alertname']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 1h
      receiver: 'email-notifications'
    receivers:
    - name: 'email-notifications'
      email_configs:
      - to: 's24353@pjwstk.edu.pl'
        send_resolved: true

    # ADD this "null" receiver:
    - name: 'null'
      # e.g. a webhook pointing to nowhere, effectively discarding alerts
      webhook_configs:
      - url: http://127.0.0.1:9
EOF

# Instaluj Prometheus Stack
helm install monitoring-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  -f monitoring-values.yaml

helm install blackbox-exporter prometheus-community/prometheus-blackbox-exporter \
  --namespace monitoring \

# Usuń tymczasowy plik
rm monitoring-values.yaml
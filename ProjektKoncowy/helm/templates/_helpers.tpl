{{/*
Expand the name of the chart.
*/}}
{{- define "asi.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "asi.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "asi.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "asi.labels" -}}
helm.sh/chart: {{ include "asi.chart" . }}
{{ include "asi.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}nameOverride
{{- end }}

{{/*
Selector labels
*/}}
{{- define "asi.selectorLabels" -}}
app.kubernetes.io/name: {{ include "asi.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Monitoring fullname
*/}}
{{- define "asi.monitoring.fullname" -}}
{{- printf "%s-monitoring" (include "asi.fullname" .) -}}
{{- end -}}

{{/*
Monitoring labels
*/}}
{{- define "asi.monitoring.labels" -}}
{{ include "asi.labels" . }}
app.kubernetes.io/component: monitoring
{{- end -}}

{{/*
Monitoring selector labels
*/}}
{{- define "asi.monitoring.selectorLabels" -}}
{{ include "asi.selectorLabels" . }}
app.kubernetes.io/component: monitoring
{{- end -}}
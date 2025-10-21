# Sistema de Agente Autónomo para Gestión de Infraestructura Dokploy
## Proyecto: InfraGuardian AI - Dokploy Edition

> **Especialmente diseñado para infraestructura 100% Dokploy + Docker Compose**
>
> **🆕 Powered by GPT-OSS 20B (OpenAI Open Source) - 100% Local, $0/mes**

### 🎯 Highlights del Proyecto

- 🤖 **GPT-OSS 20B**: Primer modelo open source de OpenAI (Apache 2.0)
- 💰 **Costo Operacional**: $0/mes (todo local en RTX 5090)
- 🔒 **Privacidad Total**: Cero datos enviados a terceros
- ⚡ **Function Calling**: OpenAI-grade, superior a Llama/Qwen
- 🎛️ **Reasoning Ajustable**: Low/Medium/High según criticidad
- 📦 **16GB VRAM**: Cabe perfecto en tu RTX 5090
- 🚀 **6 Semanas**: Plan de implementación completo

---

## 📋 Índice

1. [Contexto de Infraestructura](#contexto-de-infraestructura)
2. [Visión General](#visión-general)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Integración con Dokploy](#integración-con-dokploy)
5. [Stack Tecnológico](#stack-tecnológico)
6. [GPT-OSS 20B: El Cerebro del Agente](#gpt-oss-20b-el-cerebro-del-agente)
7. [Componentes Principales](#componentes-principales)
8. [Requerimientos](#requerimientos)
9. [Plan de Implementación](#plan-de-implementación)
10. [Casos de Uso Dokploy](#casos-de-uso-dokploy)
11. [Estimaciones](#estimaciones)

---

## 🏢 Contexto de Infraestructura

### Stack Actual

Tu infraestructura completa corre sobre:

```
┌─────────────────────────────────────────┐
│         DOKPLOY (Servidor VPS)          │
├─────────────────────────────────────────┤
│                                         │
│  ┌────────────────────────────────┐    │
│  │   Docker Compose Projects      │    │
│  ├────────────────────────────────┤    │
│  │                                │    │
│  │  • Granada Shariff             │    │
│  │    - frontend (Next.js)        │    │
│  │    - api (FastAPI)             │    │
│  │    - postgres                  │    │
│  │    - redis                     │    │
│  │    - celery                    │    │
│  │                                │    │
│  │  • SaaS RAG                    │    │
│  │    - saas-rag-fastapi          │    │
│  │    - frontend (Next.js)        │    │
│  │    - postgres                  │    │
│  │    - redis                     │    │
│  │    - mongodb                   │    │
│  │    - weaviate                  │    │
│  │    - voicechat-api             │    │
│  │                                │    │
│  │  • MCP Servers                 │    │
│  │    - mcp-server (FastAPI)      │    │
│  │    - postgres                  │    │
│  │                                │    │
│  │  • Configs Servidor            │    │
│  │    - registry                  │    │
│  │    - minio                     │    │
│  │    - rustdesk                  │    │
│  │                                │    │
│  │  • YoReparo                    │    │
│  │    - frontend                  │    │
│  │    - backend                   │    │
│  │    - postgres                  │    │
│  │                                │    │
│  │  • Random Test                 │    │
│  │    - n8n                       │    │
│  │                                │    │
│  └────────────────────────────────┘    │
│                                         │
│  Gestión:                               │
│  • Dokploy API                          │
│  • Traefik (reverse proxy)              │
│  • Docker Engine                        │
│  • Networking automático                │
│  • SSL/TLS automático                   │
│                                         │
└─────────────────────────────────────────┘
```

### Ventajas de Esta Arquitectura

1. **Centralización Total**: Todo gestionado desde Dokploy
2. **API Unificada**: 259 endpoints para control completo
3. **Docker Nativo**: Todas las operaciones son Docker-based
4. **Auto-configuración**: Traefik, SSL, networking automático
5. **Compose-First**: Todos los servicios definidos en docker-compose.yml

### Implicaciones para el Agente

**SIMPLIFICACIÓN:**
- ❌ No necesitas SSH remoto a múltiples servidores
- ❌ No necesitas múltiples estrategias de deployment
- ❌ No necesitas gestión manual de Kubernetes/VMs
- ✅ **TODO** se hace vía Dokploy API + Docker API
- ✅ Foco 100% en Compose/Containers
- ✅ Menor superficie de ataque

---

## 🎯 Visión General

**InfraGuardian AI - Dokploy Edition** es un agente autónomo especializado en infraestructura Dokploy, que entiende profundamente:

- Docker Compose services
- Dokploy projects y environments
- Container lifecycle (Traefik, health checks, etc.)
- Deployment workflows vía Dokploy
- Logs y métricas de containers

### Propuesta de Valor Específica

- **Gestión de Compose**: Entiende relaciones entre servicios (postgres→api→frontend)
- **Rollback Inteligente**: Usa Dokploy deployment history
- **Health Checks**: Monitorea health checks de Traefik + Docker
- **Logs Centralizados**: Analiza logs de todos los containers vía Docker API
- **Auto-healing**: Restart, redeploy, rollback automático

---

## 🏗️ Arquitectura del Sistema

### Arquitectura Específica Dokploy

```
┌─────────────────────────────────────────────────────────────────┐
│                     TELEGRAM BOT (Interfaz)                     │
│  - Comandos: /status, /restart, /logs, /deploy                 │
│  - Conversación: "¿Por qué está caído Granada?"                │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   LANGGRAPH AGENT CORE                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Dokploy-Aware Agent                         │  │
│  │                                                          │  │
│  │  States:                                                 │  │
│  │  1. MONITOR → Detecta anomalías en containers          │  │
│  │  2. ANALYZE → Analiza logs + métricas Docker           │  │
│  │  3. PLAN    → Decide acción (restart/redeploy/scale)   │  │
│  │  4. EXECUTE → Ejecuta vía Dokploy API                  │  │
│  │  5. VERIFY  → Valida health checks                     │  │
│  │  6. LEARN   → Actualiza knowledge base                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────┐    ┌────────────────────────────────┐    │
│  │GPT-OSS 20B      │    │   Knowledge Base               │    │
│  │ (Local/RTX5090) │    │   - Compose patterns           │    │
│  │  - Entiende     │    │   - Dokploy API calls          │    │
│  │    Compose      │    │   - Container dependencies     │    │
│  │  - Relaciones   │    │   - Runbooks específicos       │    │
│  │    servicios    │    │   - ChromaDB (local)           │    │
│  │  - Function     │    │                                │    │
│  │    calling      │    │                                │    │
│  └─────────────────┘    └────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                  HERRAMIENTAS (Tools)                           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         DOKPLOY API CLIENT (Principal)                  │   │
│  │                                                         │   │
│  │  Projects:                                              │   │
│  │  - project.all()                                        │   │
│  │  - project.one(projectId)                               │   │
│  │                                                         │   │
│  │  Compose:                                               │   │
│  │  - compose.one(composeId)                               │   │
│  │  - compose.deploy(composeId)                            │   │
│  │  - compose.redeploy(composeId)                          │   │
│  │  - compose.start(composeId)                             │   │
│  │  - compose.stop(composeId)                              │   │
│  │  - compose.loadServices(composeId)                      │   │
│  │                                                         │   │
│  │  Domains:                                               │   │
│  │  - domain.byComposeId(composeId)                        │   │
│  │  - domain.validateDomain(domain)                        │   │
│  │                                                         │   │
│  │  Deployments:                                           │   │
│  │  - deployment.all()                                     │   │
│  │  - deployment.allByCompose(composeId)                   │   │
│  │                                                         │   │
│  │  Databases:                                             │   │
│  │  - postgres.one(postgresId)                             │   │
│  │  - postgres.restart(postgresId)                         │   │
│  │  - mysql.one(mysqlId)                                   │   │
│  │  - mongo.one(mongoId)                                   │   │
│  │  - redis.one(redisId)                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         DOCKER API CLIENT (Complementario)              │   │
│  │                                                         │   │
│  │  - docker.containers.list()                             │   │
│  │  - docker.containers.get(id).logs()                     │   │
│  │  - docker.containers.get(id).stats()                    │   │
│  │  - docker.containers.get(id).restart()                  │   │
│  │  - docker.images.prune()                                │   │
│  │  - docker.volumes.prune()                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         ANALISIS DE LOGS                                │   │
│  │                                                         │   │
│  │  - parse_container_logs(container_id)                   │   │
│  │  - search_error_patterns(logs)                          │   │
│  │  - extract_stack_traces(logs)                           │   │
│  │  - correlate_service_errors(compose_services)           │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    MONITOREO                                    │
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐                 │
│  │  Docker Stats    │    │  Dokploy Health  │                 │
│  │  - CPU/RAM       │    │  - Health checks │                 │
│  │  - Network I/O   │    │  - Deploy status │                 │
│  │  - Disk I/O      │    │  - Domain status │                 │
│  └──────────────────┘    └──────────────────┘                 │
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐                 │
│  │  Uptime Kuma     │    │  Custom Metrics  │                 │
│  │  - Availability  │    │  - API latency   │                 │
│  │  - Response time │    │  - Queue depth   │                 │
│  └──────────────────┘    └──────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔗 Integración con Dokploy

### API de Dokploy: Tu Única Interfaz

Tienes acceso a **259 endpoints**. Los más relevantes para el agente:

#### Compose Management (23 endpoints)

```python
# El agente usará principalmente estos:

# Información
compose.one(composeId)              # Obtener info completa
compose.loadServices(composeId)     # Listar servicios del compose

# Lifecycle
compose.deploy(composeId)           # Deploy from scratch
compose.redeploy(composeId)         # Redeploy
compose.start(composeId)            # Start todos los servicios
compose.stop(composeId)             # Stop todos los servicios

# Troubleshooting
compose.one(composeId).env          # Ver variables de entorno
compose.one(composeId).composeFile  # Ver docker-compose.yml
deployment.allByCompose(composeId)  # Ver historial de deploys

# Rollback
# Dokploy guarda historial, el agente puede:
# 1. Ver deployment anterior exitoso
# 2. Trigger redeploy con ese deployment

# Domains
domain.byComposeId(composeId)       # Ver dominios configurados
domain.validateDomain(domain)       # Validar DNS
```

#### Docker API Integration

```python
# Para métricas y logs detallados
import docker

client = docker.from_env()

# Obtener containers de un compose
# Dokploy nombra containers: {projectName}-{serviceName}-{hash}
containers = client.containers.list(
    filters={
        "label": f"com.docker.compose.project={project_name}"
    }
)

# Para cada container:
container.stats(stream=False)  # CPU, RAM, Network, Disk
container.logs(tail=1000)      # Últimas 1000 líneas
container.top()                # Procesos running
container.exec_run("df -h")    # Comandos dentro del container
```

### Ejemplo: Granada Shariff Project

Tu proyecto Granada Shariff tiene:

```yaml
services:
  frontend:
    - Port: 3000
    - Domain: granada.sphyrnasolutions.com
    - Health check: HTTP

  api:
    - Port: 8000
    - Domain: granada.back.sphyrnasolutions.com
    - Depends on: postgres, redis

  postgres:
    - Internal: No domain público
    - Volume: Persistent data

  redis:
    - Internal: No domain público

  celery:
    - Background worker
    - Depends on: redis, postgres
```

**El agente entiende estas relaciones:**

```python
# Si "frontend" está caído:
# 1. Check frontend container
# 2. Check si API está up (frontend depende de API)
# 3. Check postgres/redis (API depende de ellos)
# 4. Analizar logs en orden inverso de dependencia

# Si "postgres" está lento:
# 1. Afecta a: API, Celery
# 2. Indirectamente afecta: Frontend
# 3. Priorizar arreglo de postgres (cascada de efectos)
```

---

## 🛠️ Stack Tecnológico Optimizado

### Backend Core

```python
# Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0

# LangChain Stack
langchain==0.1.5
langgraph==0.0.20
langchain-ollama==0.0.1       # Para GPT-OSS 20B local

# Dokploy Integration
aiohttp==3.9.1                # Async HTTP para Dokploy API
pydantic==2.5.0               # Validación de datos API

# Docker Integration
docker==7.0.0                 # Docker Python SDK
docker-compose==1.29.2        # Parse docker-compose.yml

# Vector DB
chromadb==0.4.22              # Local, gratuito

# Telegram
python-telegram-bot==20.7

# Database
psycopg2-binary==2.9.9        # PostgreSQL
redis==5.0.1                  # Redis

# Utils
pyyaml==6.0.1                 # Parse YAML (runbooks + composes)
python-dotenv==1.0.0
```

### Herramientas Específicas Dokploy

```python
# src/integrations/dokploy_client.py
class DokployClient:
    """Cliente especializado para Dokploy API"""

    base_url = "https://settings.sphyrnasolutions.com/api"
    api_key = os.getenv("DOKPLOY_API_KEY")

    async def get_all_projects(self):
        """GET /project.all"""
        return await self._request("GET", "/project.all")

    async def get_compose_services(self, compose_id: str):
        """GET /compose.loadServices"""
        return await self._request("GET", "/compose.loadServices",
                                   params={"composeId": compose_id})

    async def deploy_compose(self, compose_id: str):
        """POST /compose.deploy"""
        return await self._request("POST", "/compose.deploy",
                                   json={"composeId": compose_id})

    async def get_deployment_history(self, compose_id: str):
        """GET /deployment.allByCompose"""
        return await self._request("GET", "/deployment.allByCompose",
                                   params={"composeId": compose_id})

# src/integrations/docker_client.py
class DockerComposeAnalyzer:
    """Analiza docker-compose.yml y containers"""

    def __init__(self):
        self.docker = docker.from_env()

    def get_compose_containers(self, project_name: str):
        """Obtener todos los containers de un compose"""
        return self.docker.containers.list(
            filters={
                "label": f"com.docker.compose.project={project_name}"
            }
        )

    def analyze_service_dependencies(self, compose_file: str):
        """Parse docker-compose.yml y extraer dependencias"""
        compose_data = yaml.safe_load(compose_file)
        services = compose_data.get("services", {})

        deps = {}
        for service_name, service_config in services.items():
            deps[service_name] = {
                "depends_on": service_config.get("depends_on", []),
                "links": service_config.get("links", []),
                "volumes_from": service_config.get("volumes_from", [])
            }
        return deps

    def get_service_health(self, container_id: str):
        """Health check de un servicio"""
        container = self.docker.containers.get(container_id)
        return {
            "status": container.status,
            "health": container.attrs.get("State", {}).get("Health", {}),
            "stats": container.stats(stream=False)
        }
```

---

## 🤖 GPT-OSS 20B: El Cerebro del Agente

### Por Qué GPT-OSS 20B

En agosto 2025, OpenAI lanzó **GPT-OSS** (20B y 120B) bajo licencia Apache 2.0, su primer modelo open source desde GPT-2. Para este proyecto, GPT-OSS 20B es la opción ideal:

#### Especificaciones Técnicas

```
Modelo: gpt-oss-20b
Arquitectura: Mixture of Experts (MoE)
Parámetros totales: 21B
Parámetros activos: 3.6B (solo 17% activo por inferencia)
Cuantización: MXFP4 nativa
VRAM requerida: 16GB (perfecto para RTX 5090)
Rendimiento: Similar a o3-mini de OpenAI
Licencia: Apache 2.0 (uso comercial libre)
```

#### Capacidades Clave para el Agente

✅ **Function Calling Nativo**: OpenAI-grade, superior a Llama/Qwen
✅ **Reasoning Ajustable**: Low/Medium/High según necesidad
✅ **Chain-of-Thought Visible**: Para debugging de decisiones
✅ **Web Browsing**: Capacidad integrada
✅ **Python Execution**: Puede ejecutar código
✅ **Structured Outputs**: JSON schemas nativos
✅ **Fine-tunable**: Especializable para tu infraestructura

#### Configuración de Reasoning Effort

```python
from langchain_ollama import ChatOllama

# Para monitoreo rutinario (rápido)
llm_fast = ChatOllama(
    model="openai/gpt-oss-20b",
    temperature=0.3,
    model_kwargs={"reasoning_effort": "low"}  # ~1-2s
)

# Para diagnósticos normales (balanceado)
llm_normal = ChatOllama(
    model="openai/gpt-oss-20b",
    temperature=0.5,
    model_kwargs={"reasoning_effort": "medium"}  # ~2-3s
)

# Para análisis complejos (profundo)
llm_deep = ChatOllama(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    model_kwargs={"reasoning_effort": "high"}  # ~4-6s
)
```

#### Ventajas vs Alternativas

| Característica | GPT-OSS 20B | Llama 3.1 70B | Claude API |
|----------------|-------------|---------------|------------|
| **Function calling** | ⭐⭐⭐⭐⭐ OpenAI | ⭐⭐⭐⭐ Bueno | ⭐⭐⭐⭐⭐ Excelente |
| **VRAM requerida** | 16GB | 40GB | 0GB |
| **Velocidad** | 2-3s | 5-8s | 1-2s |
| **Costo** | $0/mes | $0/mes | $10-30/mes |
| **Razonamiento** | ⭐⭐⭐⭐ o3-mini | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Cabe RTX 5090** | ✅ Perfecto | ⚠️ Offloading | ✅ API |
| **Structured out** | ✅ Nativo | ⚠️ Limitado | ✅ Nativo |
| **Privacidad** | ✅ 100% local | ✅ 100% local | ❌ Cloud |

#### Requisitos de Hardware

```
GPU: NVIDIA RTX 5090 (24GB VRAM) ✓ DISPONIBLE
VRAM usada: 16GB modelo + 2GB buffer
RAM: 32GB recomendada
Disco: 20GB para modelo cuantizado
CPU: Mínimo 8 cores (preprocesamiento)

Configuración óptima:
- RTX 5090: 24GB VRAM → 8GB libres
- Cuantización: Q4 (nativo en Ollama)
- Offloading: No necesario
```

#### Instalación

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Descargar GPT-OSS 20B (~12GB, toma 15min)
ollama pull openai/gpt-oss-20b

# Verificar
ollama run openai/gpt-oss-20b "Eres InfraGuardian AI"

# Autostart
sudo systemctl enable ollama
sudo systemctl start ollama
```

#### Integración con LangChain

```python
from langchain_ollama import ChatOllama
from langchain.tools import tool

# Inicializar LLM
llm = ChatOllama(
    model="openai/gpt-oss-20b",
    base_url="http://localhost:11434",
    temperature=0.5
)

# Definir herramientas
@tool
def restart_service(compose_id: str) -> str:
    """Reinicia servicio Docker Compose vía Dokploy"""
    # Implementación...
    return f"Service restarted"

# Agent con tools
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    llm,
    tools=[restart_service, get_logs]
)
```

---

## 🧩 Componentes Principales

### 1. Dokploy-Aware Agent

**Archivo:** `src/agent/dokploy_agent.py`

```python
from langgraph.graph import StateGraph
from langchain_ollama import ChatOllama

class DokployAgentState(TypedDict):
    """Estado del agente con contexto Dokploy"""
    # Contexto del problema
    incident_type: str              # "container_down", "high_cpu", etc.
    project_id: Optional[str]
    compose_id: Optional[str]
    service_name: Optional[str]

    # Datos recopilados
    compose_services: List[Dict]    # Servicios del compose
    container_stats: Dict           # Métricas Docker
    logs: str                       # Logs del container
    deployment_history: List[Dict]  # Historial de deploys

    # Análisis
    root_cause: Optional[str]       # Causa raíz identificada
    affected_services: List[str]    # Servicios afectados
    solution_plan: Optional[Dict]   # Plan de solución

    # Ejecución
    actions_taken: List[Dict]       # Acciones ejecutadas
    result: Optional[str]           # Resultado final


def create_dokploy_agent():
    """Crea el agente LangGraph especializado en Dokploy"""

    workflow = StateGraph(DokployAgentState)

    # Nodos
    workflow.add_node("detect_incident", detect_incident_node)
    workflow.add_node("gather_context", gather_dokploy_context)
    workflow.add_node("analyze_compose", analyze_compose_dependencies)
    workflow.add_node("diagnose", diagnose_with_llm)
    workflow.add_node("plan_solution", plan_dokploy_solution)
    workflow.add_node("execute_action", execute_via_dokploy)
    workflow.add_node("verify_fix", verify_health_checks)
    workflow.add_node("rollback", rollback_deployment)
    workflow.add_node("escalate", escalate_to_human)

    # Flujo
    workflow.set_entry_point("detect_incident")

    workflow.add_edge("detect_incident", "gather_context")
    workflow.add_edge("gather_context", "analyze_compose")
    workflow.add_edge("analyze_compose", "diagnose")

    workflow.add_conditional_edges(
        "diagnose",
        should_auto_fix,
        {
            "auto": "plan_solution",
            "manual": "escalate"
        }
    )

    workflow.add_edge("plan_solution", "execute_action")

    workflow.add_conditional_edges(
        "execute_action",
        check_execution_success,
        {
            "success": "verify_fix",
            "failure": "rollback"
        }
    )

    workflow.add_conditional_edges(
        "verify_fix",
        check_health,
        {
            "healthy": END,
            "unhealthy": "rollback",
            "unknown": "escalate"
        }
    )

    workflow.add_edge("rollback", "escalate")

    return workflow.compile()
```

### 2. Runbooks Específicos Dokploy

**Archivo:** `runbooks/compose_service_down.yaml`

```yaml
name: "Docker Compose Service Down"
description: "Servicio de un compose ha caído"

trigger:
  event: "container_unhealthy"
  scope: "docker_compose"

context_gathering:
  - action: "get_compose_info"
    tool: "dokploy.compose.one"
    params:
      composeId: "${incident.compose_id}"

  - action: "get_all_services"
    tool: "dokploy.compose.loadServices"
    params:
      composeId: "${incident.compose_id}"

  - action: "get_container_logs"
    tool: "docker.get_logs"
    params:
      container_id: "${incident.container_id}"
      tail: 1000

  - action: "get_deployment_history"
    tool: "dokploy.deployment.allByCompose"
    params:
      composeId: "${incident.compose_id}"

diagnosis:
  llm_prompt: |
    Analiza el siguiente escenario:

    Servicio caído: ${incident.service_name}
    Project: ${context.compose_info.name}
    Compose ID: ${incident.compose_id}

    Servicios en el compose:
    ${context.all_services}

    Últimos logs (1000 líneas):
    ${context.container_logs}

    Último deployment:
    ${context.deployment_history[0]}

    Diagnóstico:
    1. ¿Qué causó la caída?
    2. ¿Hay servicios dependientes afectados?
    3. ¿Es problema de código o infraestructura?
    4. ¿El último deploy introdujo el problema?

solutions:
  - name: "Restart via Dokploy"
    confidence_threshold: 0.9
    conditions:
      - error_type: "transient"
      - no_code_changes_needed: true

    actions:
      - tool: "dokploy.compose.start"
        params:
          composeId: "${incident.compose_id}"
        retry: 2
        wait_seconds: 10

      - tool: "verify_health"
        params:
          service_name: "${incident.service_name}"
        timeout: 60

  - name: "Redeploy Compose"
    confidence_threshold: 0.8
    conditions:
      - error_type: "deployment_issue"
      - config_changed: true

    actions:
      - tool: "dokploy.compose.redeploy"
        params:
          composeId: "${incident.compose_id}"
        wait_for_completion: true

      - tool: "verify_all_services"
        params:
          composeId: "${incident.compose_id}"

  - name: "Rollback to Previous Deployment"
    confidence_threshold: 0.7
    conditions:
      - recent_deployment: true
      - error_after_deploy: true
      - previous_deployment_successful: true

    actions:
      - tool: "get_previous_successful_deployment"
        params:
          composeId: "${incident.compose_id}"

      - tool: "dokploy.compose.deploy"
        params:
          composeId: "${incident.compose_id}"
          commitHash: "${previous_deployment.commit}"
        note: "Rollback automático al commit ${previous_deployment.commit}"

escalation:
  triggers:
    - all_solutions_failed: true
    - confidence_below: 0.6
    - critical_service: true

  notification:
    telegram:
      message: |
        ⚠️ Escalamiento requerido

        Servicio: ${incident.service_name}
        Proyecto: ${context.compose_info.name}

        Problema detectado:
        ${diagnosis.root_cause}

        Soluciones intentadas:
        ${actions_taken}

        Se requiere intervención manual.

        [Ver Logs] [Ver Compose] [Historial]
```

### 3. Herramientas Dokploy

**Archivo:** `src/tools/dokploy_tools.py`

```python
from langchain.tools import tool
from typing import Optional, List, Dict

@tool
def get_project_info(project_id: str) -> Dict:
    """
    Obtiene información completa de un proyecto Dokploy.

    Args:
        project_id: ID del proyecto

    Returns:
        Información del proyecto incluyendo todos sus composes,
        bases de datos, y environments
    """
    client = DokployClient()
    return await client.get_project(project_id)


@tool
def get_compose_services(compose_id: str) -> List[Dict]:
    """
    Lista todos los servicios de un Docker Compose.

    Args:
        compose_id: ID del compose en Dokploy

    Returns:
        Lista de servicios con su configuración
    """
    client = DokployClient()
    return await client.get_compose_services(compose_id)


@tool
def restart_compose_service(
    compose_id: str,
    service_name: Optional[str] = None
) -> Dict:
    """
    Reinicia un servicio específico o todo el compose.

    Args:
        compose_id: ID del compose
        service_name: Nombre del servicio (opcional, si None reinicia todo)

    Returns:
        Estado de la operación
    """
    if service_name:
        # Restart específico vía Docker API
        docker_client = docker.from_env()
        container = docker_client.containers.get(
            f"{compose_name}-{service_name}"
        )
        container.restart()
        return {"status": "restarted", "service": service_name}
    else:
        # Restart todo el compose vía Dokploy
        client = DokployClient()
        await client.compose_stop(compose_id)
        await asyncio.sleep(5)
        await client.compose_start(compose_id)
        return {"status": "restarted", "compose_id": compose_id}


@tool
def deploy_compose(compose_id: str) -> Dict:
    """
    Deploya o redeploya un compose completo.

    Args:
        compose_id: ID del compose

    Returns:
        Estado del deployment
    """
    client = DokployClient()
    result = await client.compose_deploy(compose_id)

    # Esperar a que termine el deployment
    deployment_id = result["deploymentId"]
    status = await wait_for_deployment(deployment_id)

    return {
        "deployment_id": deployment_id,
        "status": status,
        "success": status == "done"
    }


@tool
def get_compose_logs(compose_id: str, service_name: str, tail: int = 1000) -> str:
    """
    Obtiene los logs de un servicio del compose.

    Args:
        compose_id: ID del compose
        service_name: Nombre del servicio
        tail: Número de líneas a obtener

    Returns:
        Logs del servicio
    """
    # Primero obtener el nombre del proyecto
    client = DokployClient()
    compose_info = await client.compose_one(compose_id)
    project_name = compose_info["appName"]

    # Obtener container vía Docker
    docker_client = docker.from_env()
    containers = docker_client.containers.list(
        filters={
            "label": f"com.docker.compose.project={project_name}",
            "label": f"com.docker.compose.service={service_name}"
        }
    )

    if not containers:
        return f"No container found for service {service_name}"

    container = containers[0]
    logs = container.logs(tail=tail, timestamps=True)
    return logs.decode('utf-8')


@tool
def analyze_compose_health(compose_id: str) -> Dict:
    """
    Analiza el health de todos los servicios de un compose.

    Args:
        compose_id: ID del compose

    Returns:
        Estado de salud de cada servicio
    """
    client = DokployClient()
    compose_info = await client.compose_one(compose_id)
    services = await client.get_compose_services(compose_id)

    project_name = compose_info["appName"]

    # Analizar cada servicio
    docker_client = docker.from_env()
    health_report = {}

    for service in services:
        service_name = service["name"]

        containers = docker_client.containers.list(
            all=True,
            filters={
                "label": f"com.docker.compose.project={project_name}",
                "label": f"com.docker.compose.service={service_name}"
            }
        )

        if not containers:
            health_report[service_name] = {
                "status": "not_found",
                "healthy": False
            }
            continue

        container = containers[0]
        stats = container.stats(stream=False)

        health_report[service_name] = {
            "status": container.status,
            "healthy": container.status == "running",
            "cpu_percent": calculate_cpu_percent(stats),
            "memory_mb": stats["memory_stats"]["usage"] / 1024 / 1024,
            "restart_count": container.attrs["RestartCount"]
        }

    return health_report


@tool
def rollback_compose_deployment(compose_id: str) -> Dict:
    """
    Rollback al deployment anterior exitoso.

    Args:
        compose_id: ID del compose

    Returns:
        Estado del rollback
    """
    client = DokployClient()

    # Obtener historial
    deployments = await client.get_deployment_history(compose_id)

    # Buscar último deployment exitoso anterior al actual
    successful_deployments = [
        d for d in deployments
        if d["status"] == "done" and d != deployments[0]
    ]

    if not successful_deployments:
        return {
            "success": False,
            "error": "No previous successful deployment found"
        }

    previous = successful_deployments[0]

    # Trigger redeploy con ese commit
    # Nota: Dokploy no tiene endpoint directo de rollback,
    # pero podemos hacer checkout del commit anterior y redeploy
    result = await client.compose_redeploy(compose_id)

    return {
        "success": True,
        "rolled_back_to": previous["createdAt"],
        "deployment_id": result["deploymentId"]
    }
```

---

## 💼 Casos de Uso Dokploy Específicos

### Caso 1: Granada Shariff - API No Responde

**Escenario Real:**
El servicio `api` del proyecto Granada Shariff devuelve 502.

```
[02:15:00] 🔴 DETECCIÓN
  Uptime Kuma: granada.back.sphyrnasolutions.com → HTTP 502
  Domain ID: I4WmjE5TdAWBLF4RGFOcY
  ↓
[02:15:05] 🔍 CONTEXTO
  Agente obtiene vía Dokploy API:
  - Project: Granada Shariff (sNXBbGQT2Ic9V6qXVlhUu)
  - Compose: dashboard (56SmVbZnH2IMcA4fQHLUw)
  - Services: frontend, api, postgres, redis, celery

  Estado Docker:
  - frontend: ✓ running
  - api: ✗ restarting (exit code 137 - OOM killed)
  - postgres: ✓ running
  - redis: ✓ running
  - celery: ⚠ degraded (waiting for api)
  ↓
[02:15:15] 🧠 ANÁLISIS LLM
  Claude analiza:
  "El servicio API fue killed por OOM (Out of Memory).
   Exit code 137 indica que el kernel mató el proceso.

   Últimos logs muestran:
   - Memory usage creció gradualmente
   - Última operación: bulk insert de 500k registros
   - No hay memory leaks en código reciente

   Causa raíz: Límite de memoria muy bajo (2GB)
   vs operación legítima que requiere más.

   Servicios afectados:
   - API (down)
   - Celery (degraded, esperando API)
   - Frontend (partial, cachea algunas requests)

   Solución: Aumentar memoria + reiniciar"
  ↓
[02:15:30] 💡 PLAN
  Runbook: compose_service_oom.yaml
  Confianza: 92%

  Plan:
  1. Actualizar memory limit: 2GB → 4GB
  2. Restart servicio API
  3. Verificar celery se recupera
  4. Monitorear memory usage siguiente hora
  ↓
[02:15:40] 🔧 EJECUCIÓN
  1. Agente actualiza docker-compose.yml vía Dokploy:
     services:
       api:
         deploy:
           resources:
             limits:
               memory: 4G  # era 2G

  2. Trigger redeploy vía Dokploy API:
     POST /compose.redeploy
     { "composeId": "56SmVbZnH2IMcA4fQHLUw" }

  3. Espera deployment complete (90 segundos)
  ↓
[02:17:15] ✅ VERIFICACIÓN
  Health checks:
  - api: ✓ running, memory: 1.2GB/4GB
  - celery: ✓ running, processing jobs
  - frontend: ✓ all requests succeeding

  Domain check:
  - granada.back.sphyrnasolutions.com → HTTP 200 ✓
  ↓
[02:17:20] 📱 NOTIFICACIÓN
  Telegram:
  "✅ Incidente resuelto - Granada Shariff API

   🔴 Problema:
   API caída por OOM (memoria insuficiente)

   🔧 Solución aplicada:
   • Memory limit aumentado: 2GB → 4GB
   • Servicio redeployado
   • Tiempo de resolución: 2min 20s

   📊 Estado actual:
   • API: ✓ Healthy (1.2GB/4GB)
   • Celery: ✓ Processing
   • Frontend: ✓ All requests OK

   💡 Recomendación:
   Investigar el bulk insert de 500k registros.
   Considerar paginación o procesamiento por lotes.

   [Ver Logs] [Métricas]"
  ↓
[02:17:30] 📚 APRENDIZAJE
  Agente actualiza knowledge base:

  Pattern registrado:
  - Service: API (FastAPI)
  - Symptom: Exit code 137 + restarting loop
  - Root cause: OOM durante bulk operations
  - Solution: Increase memory + code optimization

  Runbook actualizado:
  - Threshold de alerta: >80% memory durante >5min
  - Auto-scale memory si disponible
  - Notificar sobre bulk operations sin pagination
```

### Caso 2: SaaS RAG - Weaviate Lento

**Escenario Real:**
Weaviate (vector DB) respondiendo muy lento, afectando queries del RAG.

```
[14:30:00] 🟡 DETECCIÓN
  Custom metrics: Weaviate query time > 5s (threshold: 500ms)
  ↓
[14:30:05] 🔍 CONTEXTO DOKPLOY
  Project: Saas Rag (aW_XGVs4XOe-qkNLqU_c8)
  Compose: Backend (B83szPTH3c6YER7-XcZ3_)

  Servicios:
  - saas-rag-fastapi (depende de weaviate)
  - saas-rag-postgres
  - saas-rag-redis
  - saas-rag-mongodb
  - saas-rag-weaviate ← Problema aquí

  Docker stats weaviate:
  - CPU: 95% (spike inusual)
  - Memory: 2.1GB/4GB
  - Disk I/O: Alto (writes continuas)
  ↓
[14:30:15] 📊 ANÁLISIS COMPOSE
  Agente analiza docker-compose.yml:

  services:
    saas-rag-weaviate:
      image: weaviate
      environment:
        PERSISTENCE_DATA_PATH: /var/lib/weaviate
      volumes:
        - weaviate_data:/var/lib/weaviate

  Agente check volumen:
  - Size: 18GB/20GB (90% usado)
  - Inodes: 95% usado

  Logs weaviate:
  "WARN: Compaction running, high disk usage detected"
  "INFO: Running background maintenance"
  ↓
[14:30:30] 🧠 DIAGNÓSTICO LLM
  "Weaviate está ejecutando compaction automática porque
   el disco está casi lleno. Este es un proceso intensivo
   que bloquea queries.

   Causa raíz: Volumen de datos creciendo sin cleanup.

   No es un problema crítico, es mantenimiento necesario.
   PERO podemos optimizarlo:

   1. Aumentar tamaño de volumen (20GB → 50GB)
   2. Configurar cleanup automático de vectores antiguos
   3. Dejar que compaction termine naturalmente

   Riesgo: BAJO (es mantenimiento normal)
   Urgencia: MEDIA (afecta performance pero no disponibilidad)"
  ↓
[14:30:45] 🤔 DECISIÓN
  Confianza: 75% (no 100% por ser cambio de volumen)

  Agente decide: Pedir aprobación para cambios,
  pero puede optimizar configuración ya.
  ↓
[14:31:00] 📱 NOTIFICACIÓN + ACCIÓN
  Telegram:
  "⚠️ Weaviate lento - Mantenimiento en curso

   Weaviate está ejecutando compaction automática.
   Esto es normal pero está causando lentitud.

   📊 Estado:
   • Volumen: 18GB/20GB (90% usado)
   • CPU: 95% (compaction)
   • Query time: 5s (normal: 500ms)

   💡 Puedo hacer:
   1. ✅ Optimizar config de compaction (YA HECHO)
   2. ⏳ Aumentar volumen 20GB→50GB (NECESITA APROBACIÓN)
   3. ⏳ Configurar cleanup automático (NECESITA APROBACIÓN)

   La compaction terminará en ~15min. ¿Proceder con #2 y #3?

   [✅ Sí] [❌ No] [⏸ Esperar]"

  Mientras tanto, agente ya optimizó:
  - Ajustó HNSW_EF para mejor performance durante compaction
  - Configuró batch_size menor para reducir memory spikes
  ↓
[14:35:00] 👤 USUARIO APRUEBA
  ↓
[14:35:10] 🔧 EJECUCIÓN
  1. Agente actualiza docker-compose.yml:
     volumes:
       weaviate_data:
         driver: local
         driver_opts:
           type: none
           device: /mnt/weaviate-large  # Nuevo volumen 50GB
           o: bind

  2. Agente crea script de migración:
     - Stop weaviate
     - Rsync data a nuevo volumen
     - Update compose
     - Redeploy

  3. Ejecuta vía Dokploy:
     POST /compose.update  # Actualizar compose
     POST /compose.redeploy  # Redeploy con nuevo volumen
  ↓
[14:42:00] ✅ COMPLETADO
  Telegram:
  "✅ Weaviate optimizado

   ✓ Compaction completada naturalmente
   ✓ Volumen migrado: 20GB → 50GB
   ✓ Config optimizada para auto-cleanup

   📊 Resultado:
   • Query time: 5s → 180ms ✓
   • CPU: 95% → 12%
   • Disk usage: 90% → 36%

   🎯 Próximos pasos automáticos:
   • Cleanup de vectores >90 días (semanal)
   • Alerta si disco >70%
   • Optimización de índices (mensual)"
```

### Caso 3: N8N - Workflow Bloqueado

**Escenario:**
N8N workflow stuck, no procesa nuevas ejecuciones.

```
[09:00:00] 🔴 DETECCIÓN
  Custom monitor: N8N queue depth = 45 (threshold: 10)
  Última ejecución completada: hace 2 horas
  ↓
[09:00:05] 🔍 ANÁLISIS DOKPLOY
  Project: Random_Test (5oFz33_YIUBsd8itqRgvu)
  Compose: n8n (NYEI7PjWArBVZcFMs2hU0)

  Servicio: n8n (isolated deployment)

  Docker stats:
  - Status: running
  - CPU: 0.1% (sospechosamente bajo)
  - Memory: 890MB/1GB
  - No errors en health check

  Logs N8N:
  "Workflow 'daily-backup' execution started"
  "Connecting to S3..."
  [Silence durante 2 horas]
  ↓
[09:00:20] 🧠 DIAGNÓSTICO
  Agente analiza:
  "N8N está stuck en una operación de S3.
   Probablemente timeout o deadlock en el workflow.

   Opciones:
   1. Restart container (pierde ejecución actual)
   2. Exec into container y kill proceso específico
   3. Esperar timeout (si está configurado)

   Dado que han pasado 2 horas y threshold es 30min,
   restart es la mejor opción."

  Confianza: 88%
  ↓
[09:00:30] 🔧 AUTO-FIX
  Acción: Restart container N8N

  vía Docker API (más rápido que redeploy):
  docker.containers.get("randomtest-n8n").restart()
  ↓
[09:00:45] ✅ VERIFICACIÓN
  - Container: ✓ running
  - N8N responsive: ✓
  - Queue processing: ✓ 45 → 0 en 2min

  Investigación post-mortem automática:
  - Check workflow 'daily-backup'
  - Encuentra: S3 endpoint cambió (configuración)
  ↓
[09:03:00] 📱 NOTIFICACIÓN
  Telegram:
  "✅ N8N desbloqueado

   El workflow 'daily-backup' estaba stuck
   esperando S3 que no respondía.

   🔧 Acción: Container restart
   📊 Resultado: 45 workflows procesados

   ⚠️ Problema encontrado:
   S3 endpoint en workflow está desactualizado.

   ¿Quieres que actualice el workflow automáticamente?
   Nuevo endpoint: https://s3.sphyrnasolutions.com

   [✅ Actualizar] [❌ Revisar manual]"
```

---

## 📅 Plan de Implementación Optimizado

### Fase 1: Core Dokploy (Semana 1-2)

#### Sprint 1.1: Dokploy Client (3 días)

```python
Entregables:
✓ DokployClient con 30+ métodos
✓ Tests de integración con API real
✓ Error handling robusto
✓ Async/await optimizado

Tareas:
1. Implementar cliente HTTP para Dokploy API
2. Métodos para compose (deploy, start, stop, etc.)
3. Métodos para projects, domains, deployments
4. Rate limiting y retry logic
5. Tests unitarios + integración
```

#### Sprint 1.2: Docker Integration (4 días)

```python
Entregables:
✓ Docker client wrapper
✓ Compose analyzer (parse docker-compose.yml)
✓ Container health checker
✓ Log aggregator
✓ Stats collector

Tareas:
1. Docker SDK integration
2. Parse de docker-compose.yml (dependencies)
3. Health check monitor
4. Log streaming desde containers
5. Metrics collection (CPU, RAM, Network)
```

### Fase 2: Agent Intelligence (Semana 3-4)

#### Sprint 2.1: LangGraph Agent (5 días)

```python
Entregables:
✓ DokployAgentState definido
✓ StateGraph con 8 nodos
✓ 3 runbooks básicos funcionando
✓ Claude integration

Tareas:
1. Definir DokployAgentState (TypedDict)
2. Crear StateGraph con flujo completo
3. Implementar nodos: detect, analyze, plan, execute, verify
4. Integrar Claude Sonnet
5. Runbooks: service_down, high_memory, deployment_failed
```

#### Sprint 2.2: Knowledge Base (5 días)

```python
Entregables:
✓ ChromaDB setup
✓ Incident memory (embeddings)
✓ 10 runbooks Dokploy
✓ Compose pattern recognition

Tareas:
1. Setup ChromaDB local
2. Embeddings de incidentes pasados
3. 10 runbooks completos (YAML)
4. Sistema de búsqueda semántica
5. Compose dependency analyzer
```

### Fase 3: Interfaces (Semana 5)

#### Sprint 3.1: Telegram Bot (4 días)

```python
Entregables:
✓ Bot 24/7 funcional
✓ 15 comandos
✓ Conversación natural
✓ Notificaciones rich

Comandos:
/status [project]       - Estado general o de proyecto
/services [compose]     - Listar servicios de compose
/logs <service> [n]     - Ver logs (últimas n líneas)
/restart <service>      - Reiniciar servicio
/deploy <compose>       - Deploy/redeploy
/rollback <compose>     - Rollback a deploy anterior
/health <compose>       - Health de todos los servicios
/metrics <service>      - CPU/RAM/Network
/incidents [n]          - Últimos n incidentes
/approve <incident>     - Aprobar acción propuesta
/help                   - Ayuda

Conversacional:
"¿Por qué está caído Granada?"
"Muéstrame los logs del API de RAG"
"Reinicia el Weaviate"
"¿Cuánto CPU usa el frontend?"
```

#### Sprint 3.2: Dashboard (3 días)

```python
Entregables:
✓ Next.js dashboard
✓ Vista de projects/composes
✓ Timeline de incidentes
✓ Métricas en tiempo real

Páginas:
- /              # Overview de todos los projects
- /projects/:id  # Detalle de project con composes
- /composes/:id  # Servicios del compose + métricas
- /incidents     # Timeline de incidentes
- /agent         # Estado del agente
```

### Fase 4: Testing & Deploy (Semana 6)

#### Sprint 4.1: Testing Completo (3 días)

```python
Entregables:
✓ Tests unitarios (80%+ coverage)
✓ Tests de integración
✓ Tests end-to-end

Tests críticos:
- Restart service → Verifica que sube
- Deploy compose → Verifica health checks
- Rollback → Verifica deployment anterior
- Agent flow completo (detect→fix→verify)
```

#### Sprint 4.2: Production Deploy (4 días)

```python
Entregables:
✓ Agente deployado en Dokploy (ironía!)
✓ CI/CD configurado
✓ Monitoring del agente mismo
✓ Documentación completa

Deploy:
El agente mismo será un compose en Dokploy:

services:
  infraguardian-agent:
    build: .
    environment:
      - DOKPLOY_API_KEY=${API_KEY}
      - CLAUDE_API_KEY=${CLAUDE_KEY}
      - TELEGRAM_BOT_TOKEN=${BOT_TOKEN}
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./knowledge:/app/knowledge

  infraguardian-db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

  infraguardian-redis:
    image: redis:7

  infraguardian-chromadb:
    image: chromadb/chroma:latest
    volumes:
      - chroma_data:/chroma/chroma
```

---

## 💰 Estimaciones Actualizadas

### Desarrollo

```
Fase 1: Dokploy Integration     2 semanas
Fase 2: Agent Intelligence       2 semanas
Fase 3: Interfaces               1 semana
Fase 4: Testing & Deploy         1 semana
────────────────────────────────────────
TOTAL                            6 semanas
```

### Costos Operacionales

```
LLM (GPT-OSS 20B):
  - Modelo: 100% local en RTX 5090
  - VRAM requerida: 16GB (Q4 cuantizado)
  - Costo API: $0/mes
  - Latencia: ~2-3s por respuesta
  - Sin límites de tokens
  Total: $0/mes

Infraestructura:
  - Servidor: $0 (ya existe, Dokploy)
  - GPU: $0 (ya existe, RTX 5090)
  - Docker resources:
    - CPU: 0.5 core
    - RAM: 2GB
    - Disk: 20GB (modelo + datos)
  - PostgreSQL: $0 (containerizado)
  - Redis: $0 (containerizado)
  - ChromaDB: $0 (local)

Telegram: $0 (gratuito)

──────────────────────────
TOTAL: $0/mes 🎉
```

### ROI

```
Ahorro de tiempo actual:
  - Incidentes/mes Dokploy: ~15
  - Tiempo promedio resolución: 45min
  - Total: 11.25 horas/mes

Con InfraGuardian:
  - Auto-resolución: 85% (12 incidentes)
  - Tiempo auto: 3min promedio
  - Manual asistido: 15% (3 incidentes)
  - Tiempo asistido: 20min

  Tiempo total: (12 × 3min) + (3 × 20min) = 96min

Ahorro: 11.25h - 1.6h = 9.65 horas/mes

Valor: 9.65h × $50/h = $482.50/mes
Costo: $0/mes (100% local)

ROI: INFINITO ∞ (sin costos recurrentes)
```

---

## 🚀 Próximos Pasos

### Comenzar HOY

```bash
# 1. Crear proyecto
mkdir infraguardian-dokploy
cd infraguardian-dokploy

# 2. Estructura
mkdir -p src/{agent,tools,integrations,interfaces,knowledge}
mkdir -p runbooks tests config

# 3. Setup Python
python3.11 -m venv venv
source venv/bin/activate

# 4. Instalar dependencias base
pip install \
  langchain==0.1.5 \
  langgraph==0.0.20 \
  langchain-anthropic==0.0.2 \
  docker==7.0.0 \
  python-telegram-bot==20.7 \
  chromadb==0.4.22 \
  fastapi==0.109.0

# 5. Instalar y configurar Ollama + GPT-OSS 20B
curl -fsSL https://ollama.com/install.sh | sh
ollama pull openai/gpt-oss-20b

# Test rápido del modelo
ollama run openai/gpt-oss-20b "Analiza este error de Docker: 'Exit code 137'. ¿Qué significa?"
# Debe responder sobre OOM (Out of Memory)

# 6. Configurar .env
cat > .env << EOF
DOKPLOY_API_URL=https://settings.sphyrnasolutions.com/api
DOKPLOY_API_KEY=claude_mcplpIwzCRCcOdvOmdtYcFNaBrzkdtJSoZIdtJvPhfmWhdBSRQNcijXVemATQXlRPHb
OLLAMA_MODEL=openai/gpt-oss-20b
OLLAMA_BASE_URL=http://localhost:11434
TELEGRAM_BOT_TOKEN=tu_bot_token
EOF

# 7. Primera prueba: Dokploy Client
cat > src/integrations/dokploy_client.py << 'EOF'
import aiohttp
import os

class DokployClient:
    def __init__(self):
        self.base_url = os.getenv("DOKPLOY_API_URL")
        self.api_key = os.getenv("DOKPLOY_API_KEY")

    async def get_all_projects(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/project.all",
                headers={"x-api-key": self.api_key}
            ) as response:
                return await response.json()

# Test
if __name__ == "__main__":
    import asyncio
    client = DokployClient()
    projects = asyncio.run(client.get_all_projects())
    print(f"Found {len(projects)} projects")
    for p in projects:
        print(f"  - {p['name']}")
EOF

# 8. Ejecutar test
python src/integrations/dokploy_client.py
```

### Primer Milestone (Semana 1)

**Objetivo:** Cliente Dokploy funcional + Docker integration

```python
# Al final de la semana 1 deberías tener:

# 1. Dokploy Client completo
client = DokployClient()
projects = await client.get_all_projects()
composes = await client.get_compose_services(compose_id)
await client.restart_compose(compose_id)

# 2. Docker integration
docker_client = DockerClient()
containers = docker_client.get_compose_containers("granada-shariff")
logs = docker_client.get_logs(container_id, tail=100)
stats = docker_client.get_stats(container_id)

# 3. Primer runbook funcionando
# runbooks/compose_service_down.yaml ejecutándose
```

---

## 📚 Recursos Específicos Dokploy

### Documentación

- **Dokploy API OpenAPI**: https://settings.sphyrnasolutions.com/swagger
- **Tu OpenAPI Document**: `/tmp/dokploy-openapi.json` (ya descargado)
- **Docker Compose Reference**: https://docs.docker.com/compose/
- **Docker Python SDK**: https://docker-py.readthedocs.io/

### Ejemplos de Compose

Puedes acceder a tus propios docker-compose.yml vía Dokploy API:

```python
# Ver compose de Granada
compose_info = await client.compose_one("56SmVbZnH2IMcA4fQHLUw")
compose_file = compose_info["composeFile"]

# Ahora el agente puede parsear y entender:
import yaml
compose_data = yaml.safe_load(compose_file)
services = compose_data["services"]
# Analizar dependencies, volumes, networks, etc.
```

---

## 🎯 Conclusión

**InfraGuardian AI - Dokploy Edition** está diseñado específicamente para tu stack:

✅ **100% Dokploy-native**: Usa exclusivamente Dokploy API
✅ **Compose-aware**: Entiende relaciones entre servicios
✅ **Docker-optimized**: Aprovecha Docker API para detalles
✅ **Simple deployment**: El agente mismo corre en Dokploy
✅ **100% Gratuito**: $0/mes (GPT-OSS 20B local en RTX 5090)
✅ **Privacidad total**: Todo corre en tu servidor, cero datos a terceros
✅ **Fast to build**: 6 semanas vs 8-10 de versión genérica

**Siguiente acción:**
Ejecuta los comandos de "Comenzar HOY" y tendrás el proyecto base funcionando en 30 minutos.

¿Empezamos? 🚀

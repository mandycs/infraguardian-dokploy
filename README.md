# InfraGuardian AI - Dokploy Edition

🤖 Agente autónomo para gestión de infraestructura Dokploy con Telegram Bot y GPT-OSS 20B.

[![GitHub](https://img.shields.io/badge/github-infraguardian--dokploy-blue?logo=github)](https://github.com/mandycs/infraguardian-dokploy)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Características

- 🤖 Bot de Telegram con comandos interactivos
- 📊 Monitoreo automático de servicios Dokploy
- 🧠 IA local con GPT-OSS 20B (100% privado, $0/mes)
- ⚡ Alertas en tiempo real
- 🔧 Gestión de Docker Compose vía API de Dokploy

## Requisitos

- Python 3.11+
- Ollama con GPT-OSS 20B instalado
- Cuenta de Telegram Bot Token
- Acceso a API de Dokploy

## Instalación

```bash
# 0. Clonar el repositorio
git clone https://github.com/mandycs/infraguardian-dokploy.git
cd infraguardian-dokploy

# 1. Crear virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales:
#   - DOKPLOY_API_URL: URL de tu instancia Dokploy
#   - DOKPLOY_API_KEY: API key de Dokploy
#   - TELEGRAM_BOT_TOKEN: Token de @BotFather
#   - OPENAI_API_BASE: http://localhost:11434/v1 (Ollama)
#   - OPENAI_MODEL_NAME: gpt-oss

# 4. Crear bot de Telegram
# Habla con @BotFather en Telegram:
# /newbot -> sigue las instrucciones -> copia el token

# 5. Ejecutar GPT-OSS en Ollama
ollama run gpt-oss

# 6. Ejecutar bot
python main.py
```

## Comandos del Bot

**💬 Conversación Directa con IA:**
El bot responde a cualquier mensaje de texto usando GPT-OSS 20B. No necesitas comandos especiales:
- "¿Cuántos composes tengo activos?"
- "¿Qué significa exit code 137?"
- "Explica la diferencia entre docker-compose restart y down/up"
- El bot tiene contexto de tu infraestructura actual

**📋 Comandos de Información:**
- `/start` - Mensaje de bienvenida
- `/help` - Ayuda detallada
- `/projects` - Lista todos los proyectos Dokploy
- `/composes` - Lista todos los composes
- `/status <compose_id>` - Estado detallado de un compose
- `/services <compose_id>` - Servicios de un compose

**🔧 Comandos de Gestión:**
- `/deploy <compose_id>` - Deploya/redeploya un compose
- `/start_compose <compose_id>` - Inicia un compose
- `/stop_compose <compose_id>` - Detiene un compose

## Estructura del Proyecto

```
infraguardian-dokploy/
├── src/
│   ├── integrations/
│   │   └── dokploy_client.py   # Cliente API Dokploy
│   ├── bot/
│   │   └── telegram_bot.py     # Bot de Telegram
│   ├── llm/
│   │   └── gpt_oss_client.py   # Cliente GPT-OSS
│   └── monitor/
│       └── service_monitor.py  # Sistema de monitoreo
├── docs/
│   └── PROYECTO_AGENTE_AUTONOMO_DOKPLOY.md
├── main.py                     # Punto de entrada
├── requirements.txt
├── .env.example
└── README.md
```

## Documentación

Ver [PROYECTO_AGENTE_AUTONOMO_DOKPLOY.md](docs/PROYECTO_AGENTE_AUTONOMO_DOKPLOY.md) para especificaciones completas.

## Licencia

MIT

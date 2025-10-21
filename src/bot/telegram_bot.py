#!/usr/bin/env python3
"""
Telegram Bot para InfraGuardian AI
Bot para monitoreo y gestión de infraestructura Dokploy
"""
import os
import logging
from typing import Optional
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from ..integrations.dokploy_client import DokployClient
from ..llm.gpt_oss_client import GPTOSSClient

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class InfraGuardianBot:
    """Bot de Telegram para gestión de Dokploy"""

    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token or self.token == "YOUR_BOT_TOKEN_HERE":
            raise ValueError("TELEGRAM_BOT_TOKEN no configurado en .env")

        self.dokploy = DokployClient()
        self.gpt_oss = GPTOSSClient()
        self.app = Application.builder().token(self.token).build()
        self._register_handlers()

    def _register_handlers(self):
        """Registra todos los command handlers"""
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(CommandHandler("projects", self.projects))
        self.app.add_handler(CommandHandler("composes", self.composes))
        self.app.add_handler(CommandHandler("status", self.status))
        self.app.add_handler(CommandHandler("services", self.services))
        self.app.add_handler(CommandHandler("deploy", self.deploy))
        self.app.add_handler(CommandHandler("start_compose", self.start_compose))
        self.app.add_handler(CommandHandler("stop_compose", self.stop_compose))

        # Handler para mensajes no-comando (conversación con GPT-OSS)
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start - Mensaje de bienvenida"""
        welcome_msg = """
🤖 *InfraGuardian AI* - Tu asistente de infraestructura

💬 *¡Conversación directa habilitada!*
Escríbeme cualquier pregunta sobre Docker, Dokploy o tu infraestructura.
No necesitas usar comandos especiales, solo pregunta naturalmente.

📋 *Comandos de Información:*
/projects - Lista todos los proyectos
/composes - Lista todos los composes
/status <compose_id> - Estado de un compose
/services <compose_id> - Servicios de un compose

🔧 *Comandos de Gestión:*
/deploy <compose_id> - Deploya un compose
/start_compose <compose_id> - Inicia un compose
/stop_compose <compose_id> - Detiene un compose

❓ /help - Ayuda detallada

*Ejemplos de preguntas:*
• "¿Cuántos composes tengo activos?"
• "¿Qué significa exit code 137?"
• "¿Cómo puedo ver los logs de un contenedor?"
        """
        await update.message.reply_text(
            welcome_msg,
            parse_mode='Markdown'
        )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help - Ayuda detallada"""
        help_msg = """
📖 *Ayuda de InfraGuardian AI*

*Comandos de Información:*

• `/projects`
  Lista todos los proyectos en Dokploy

• `/composes`
  Lista todos los composes de todos los proyectos

• `/status <compose_id>`
  Muestra el estado detallado de un compose específico
  Ejemplo: `/status abc123`

• `/services <compose_id>`
  Lista los servicios dentro de un compose
  Ejemplo: `/services abc123`

*Comandos de Gestión:*

• `/deploy <compose_id>`
  Deploya/redeploya un compose
  Ejemplo: `/deploy abc123`

• `/start_compose <compose_id>`
  Inicia todos los servicios de un compose
  Ejemplo: `/start_compose abc123`

• `/stop_compose <compose_id>`
  Detiene todos los servicios de un compose
  Ejemplo: `/stop_compose abc123`

💡 Tip: Usa `/composes` para obtener los IDs de tus composes
        """
        await update.message.reply_text(
            help_msg,
            parse_mode='Markdown'
        )

    async def projects(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /projects - Lista todos los proyectos"""
        try:
            await update.message.reply_text("🔍 Obteniendo proyectos...")

            projects = await self.dokploy.get_all_projects()

            if not projects:
                await update.message.reply_text("No se encontraron proyectos.")
                return

            msg = f"📋 *Proyectos Dokploy* ({len(projects)}):\n\n"

            for project in projects:
                name = project.get("name", "Sin nombre")
                project_id = project.get("projectId", "N/A")
                description = project.get("description", "")

                msg += f"• *{name}*\n"
                msg += f"  ID: `{project_id}`\n"
                if description:
                    msg += f"  {description}\n"
                msg += "\n"

            await update.message.reply_text(msg, parse_mode='Markdown')

        except Exception as e:
            logger.error(f"Error en /projects: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")

    async def composes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /composes - Lista todos los composes"""
        try:
            await update.message.reply_text("🔍 Obteniendo composes...")

            composes = await self.dokploy.get_all_composes()

            if not composes:
                await update.message.reply_text("No se encontraron composes.")
                return

            msg = f"📦 *Composes Dokploy* ({len(composes)}):\n\n"

            for compose in composes:
                name = compose.get("name", "Sin nombre")
                compose_id = compose.get("composeId", "N/A")
                project_name = compose.get("project_name", "Unknown")
                status = compose.get("composeStatus", "unknown")

                msg += f"• *{name}*\n"
                msg += f"  ID: `{compose_id}`\n"
                msg += f"  Proyecto: {project_name}\n"
                msg += f"  Estado: {status}\n\n"

            await update.message.reply_text(msg, parse_mode='Markdown')

        except Exception as e:
            logger.error(f"Error en /composes: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status <compose_id> - Estado de un compose"""
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /status <compose_id>\n"
                "Obtén el ID con /composes"
            )
            return

        compose_id = context.args[0]

        try:
            await update.message.reply_text(f"🔍 Obteniendo estado de {compose_id}...")

            health = await self.dokploy.get_compose_health(compose_id)

            msg = f"🏥 *Estado del Compose*\n\n"
            msg += f"Nombre: *{health['name']}*\n"
            msg += f"ID: `{health['compose_id']}`\n"
            msg += f"Estado: {health['status']}\n"
            msg += f"Servicios: {health['services_count']}\n\n"

            if health['services']:
                msg += "*Servicios:*\n"
                for service in health['services']:
                    service_name = service.get('name', 'Unknown')
                    msg += f"  • {service_name}\n"

            await update.message.reply_text(msg, parse_mode='Markdown')

        except Exception as e:
            logger.error(f"Error en /status: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")

    async def services(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /services <compose_id> - Lista servicios de un compose"""
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /services <compose_id>\n"
                "Obtén el ID con /composes"
            )
            return

        compose_id = context.args[0]

        try:
            await update.message.reply_text(f"🔍 Obteniendo servicios...")

            services = await self.dokploy.get_compose_services(compose_id)

            if not services:
                await update.message.reply_text("No se encontraron servicios.")
                return

            msg = f"🔧 *Servicios* ({len(services)}):\n\n"

            for service in services:
                service_name = service.get('name', 'Unknown')
                msg += f"• {service_name}\n"

            await update.message.reply_text(msg, parse_mode='Markdown')

        except Exception as e:
            logger.error(f"Error en /services: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")

    async def deploy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /deploy <compose_id> - Deploya un compose"""
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /deploy <compose_id>\n"
                "Obtén el ID con /composes"
            )
            return

        compose_id = context.args[0]

        try:
            await update.message.reply_text(f"🚀 Iniciando deploy de {compose_id}...")

            result = await self.dokploy.deploy_compose(compose_id)

            await update.message.reply_text(
                f"✅ Deploy iniciado correctamente\n"
                f"ID: `{compose_id}`"
            )

        except Exception as e:
            logger.error(f"Error en /deploy: {e}")
            await update.message.reply_text(f"❌ Error al deployar: {str(e)}")

    async def start_compose(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start_compose <compose_id> - Inicia un compose"""
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /start_compose <compose_id>\n"
                "Obtén el ID con /composes"
            )
            return

        compose_id = context.args[0]

        try:
            await update.message.reply_text(f"▶️ Iniciando compose {compose_id}...")

            result = await self.dokploy.start_compose(compose_id)

            await update.message.reply_text(
                f"✅ Compose iniciado correctamente\n"
                f"ID: `{compose_id}`"
            )

        except Exception as e:
            logger.error(f"Error en /start_compose: {e}")
            await update.message.reply_text(f"❌ Error al iniciar: {str(e)}")

    async def stop_compose(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /stop_compose <compose_id> - Detiene un compose"""
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /stop_compose <compose_id>\n"
                "Obtén el ID con /composes"
            )
            return

        compose_id = context.args[0]

        try:
            await update.message.reply_text(f"⏸️ Deteniendo compose {compose_id}...")

            result = await self.dokploy.stop_compose(compose_id)

            await update.message.reply_text(
                f"✅ Compose detenido correctamente\n"
                f"ID: `{compose_id}`"
            )

        except Exception as e:
            logger.error(f"Error en /stop_compose: {e}")
            await update.message.reply_text(f"❌ Error al detener: {str(e)}")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja mensajes no-comando usando GPT-OSS"""
        try:
            user_message = update.message.text
            logger.info(f"💬 Mensaje recibido: {user_message}")

            # Indicador de "escribiendo..."
            await update.message.chat.send_action(action="typing")

            # Obtener contexto de Dokploy
            try:
                composes = await self.dokploy.get_all_composes()

                # Preparar estadísticas
                status_counts = {}
                for compose in composes:
                    status = compose.get("composeStatus", "unknown")
                    status_counts[status] = status_counts.get(status, 0) + 1

                context_data = {
                    "composes": composes,
                    "stats": {
                        "total_composes": len(composes),
                        "status_distribution": status_counts
                    }
                }
            except Exception as e:
                logger.warning(f"No se pudo obtener contexto de Dokploy: {e}")
                context_data = None

            # Consultar a GPT-OSS
            response = await self.gpt_oss.ask(user_message, context=context_data)

            # Enviar respuesta
            await update.message.reply_text(response)

        except Exception as e:
            logger.error(f"Error en handle_message: {e}")
            await update.message.reply_text(
                f"❌ Error al procesar tu mensaje: {str(e)}\n\n"
                "Asegúrate de que GPT-OSS esté corriendo en Ollama:\n"
                "`ollama run gpt-oss`"
            )

    def run(self):
        """Inicia el bot"""
        logger.info("🤖 Iniciando InfraGuardian Bot...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


# Punto de entrada
if __name__ == "__main__":
    try:
        bot = InfraGuardianBot()
        bot.run()
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")

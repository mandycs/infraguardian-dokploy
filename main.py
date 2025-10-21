#!/usr/bin/env python3
"""
InfraGuardian AI - Main Entry Point
Bot autónomo para monitoreo y gestión de infraestructura Dokploy
"""
import sys
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Punto de entrada principal"""
    try:
        from src.bot import InfraGuardianBot

        logger.info("🚀 Iniciando InfraGuardian AI...")

        bot = InfraGuardianBot()
        bot.run()

    except KeyboardInterrupt:
        logger.info("\n👋 Bot detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

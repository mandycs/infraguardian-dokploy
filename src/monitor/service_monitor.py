#!/usr/bin/env python3
"""
Sistema de monitoreo de servicios Dokploy
Monitorea el estado de los composes y detecta anomalías
"""
import asyncio
import logging
from typing import Dict, List, Optional, Set
from datetime import datetime
from ..integrations.dokploy_client import DokployClient

logger = logging.getLogger(__name__)


class ServiceMonitor:
    """Monitor de servicios Dokploy con detección de cambios"""

    def __init__(
        self,
        dokploy_client: DokployClient,
        check_interval: int = 60,
        on_status_change=None
    ):
        """
        Args:
            dokploy_client: Cliente de Dokploy
            check_interval: Intervalo de chequeo en segundos (default: 60)
            on_status_change: Callback async cuando cambia el estado de un compose
        """
        self.client = dokploy_client
        self.check_interval = check_interval
        self.on_status_change = on_status_change

        # Estado anterior de los composes
        self.previous_states: Dict[str, str] = {}

        # Control de monitoreo
        self.is_running = False
        self._monitor_task: Optional[asyncio.Task] = None

    async def check_all_composes(self) -> List[Dict]:
        """
        Verifica el estado de todos los composes
        Returns:
            Lista de composes con su estado actual
        """
        try:
            composes = await self.client.get_all_composes()

            results = []
            for compose in composes:
                compose_id = compose.get("composeId")
                name = compose.get("name", "Unknown")
                current_status = compose.get("composeStatus", "unknown")

                # Detectar cambio de estado
                previous_status = self.previous_states.get(compose_id)
                status_changed = previous_status and previous_status != current_status

                result = {
                    "compose_id": compose_id,
                    "name": name,
                    "status": current_status,
                    "previous_status": previous_status,
                    "status_changed": status_changed,
                    "project_name": compose.get("project_name", "Unknown"),
                    "checked_at": datetime.now().isoformat()
                }

                # Notificar cambio de estado
                if status_changed and self.on_status_change:
                    try:
                        await self.on_status_change(result)
                    except Exception as e:
                        logger.error(f"Error en callback on_status_change: {e}")

                # Actualizar estado previo
                self.previous_states[compose_id] = current_status

                results.append(result)

            return results

        except Exception as e:
            logger.error(f"Error al verificar composes: {e}")
            return []

    async def check_compose_health(self, compose_id: str) -> Dict:
        """
        Verifica el health de un compose específico

        Args:
            compose_id: ID del compose a verificar

        Returns:
            Información de health del compose
        """
        try:
            health = await self.client.get_compose_health(compose_id)

            # Análisis básico de health
            services_count = health.get("services_count", 0)
            status = health.get("status", "unknown")

            health["healthy"] = status == "done" and services_count > 0
            health["checked_at"] = datetime.now().isoformat()

            return health

        except Exception as e:
            logger.error(f"Error al verificar health de {compose_id}: {e}")
            return {
                "compose_id": compose_id,
                "healthy": False,
                "error": str(e),
                "checked_at": datetime.now().isoformat()
            }

    async def get_unhealthy_composes(self) -> List[Dict]:
        """
        Obtiene lista de composes con problemas

        Returns:
            Lista de composes que no están en estado 'done'
        """
        composes = await self.check_all_composes()

        unhealthy = [
            c for c in composes
            if c.get("status") not in ["done", "running", "idle"]
        ]

        return unhealthy

    async def _monitor_loop(self):
        """Loop principal de monitoreo"""
        logger.info(f"🔍 Monitor iniciado (intervalo: {self.check_interval}s)")

        while self.is_running:
            try:
                # Verificar todos los composes
                results = await self.check_all_composes()

                # Log de resumen
                total = len(results)
                changed = sum(1 for r in results if r.get("status_changed"))

                if changed > 0:
                    logger.info(f"✅ Chequeo completado: {total} composes, {changed} cambios detectados")
                else:
                    logger.debug(f"✅ Chequeo completado: {total} composes, sin cambios")

                # Esperar antes del próximo chequeo
                await asyncio.sleep(self.check_interval)

            except asyncio.CancelledError:
                logger.info("⏹️ Monitor detenido")
                break
            except Exception as e:
                logger.error(f"❌ Error en monitor loop: {e}")
                await asyncio.sleep(self.check_interval)

    async def start(self):
        """Inicia el monitoreo en background"""
        if self.is_running:
            logger.warning("Monitor ya está corriendo")
            return

        self.is_running = True
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info("🚀 Monitor de servicios iniciado")

    async def stop(self):
        """Detiene el monitoreo"""
        if not self.is_running:
            return

        self.is_running = False

        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass

        logger.info("⏹️ Monitor de servicios detenido")

    async def get_monitoring_stats(self) -> Dict:
        """
        Obtiene estadísticas del monitoreo

        Returns:
            Estadísticas de monitoreo
        """
        composes = await self.client.get_all_composes()

        status_counts = {}
        for compose in composes:
            status = compose.get("composeStatus", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            "total_composes": len(composes),
            "monitoring_active": self.is_running,
            "check_interval": self.check_interval,
            "status_distribution": status_counts,
            "tracked_composes": len(self.previous_states)
        }


# Test del monitor
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    async def on_change(result: Dict):
        """Callback de ejemplo cuando cambia el estado"""
        print(f"\n🔔 CAMBIO DETECTADO:")
        print(f"  Compose: {result['name']}")
        print(f"  Estado: {result['previous_status']} → {result['status']}")

    async def test():
        print("🧪 Test del Service Monitor\n")

        client = DokployClient()
        monitor = ServiceMonitor(
            dokploy_client=client,
            check_interval=10,  # 10 segundos para el test
            on_status_change=on_change
        )

        # Test 1: Chequeo manual
        print("📊 Test 1: Chequeo manual de composes")
        results = await monitor.check_all_composes()
        for r in results:
            print(f"  • {r['name']}: {r['status']}")

        # Test 2: Estadísticas
        print(f"\n📈 Test 2: Estadísticas")
        stats = await monitor.get_monitoring_stats()
        print(f"  Total composes: {stats['total_composes']}")
        print(f"  Distribución de estados: {stats['status_distribution']}")

        # Test 3: Composes con problemas
        print(f"\n⚠️  Test 3: Composes con problemas")
        unhealthy = await monitor.get_unhealthy_composes()
        if unhealthy:
            for c in unhealthy:
                print(f"  • {c['name']}: {c['status']}")
        else:
            print("  ✅ Todos los composes están saludables")

        print("\n✅ Tests completados!")

    asyncio.run(test())

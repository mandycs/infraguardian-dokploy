#!/usr/bin/env python3
"""
Test del Service Monitor
"""
import asyncio
from dotenv import load_dotenv
from src.integrations.dokploy_client import DokployClient
from src.monitor.service_monitor import ServiceMonitor

load_dotenv()

async def on_change(result: dict):
    """Callback cuando cambia el estado de un compose"""
    print(f"\n🔔 CAMBIO DETECTADO:")
    print(f"  Compose: {result['name']}")
    print(f"  Estado: {result['previous_status']} → {result['status']}")

async def main():
    print("🧪 Test del Service Monitor\n")
    print("=" * 60)

    client = DokployClient()
    monitor = ServiceMonitor(
        dokploy_client=client,
        check_interval=10,
        on_status_change=on_change
    )

    # Test 1: Chequeo manual
    print("\n📊 Test 1: Chequeo manual de composes")
    print("-" * 60)
    results = await monitor.check_all_composes()
    print(f"Total composes: {len(results)}\n")
    for r in results[:5]:  # Mostrar primeros 5
        print(f"  • {r['name']}: {r['status']}")
    if len(results) > 5:
        print(f"  ... y {len(results) - 5} más")

    # Test 2: Estadísticas
    print(f"\n📈 Test 2: Estadísticas")
    print("-" * 60)
    stats = await monitor.get_monitoring_stats()
    print(f"  Total composes: {stats['total_composes']}")
    print(f"  Monitor activo: {stats['monitoring_active']}")
    print(f"  Intervalo: {stats['check_interval']}s")
    print(f"  Distribución de estados:")
    for status, count in stats['status_distribution'].items():
        print(f"    - {status}: {count}")

    # Test 3: Composes con problemas
    print(f"\n⚠️  Test 3: Composes con problemas")
    print("-" * 60)
    unhealthy = await monitor.get_unhealthy_composes()
    if unhealthy:
        for c in unhealthy:
            print(f"  • {c['name']}: {c['status']}")
    else:
        print("  ✅ Todos los composes están saludables")

    # Test 4: Health de un compose específico
    if results:
        print(f"\n🏥 Test 4: Health de un compose específico")
        print("-" * 60)
        first_compose_id = results[0]['compose_id']
        first_compose_name = results[0]['name']
        print(f"  Analizando: {first_compose_name}")
        health = await monitor.check_compose_health(first_compose_id)
        print(f"    Estado: {health.get('status')}")
        print(f"    Servicios: {health.get('services_count')}")
        print(f"    Saludable: {health.get('healthy')}")

    print("\n" + "=" * 60)
    print("✅ Tests completados!")

if __name__ == "__main__":
    asyncio.run(main())

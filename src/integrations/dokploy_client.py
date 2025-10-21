"""
Cliente para interactuar con la API de Dokploy
"""
import aiohttp
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class DokployClient:
    """Cliente asíncrono para la API de Dokploy"""

    def __init__(self):
        self.base_url = os.getenv("DOKPLOY_API_URL", "https://settings.sphyrnasolutions.com/api")
        self.api_key = os.getenv("DOKPLOY_API_KEY")

        if not self.api_key:
            raise ValueError("DOKPLOY_API_KEY no configurada en .env")

        # Dokploy usa x-api-key header (no Bearer)
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Realiza una petición HTTP a la API de Dokploy"""
        url = f"{self.base_url}{endpoint}"

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                url,
                headers=self.headers,
                **kwargs
            ) as response:
                response.raise_for_status()
                return await response.json()

    # ========== PROJECT ENDPOINTS ==========

    async def get_all_projects(self) -> List[Dict]:
        """Obtiene todos los proyectos de Dokploy"""
        return await self._request("GET", "/project.all")

    async def get_project(self, project_id: str) -> Dict:
        """Obtiene información de un proyecto específico"""
        return await self._request("GET", "/project.one", params={"projectId": project_id})

    # ========== COMPOSE ENDPOINTS ==========

    async def get_compose(self, compose_id: str) -> Dict:
        """Obtiene información de un compose"""
        return await self._request("GET", "/compose.one", params={"composeId": compose_id})

    async def get_compose_services(self, compose_id: str) -> List[Dict]:
        """Obtiene los servicios de un compose"""
        return await self._request("GET", "/compose.loadServices", params={"composeId": compose_id})

    async def start_compose(self, compose_id: str) -> Dict:
        """Inicia todos los servicios de un compose"""
        return await self._request("POST", "/compose.start", json={"composeId": compose_id})

    async def stop_compose(self, compose_id: str) -> Dict:
        """Detiene todos los servicios de un compose"""
        return await self._request("POST", "/compose.stop", json={"composeId": compose_id})

    async def deploy_compose(self, compose_id: str) -> Dict:
        """Deploya/redeploya un compose"""
        return await self._request("POST", "/compose.deploy", json={"composeId": compose_id})

    # ========== DEPLOYMENT ENDPOINTS ==========

    async def get_deployments(self) -> List[Dict]:
        """Obtiene todos los deployments"""
        return await self._request("GET", "/deployment.all")

    async def get_compose_deployments(self, compose_id: str) -> List[Dict]:
        """Obtiene el historial de deployments de un compose"""
        return await self._request("GET", "/deployment.allByCompose", params={"composeId": compose_id})

    # ========== DOMAIN ENDPOINTS ==========

    async def get_domains_by_compose(self, compose_id: str) -> List[Dict]:
        """Obtiene los dominios configurados para un compose"""
        return await self._request("GET", "/domain.byComposeId", params={"composeId": compose_id})

    # ========== HELPER METHODS ==========

    async def get_all_composes(self) -> List[Dict]:
        """Obtiene todos los composes de todos los proyectos"""
        projects = await self.get_all_projects()
        composes = []

        for project in projects:
            project_name = project.get("name", "Unknown")
            project_id = project.get("projectId")

            # Los composes están dentro de environments -> compose
            for environment in project.get("environments", []):
                env_name = environment.get("name", "Unknown")

                for compose in environment.get("compose", []):
                    # Agregar info del proyecto y environment
                    compose["project_name"] = project_name
                    compose["project_id"] = project_id
                    compose["environment_name"] = env_name
                    compose["environment_id"] = environment.get("environmentId")
                    composes.append(compose)

        return composes

    async def get_compose_health(self, compose_id: str) -> Dict:
        """
        Analiza el health de un compose
        Retorna información sobre el estado de los servicios
        """
        compose_info = await self.get_compose(compose_id)
        services = await self.get_compose_services(compose_id)

        return {
            "compose_id": compose_id,
            "name": compose_info.get("name", "Unknown"),
            "status": compose_info.get("composeStatus", "unknown"),
            "services_count": len(services),
            "services": services
        }


# Test del cliente
if __name__ == "__main__":
    import asyncio

    async def test():
        client = DokployClient()

        print("🔍 Probando cliente Dokploy...\n")

        # Test 1: Obtener proyectos
        print("📋 Proyectos:")
        projects = await client.get_all_projects()
        for project in projects:
            print(f"  - {project.get('name')} (ID: {project.get('projectId')})")

        print(f"\nTotal: {len(projects)} proyectos\n")

        # Test 2: Obtener composes
        print("📦 Composes:")
        composes = await client.get_all_composes()
        for compose in composes:
            print(f"  - {compose.get('name')} ({compose.get('project_name')})")

        print(f"\nTotal: {len(composes)} composes\n")

        # Test 3: Health de primer compose
        if composes:
            first_compose = composes[0]
            compose_id = first_compose.get("composeId")
            print(f"🏥 Health del compose '{first_compose.get('name')}':")
            health = await client.get_compose_health(compose_id)
            print(f"  Status: {health['status']}")
            print(f"  Servicios: {health['services_count']}")

        print("\n✅ Cliente Dokploy funcionando correctamente!")

    asyncio.run(test())

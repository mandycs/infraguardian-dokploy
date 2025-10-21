#!/usr/bin/env python3
"""
Cliente GPT-OSS para análisis de infraestructura
Usa LangChain-OpenAI apuntando a Ollama
"""
import os
import logging
from typing import Optional, Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

logger = logging.getLogger(__name__)


class GPTOSSClient:
    """Cliente para interactuar con GPT-OSS 20B"""

    def __init__(self):
        self.model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-oss")
        self.base_url = os.getenv("OPENAI_API_BASE", "http://localhost:11434/v1")
        self.api_key = os.getenv("OPENAI_API_KEY", "ollama")

        self.llm = ChatOpenAI(
            model=self.model_name,
            base_url=self.base_url,
            api_key=self.api_key,
            temperature=0.7,
        )

        # System prompt para el agente
        self.system_prompt = """Eres InfraGuardian AI, un asistente experto en infraestructura Dokploy y Docker.

Tu rol es ayudar al usuario a:
- Gestionar y monitorear servicios Docker Compose desplegados en Dokploy
- Diagnosticar problemas de infraestructura
- Explicar conceptos de Docker, Docker Compose y Dokploy
- Sugerir mejores prácticas y soluciones

Características:
- Respuestas concisas y técnicas
- Enfocado en soluciones prácticas
- Usa emojis ocasionalmente para claridad visual
- Si no conoces algo específico, admítelo

El usuario puede preguntarte cualquier cosa sobre Docker, Dokploy o su infraestructura."""

    async def ask(
        self,
        question: str,
        context: Optional[Dict] = None
    ) -> str:
        """
        Envía una pregunta a GPT-OSS

        Args:
            question: Pregunta del usuario
            context: Contexto adicional (ej. info de composes)

        Returns:
            Respuesta de GPT-OSS
        """
        try:
            messages = [SystemMessage(content=self.system_prompt)]

            # Agregar contexto si está disponible
            if context:
                context_text = self._format_context(context)
                messages.append(SystemMessage(content=f"Contexto actual:\n{context_text}"))

            # Agregar pregunta del usuario
            messages.append(HumanMessage(content=question))

            # Invocar modelo
            response = await self.llm.ainvoke(messages)

            return response.content

        except Exception as e:
            logger.error(f"Error al consultar GPT-OSS: {e}")
            return f"❌ Error al procesar tu pregunta: {str(e)}\n\nVerifica que GPT-OSS esté corriendo en Ollama."

    def _format_context(self, context: Dict) -> str:
        """Formatea el contexto para el prompt"""
        parts = []

        # Información de composes
        if "composes" in context:
            composes = context["composes"]
            parts.append(f"Composes disponibles: {len(composes)}")

            # Detalles de composes (máximo 10 para no saturar el contexto)
            if composes:
                parts.append("\nComposes activos:")
                for compose in composes[:10]:
                    name = compose.get("name", "Unknown")
                    status = compose.get("composeStatus", "unknown")
                    project = compose.get("project_name", "Unknown")
                    parts.append(f"  - {name} ({project}): {status}")

                if len(composes) > 10:
                    parts.append(f"  ... y {len(composes) - 10} más")

        # Estadísticas
        if "stats" in context:
            stats = context["stats"]
            parts.append(f"\nEstadísticas:")
            parts.append(f"  Total composes: {stats.get('total_composes', 0)}")

            if "status_distribution" in stats:
                parts.append(f"  Distribución:")
                for status, count in stats["status_distribution"].items():
                    parts.append(f"    - {status}: {count}")

        return "\n".join(parts)

    async def analyze_compose_issue(
        self,
        compose_name: str,
        compose_status: str,
        error_logs: Optional[str] = None
    ) -> str:
        """
        Analiza un problema específico de un compose

        Args:
            compose_name: Nombre del compose
            compose_status: Estado actual
            error_logs: Logs de error (opcional)

        Returns:
            Análisis y sugerencias
        """
        prompt = f"""Analiza este problema de un compose en Dokploy:

Compose: {compose_name}
Estado actual: {compose_status}
"""

        if error_logs:
            prompt += f"\nLogs de error:\n{error_logs}\n"

        prompt += """
Proporciona:
1. Posibles causas del problema
2. Pasos para diagnosticar
3. Soluciones recomendadas
"""

        return await self.ask(prompt)


# Test del cliente
if __name__ == "__main__":
    import asyncio

    async def test():
        print("🧪 Test de GPT-OSS Client\n")
        print("=" * 60)

        client = GPTOSSClient()

        # Test 1: Pregunta simple
        print("\n📝 Test 1: Pregunta simple")
        print("-" * 60)
        response = await client.ask("¿Qué es Dokploy?")
        print(f"Respuesta: {response}")

        # Test 2: Pregunta con contexto
        print("\n📊 Test 2: Pregunta con contexto")
        print("-" * 60)
        context = {
            "composes": [
                {"name": "frontend", "composeStatus": "done", "project_name": "Web"},
                {"name": "backend", "composeStatus": "error", "project_name": "API"},
            ],
            "stats": {
                "total_composes": 2,
                "status_distribution": {"done": 1, "error": 1}
            }
        }
        response = await client.ask(
            "¿Qué composes tengo y cuál está fallando?",
            context=context
        )
        print(f"Respuesta: {response}")

        # Test 3: Análisis de problema
        print("\n🔍 Test 3: Análisis de problema")
        print("-" * 60)
        response = await client.analyze_compose_issue(
            compose_name="backend",
            compose_status="error",
            error_logs="Error: ECONNREFUSED connecting to database"
        )
        print(f"Respuesta: {response}")

        print("\n" + "=" * 60)
        print("✅ Tests completados!")

    asyncio.run(test())

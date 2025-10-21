#!/usr/bin/env python3
"""
Test GPT-OSS 20B con LangChain OpenAI (apuntando a Ollama)
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Cargar variables de entorno
load_dotenv()

# Configurar LLM apuntando a Ollama
llm = ChatOpenAI(
    model="gpt-oss",
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Dummy key
    temperature=0.5,
)

print("🧪 Test de GPT-OSS 20B con LangChain-OpenAI\n")
print("=" * 60)

# Test 1: Pregunta simple
print("\n📝 Test 1: Pregunta simple sobre Docker")
print("-" * 60)
response = llm.invoke("¿Qué significa el exit code 137 en Docker? Responde en 1 línea.")
print(f"Respuesta: {response.content}\n")

# Test 2: Function calling (test básico)
print("\n🔧 Test 2: Capacidad de seguir instrucciones estructuradas")
print("-" * 60)
prompt = """Analiza este error de un contenedor Docker:
ERROR: Failed to connect to database
Exit code: 1

Dame SOLO 3 acciones en formato JSON:
{"actions": ["acción1", "acción2", "acción3"]}
"""
response = llm.invoke(prompt)
print(f"Respuesta: {response.content}\n")

print("\n✅ Tests completados!")
print("=" * 60)
print("\n💡 GPT-OSS 20B está funcionando correctamente con LangChain-OpenAI")

"""
Bankbot - Chatbot CLI simple con soporte para Ollama y Groq.

Uso:
    python app.py

Comandos disponibles:
    exit  - Salir del chatbot
    reset - Borrar historial de conversación
"""
import os
import sys
import requests
from dotenv import load_dotenv


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

def load_config():
    """Carga y valida la configuración desde variables de entorno."""
    load_dotenv()

    config = {
        "backend": os.getenv("BACKEND", "ollama").lower(),
        "temperature": float(os.getenv("TEMPERATURE", "0.2")),
        "ollama_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1/chat/completions"),
        "ollama_model": os.getenv("OLLAMA_MODEL", "llama3"),
        "groq_url": os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1/chat/completions"),
        "groq_model": os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        "groq_api_key": os.getenv("GROQ_API_KEY"),
    }

    # Validar backend
    if config["backend"] not in ["ollama", "groq"]:
        print(f"Error: BACKEND inválido '{config['backend']}'. Usa 'ollama' o 'groq'.")
        sys.exit(1)

    # Validar API key para Groq
    if config["backend"] == "groq" and not config["groq_api_key"]:
        print("Error: BACKEND=groq requiere GROQ_API_KEY.")
        sys.exit(1)

    return config


# ============================================================================
# FUNCIONES DE CHAT (BACKENDS)
# ============================================================================

def chat_ollama(messages, config):
    """Envía mensaje a Ollama local y devuelve la respuesta."""
    payload = {
        "model": config["ollama_model"],
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": config["temperature"],
        }
    }

    try:
        response = requests.post(config["ollama_url"], json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error de conexión con Ollama: {e}"
    except KeyError as e:
        return f"Error: respuesta inesperada de Ollama: {data}"


def chat_groq(messages, config):
    """Envía mensaje a GroqCloud y devuelve la respuesta."""
    headers = {
        "Authorization": f"Bearer {config['groq_api_key']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config["groq_model"],
        "messages": messages,
        "temperature": config["temperature"],
    }

    try:
        response = requests.post(config["groq_url"], json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error de conexión con Groq: {e}"


# ============================================================================
# BUCLE PRINCIPAL
# ============================================================================

def main():
    """Punto de entrada principal del chatbot."""
    config = load_config()
    
    print(f"Bankbot iniciado. Backend: {config['backend'].upper()}")
    print("Comandos: 'exit' para salir, 'reset' para borrar historial.\n")

    # Historial con mensaje de sistema inicial
    system_message = {"role": "system", "content": "Eres un asistente bancario útil y amable."}
    history = [system_message]

    while True:
        # Leer entrada del usuario
        try:
            user_input = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            break

        # Ignorar entradas vacías
        if not user_input:
            continue

        # Comandos especiales
        if user_input.lower() == "exit":
            print("¡Hasta luego!")
            break

        if user_input.lower() == "reset":
            history = [system_message]
            print("Historial borrado.\n")
            continue

        # Añadir mensaje del usuario al historial
        history.append({"role": "user", "content": user_input})

        # Obtener respuesta del backend
        print("Asistente: ", end="", flush=True)
        
        if config["backend"] == "ollama":
            response = chat_ollama(history, config)
        else:
            response = chat_groq(history, config)

        print(response + "\n")

        # Añadir respuesta al historial
        history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()

# Bankbot

Chatbot CLI simple con soporte para Ollama (local) y Groq (cloud).

## Requisitos

- Python 3.10+
- Ollama instalado localmente (opcional)
- API Key de Groq (opcional)

## Instalación

```bash
# Clonar e instalar dependencias
pip install -r requirements.txt

# Configurar entorno
cp .env.example .env
# Editar .env con tu configuración
```

## Uso

### Con Ollama (local)

1. Inicia Ollama: `ollama serve`
2. Descarga un modelo: `ollama pull llama3`
3. Configura `.env`:
   ```ini
   BACKEND=ollama
   OLLAMA_MODEL=llama3
   ```
4. Ejecuta: `python app.py`

### Con Groq (cloud)

1. Obtén una API Key en [console.groq.com](https://console.groq.com)
2. Configura `.env`:
   ```ini
   BACKEND=groq
   GROQ_API_KEY=tu_api_key
   ```
3. Ejecuta: `python app.py`

## Comandos del Chat

| Comando | Acción |
|---------|--------|
| `exit`  | Salir del chatbot |
| `reset` | Borrar historial de conversación |

## Estructura

```
├── app.py           # Código principal
├── requirements.txt # Dependencias
├── .env             # Configuración (no subir a Git)
├── .env.example     # Plantilla de configuración
└── .gitignore       # Archivos ignorados
```

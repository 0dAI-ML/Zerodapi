# Documentación de Zerodai

Empieza!

```bash
export zerodapi_key="TU_API_KEY"
```

Chat Conversacional Simple - Sin memoria
```python

from zerodai import zerodai
import os
zerodai.api_auth(os.getenv("zerodapi_key"))
messages = []
while True:
    prompt = input("> ")
    if prompt == "exit":
        break
    messages.append({"role": "user", "content": prompt})

    messages.append({"role": "system", "content": "Eres 0dAI un asistente de ciberseguridad cuya unica función es..."})
    zerodai.inference(model="0dai70b", messages=messages, temperature=0.7, stream=True)

```
Zerodai es una librería de procesamiento de lenguaje natural orientada a ciberseguridad que busca automatizar parcialmente procesos basados en el procesamiento humano de información, razonamiento, planificación y ejecución. Buscamos crear un framework de agentes para ciberseguridad con las siguientes capacidades:

## Capacidades

- **Modularidad y adaptabilidad**: Queremos que esta librería sea fácil de implementar y de integrar con otras piezas de software.
- **Simplificación**: Queremos simplificar a un formato más humano toda la información que reciba el usuario al final de un proceso.

## Inferencias

Es el método base de interacción con el modelo y cuenta con los siguientes parámetros. Es importante que estos parámetros se aprendan y se entiendan bien, pues son la base de la librería.

### Parámetros

- **model**: El modelo de lenguaje a utilizar. Los modelos disponibles son:

  - **0dai7b**: Modelo básico con uso ilimitado, rápido y perfecto para conversaciones simples y asistencia en programación. Defiende bien en ciberseguridad.
    - 16k de contexto
    - 16 bits
    - No function calls

  - **0dai8x7b**: Modelo flexible con una ventana de contexto grande, nivel de GPT-4 en cuanto a código, bueno para preguntas y scripts complejos de ciberseguridad.
    - 32k de contexto
    - 8 bits
    - No function calls

  - **0daifn**: Modelo flexible con una ventana de contexto grande, nivel de GPT-4 en cuanto a código, bueno para preguntas y scripts complejos de ciberseguridad.
    - 64k de contexto
    - 16 bits
    - Capacidad de Function Calls

  - **0dai70b (Recomendado)**: Actualmente SOTA en ciberseguridad, capaz de hacer complejos razonamientos lógicos en base a mucho contexto y resolver pruebas de pentesting de forma semiautónoma. Cuenta con function calls y puede responder en mensajes estructurados. Es el más lento pero ofrece un gran salto de calidad.
    - 64k de contexto
    - 16 bits
    - Capacidad de function calls

- **messages**: Los mensajes que se enviarán al modelo. Aquí tenemos que entender 3 roles:
  - **system**: Prompt con instrucciones a seguir.
  - **user**: Tarea o pregunta.
  - **assistant**: Respuesta del asistente.

  Los mensajes deben ir con este formato:
```python
  messages = [
{"role": "system", "content": """Eres 0dAI tu función es..."""},
{"role": "user", "content": "0dAI escribe un exploit en C"},
]
```
- **functions**: Las funciones que se pueden llamar durante la interacción. Entraremos más a detalle en las funciones en `fn_c`. En este caso, simplemente nos dará el JSON.

  Una función se declara así:
```python
function_shodan = [ {
    "name": "shodan_dork",
    "description": "This tools is used to generate a shodan query",
    "parameter_definitions": {
      "dork": {
        "type": "string",
        "description": "The shodan dork",
        "required": True
      }
    }
  }, ]
``` 

- **temperature**: Controla la aleatoriedad de las respuestas del modelo. A mayor temperatura, más aleatoriedad; a menor temperatura, menos aleatoriedad.

- **stream (bool)**: Si se debe transmitir la respuesta en tiempo real.


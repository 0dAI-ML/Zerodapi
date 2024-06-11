# Documentación de Zerodai

Empieza!


```bash
pip install zerodai==0.0.0.20
```

```bash
export zerodapi_key="TU_API_KEY"
```
Obtén tu api key https://zerodai.com
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

### Uso:
 
```python
from zerodai import zerodai
messages = []
messages.append({"role": "user", "content": prompt})
messages.append({"role": "system", "content": "Eres 0dAI un asistente de ciberseguridad cuya unica función es..."})
zerodai.inference(model="0dai70b", messages=messages, temperature=0.7, stream=True)
```
## Function calls (fn_c)
En base a una función a una lista de funciones en el parametro **function** el Modelo será capaz de generar una respuesta estructurada que nos pueda servir una respuesta estructurada tras una inferencia: 
**Función base**
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

Respuesta del modelo en base a esta función

```json
[
    {
        "tool_name": "shodan_dork",
        "parameters": {
            "dork": "hacked-router-help-sos"
        }
    }
]
```

Estas funciones pueden ser multipaso o no, eso lo definira el numero de posiciones del JSON, una respuesta multipaso se ve así

```json
[
    {
        "tool_name": "shodan_dork",
        "parameters": {
            "dork": "hacked-router-help-sos"
        }
    },
    {
        "tool_name": "shodan_dork",
        "parameters": {
            "dork": "\"smb\" \"authentication: disabled\""
        }
    },
      {
        "tool_name": "shodan_dork",
        "parameters": {
            "dork": ".docuword_exploited.txt"
        }
     }
   ]
```

También puede existir una lógica recursiva en cuanto inferencia - función que se retroalimenten imaginemos este caso

**Función subdominios**
```python
funcion_subdomains = [ {
    "name": "subdominios",
    "description": "This tools is used to collect domains to extract subdomains",
    "parameter_definitions": {
      "domain": {
        "type": "string",
        "description": "The domain",
        "required": True
      }
    }
  }, ]
```
**Función crawler**
```python
crawler_endpoints = [ {
    "name": "crawler",
    "description": "This tools is used to crawle ndpoints for a host",
    "parameter_definitions": {
      "host": {
        "type": "string",
        "description": "The domain",
        "required": True
      }
    }
  }, ]
```
Input:

Necesito obtener los subdominios de openai.com y omegaai.io

Output 1. Función:

```json
[
    {
        "tool_name": "subdomains",
        "parameters": {
            "domain": "openai.com"
        }
    },
    {
        "tool_name": "subdomains",
        "parameters": {
            "domain": "omegaai.io"
        }
    },
]
```

Tras extraer los subdominios del input aplicamos nuestra logica de ejecución que sería obtener los subdominios...

```bash
subdomain1.openai.com
subdomain2.openai.com
subdomain3.openai.com
subdomain1.omegaai.io
subdomain2.omegaai.io
subdomain3.omegaai.io
```
Tras pasar esto a la función del crawler sería algo como 

Output 2. Función:
```json
[
    {
        "tool_name": "crawler",
        "parameters": {
            "domain": "subdominio1.openai.com"
        }
    },
    {
        "tool_name": "crawler",
        "parameters": {
            "domain": "subdominio1.omegaai.io"
        }
    },
   {
        "tool_name": "crawler",
        "parameters": {
            "domain": "subdominio2.openai.com"
        }
    },
    {
        "tool_name": "crawler",
        "parameters": {
            "domain": "subdominio2.omegaai.io"
        }
    },
   {
        "tool_name": "crawler",
        "parameters": {
            "domain": "subdominio3.openai.com"
        }
    },
    {
        "tool_name": "crawler",
        "parameters": {
            "domain": "subdominio3.omegaai.io"
        }
    },
]
```

**fn_c** Lo que nos permite es recopilar los parametros y el nombre de la tool directamente sin tener que pasar por esa logica de filtrar el JSON en si

###USO
```python
from zerodai import zerodai
zerodai.api_auth("TU_API_KEY")
tool_name, parameters = zerodai.fn_c(model_fn=model_fn_call, messages=messages, functions=subdomain_functions, stream=stream, multistep=False)
print(tool_name)
print(parameters)
print(parameters["domain"])
```
Nota: El estandar de funciones suele ser OpenAI, para ello hemos diseñado una función que convierte las funciones de openAI a nuestro formato propio, ejemplo:

```python
tool_name, parameters = cls.fn_c(model_fn=model_fn_call, messages=messages, functions=OpenAI2CommandR(osint_funcs), stream=stream, multistep=False)
```

## Agentes

Zerodai incluye un sistema de agentes que se puede extender mediante funciones y un modulo de ejecución 
```python
def exec_module(tool, arguments, multitool=True):
    output = ""
    if tool == "Shodan":
        process = subprocess.Popen(["nmap", "-Pn", next(iter(arguments.values()))], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(process.stdout.readline, b''):
            output += line.decode('utf-8').strip()
            print(line.decode('utf-8').strip())
            
    elif tool == "XSS-Scanner" or tool == "nuclei-http":
      try:
        process = subprocess.Popen(["nuclei", "-t", "dns", next(iter(arguments.values()))], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd="/home/omegaleitatadmin/exllamav2/0dAPI/nuclei-templates/nuclei-templates-9.8.6/")
        for line in iter(process.stdout.readline, b''):
            output += line.decode('utf-8').strip()
            print(line.decode('utf-8').strip())
      except:
        pass
    elif tool == "WAF-tool":
        process = subprocess.Popen(["python3", "whatwaf", "-u", "https://" + next(iter(arguments.values()))], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd="/home/omegaleitatadmin/exllamav2/0dAPI/WhatWaf")
        for line in iter(process.stdout.readline, b''):
            output += line.decode('utf-8').strip()
            print(line.decode('utf-8').strip())
      
    elif tool == "Attack":
        process = subprocess.Popen(["nmap", "-Pn", next(iter(arguments.values()))], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(process.stdout.readline, b''):
            output += line.decode('utf-8').strip()
            print(line.decode('utf-8').strip())
    elif tool == "OSINT":
        ZeroDAI.Osint(next(iter(arguments.values())))
        
    return output
```
Este codigo debe de ir a la par que las funciones usadas

```python
python_functions = [ {
    "name": "Shodan",
    "description": "tool for shodan",
    "parameter_definitions": {
      "ip": {
        "type": "string",
        "description": "The ip",
        "required": True
      }
    }
  },
 {
    "name": "nuclei-http",
    "description": "This tools is use for nuclei",
    "parameter_definitions": {
      "target": {
        "type": "string",
        "description": "The domain",
        "required": True
      }
    }
  },
 {
    "name": "WAF-tool",
    "description": "This tools is used for waf",
    "parameter_definitions": {
      "webapp": {
        "type": "string",
        "description": "The webapp",
        "required": True
      }
    }
  },
 {
    "name": "Attack",
    "description": "This tools is used to attack a host",
    "parameter_definitions": {
      "host": {
        "type": "string",
        "description": "The domain",
        "required": True
      }
    }
  }, ]
```
Esto permite hacer agentes dinamicos multipaso y multiherramienta

###Uso

```python
zerodai.agent(model="0dai70b", 
                  messages=messages, 
                  model_fn_call="0daifn", 
                  temperature=0.7,
                  functions=python_functions,
                  exec_module=exec_module,
                  exec_module_bool=True, 
                  multistep=True)
```
**exec_module-bool** para indicar si queremos usar un modulo de ejecución (Si ponemos True y no un modulo de ejecución ejecutara uno por defecto)

**exec_module** modulo de ejecución

**functions** Funciones acorde al modulo de ejecución

**multistep** Si queremos que se ejecuten varios pasos en cada iteraccion del modelo de function calls

##Pruebas de concepto 

## 4. DATA LEAKS PoC

[![DarkGPT-Osint](https://imgur.com/9JgM806.png)](https://youtu.be/C8ykBmlYm3Y)

## 5. MultiStep-Agent PoC

[![DarkGPT-Osint](https://imgur.com/poFbqJ2.png)](https://youtu.be/04IQ31xc8ws)



Esta API viene con integraciones de shodan, varios servicios de datos, censys y mucho mas, estos servicios solo requieren de la API de 0dAI:

## Filtraciones de datos
zerodai.Osint(prompt)

**prompt** - Simple mensaje en lenguaje natural para que el LLM realice una busqueda en fuentes de filtraciones de datos privadas nuestra y te de las filtraciones de un usuario

## Shodan
zerodai.Osint(prompt)

**prompt** - Simple mensaje en lenguaje natural para que el LLM realice una busqueda en shodan y te de los resultados directamente

## Rubber ducky
zerodai.rubberducky_gen(prompt)

**prompt** - Simple mensaje en lenguaje natural para que el LLM realice un payload valido de rubber ducy

Esta API ha sido desarrollada en su totalidad por Luijait (Luis Javier Navarrete Lozano) bajo 0dAI, si se usan los conocimientos descritos aquí en otro paper es necesario dar creditos al autor, como primer nombre Luijait y como segundo 0dAI

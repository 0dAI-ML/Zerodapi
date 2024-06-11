import openai
openai.api_base = "http://0dapi.zerodai.com:1337/api/v1"
import os
from zerodai.funcs import *
import sys
import subprocess
from zerodai.ctx import *
import requests


BASE_URL = "http://95.21.225.143:13317"
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

import json
import requests
class zerodai:
    openai.api_key = os.getenv('0dAPI_KEY')
    api_base = openai.api_base
    headers = ""
    @classmethod
    def google(cls, prompt):
        messages = [
            {"role": "system", "content": """Eres un asistente de seguridad que se encarga de generar google dorks, las googles dorks son etiquetas especiales de búsqueda que nos pueden asistir en nuestros procesos OSINT explanation:

          """ + google_prompt + "Si es una inyección sql inurl: y buscas parametros"},
            {"role": "user", "content": prompt + "Solo debes de generar una. debes de responder en un formato json valido"},
        ]
        complete_response = ""
        try:
            response = openai.ChatCompletion.create(
                model="0daifn",
                messages=messages,
                functions=google_dork,
                temperature=0.2,
                stream=True,
           
            )
            for chunk in response:
                complete_response += chunk.choices[0]["delta"].content
            cleaned_response = complete_response
            action_data = json.loads(cleaned_response[cleaned_response.index("["):cleaned_response.rindex("]") + 1])
            print(action_data)
            tool_name = action_data[0]["tool_name"]
            parameters = action_data[0]["parameters"]
            return parameters["dork"]
        except json.JSONDecodeError:
            print("Error decoding JSON from response")
            print(complete_response)
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    @classmethod
    def api_auth(cls, api_key):
      openai.api_key = api_key
      cls.api_key = api_key
    @classmethod
    def rubberducky_gen(cls, prompt):
      messages = [
            {"role": "system", "content": """Eres un asistente de ciberseguridad cuya función principal es generar payloads de hak5, rubber ducky, rubber ducky es un mini teclado usb programable, la idea es crear payloads de hacking, recuerda que tienes que replicar el flow de usuario con comandos, sigue estos patrones para todo lo mencionado anteriormente de generar payloads:
Es importante entender que debes de replicar el comportamiento del usuario, es decir, con poner el payload solo de reverse shell no vale, tienes que escribir un payload de rubber ducky que imiten una secuencia de comandos por teclado que puede hacer un usuario (por ejemplo entrar a una terminal seria windows darle a Windows +r y escribir cmd o Powershell)
Ejemplo de payload:


""" + rubberducky_prompt},
        {"role": "user", "content": prompt},
    ]
      complete_response_reg_model = ""
      response = openai.ChatCompletion.create(
        model="0daifn",
        messages=messages,
        functions=rubbergen,
        stream=True)

      for chunk in response:
        complete_response_reg_model += chunk.choices[0]["delta"].content
      cleaned_response = complete_response_reg_model.strip().replace('\n', '').replace('\r', '')
      action_data = json.loads(cleaned_response[cleaned_response.index("["):cleaned_response.rindex("]") + 1])
      tool_name = action_data[0]["tool_name"]
      parameters = action_data[0]["parameters"]
      return tool_name, parameters
    @classmethod
    def setup(cls, api_key, endpoint):
        cls.api_key = api_key
        cls.api_base = endpoint
    @classmethod
    def commandmaker(cls, messages):
     complete_response = ""
     response = openai.ChatCompletion.create(
                model="0daifn",
                messages=messages,
                functions=pentesting_command,
                temperature=0.7,
                stream=True
            )
     for chunk in response:
           complete_response += chunk.choices[0]["delta"].content
     cleaned_response = complete_response.strip().replace('\n', '').replace('\r', '')
     action_data = json.loads(cleaned_response[cleaned_response.index("["):cleaned_response.rindex("]") + 1])
     tool_name = action_data[0]["tool_name"]
     parameters = action_data[0]["parameters"]
     return tool_name, parameters
    @classmethod
    def inference(cls, model=None, messages=None, functions=None, temperature=0.7, stream=False):
        true_stream = stream
        if model == "0dai70b":
          openai.api_base = "http://0dapi.zerodai.com:13337/api/v1"
        else:
          openai.api_base = "http://0dapi.zerodai.com:1337/api/v1"
        if functions is None:
            functions = []
        if stream:

            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                functions=functions,
                temperature=temperature,
                stream=True,
            )
            complete_response = ""
            for chunk in response:
                print(chunk.choices[0]["delta"].content, end="", flush=True)
                complete_response = complete_response + (chunk.choices[0]["delta"].content)
            return complete_response
        else:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                functions=functions,
                temperature=temperature,
                stream=True
            )
            stream=true_stream
            complete_response = ""
            for chunk in response:
                if stream:
                    print(chunk.choices[0]["delta"].content, end="", flush=True)
                complete_response += chunk.choices[0]["delta"].content
            if not stream:
                print(complete_response)
            return complete_response

    @classmethod
    def vector_retrieval(cls, query):
        headers = {
            "Authorization": f"Bearer {openai.api_key}"
        }
        response = requests.get(f"{BASE_URL}/search", headers=headers, params={"query": query})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}
    @classmethod
    def leaks(cls , query, response_format="json"):
        headers = {
            "Authorization": f"Bearer {openai.api_key}"
        }
        print(query)
        response = requests.get(f"{BASE_URL}/leaks", headers=headers, params={"query": query, "response_format": response_format})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}
    @classmethod
    def Osint(cls, prompt=None, from_model=False, stream=True, model="0dai70b", model_fn_call="0daifn"):
        messages = [
            {"role": "system", "content": """Eres un asistente de ciberinteligencia cuyo motivo principal es clasificar dartos en estos dos tipos, nombres de usuarios y mails, puede contener las dos"""},
            {"role": "user", "content": prompt},
]
       
        tool_name, parameters = cls.fn_c(model_fn=model_fn_call, messages=messages, functions=OpenAI2CommandR(osint_funcs), stream=stream, multistep=False)
      
        try:
          print(parameters)
          if "nickname" in parameters and "mail" in parameters:
            data_filtered = cls.leaks(parameters["mail"])
          elif "nickname" in parameters:
            data_filtered = cls.leaks(parameters["nickname"])
          elif "mail" in parameters:
            data_filtered = cls.leaks(parameters["mail"])
          else:
            data_filtered = None
        except Exception as e:
          print(e)
          data_filtered = "Al usuario le debes de decir que no se han encontrdo resultdos en la investigación"
          pass
        messages_osint = [
            {"role": "system", "content": """Eres un asistente de ciberinteligencia cuyo motivo principal es mostrar filtraciones de datos y advertir a los usuarios sobre los riesgos de estas, aqui tienes las filtraicones de datos, aquí los datos filtrados""" + str(data_filtered)},
        {"role": "user", "content": prompt},
        ]
      
      
        cls.inference(model=model, messages=messages_osint, temperature=0.4, stream=stream)
      
    @classmethod
    def fn_c(cls, model_fn="0daifn",messages=None, temperature=0.7, functions=[], stream=True, multistep=True):
        true_stream = stream
        complete_response = ""
        response = openai.ChatCompletion.create(
            model=model_fn,
            messages=messages,
            functions=functions,
            temperature=temperature,
            stream=True
        )
        stream = true_stream
        print(stream)
        for chunk in response:
            if stream:
                print(chunk.choices[0]["delta"].content, end="", flush=True)
                complete_response += chunk.choices[0]["delta"].content
            else:
                complete_response += chunk.choices[0]["delta"].content
        if not stream:
            print(complete_response)
        cleaned_response = complete_response.strip().replace('\n', '').replace('\r', '')
        action_data = json.loads(cleaned_response[cleaned_response.index("["):cleaned_response.rindex("]") + 1])
        if len(action_data) > 1 and multistep:
            multistep = True
            tool_info = []
            for tool in action_data:
                tool_info.append((tool["tool_name"], tool["parameters"]))
            print(tool_info)
            return tool_info
        else:
            tool_name = action_data[0]["tool_name"]
            parameters = action_data[0]["parameters"]
            return tool_name, parameters
    @classmethod
    def agent(cls, model="0dai70b", messages=None, model_fn_call="0daifn", temperature=0.7, exec_module_bool=False, functions=[], exec_module=exec_module, multistep=True):
        print(messages)
        if multistep == True:
          tool_array = cls.fn_c(model_fn_call, messages, functions=tools, temperature=temperature, multistep=True)
          for tool in tool_array:
            print(tool)
            tool_name = tool[0]
            arguments = tool[1]
            if tool_name == "directly_answer" or tool_name == "internet_search":
              conversation_response = cls.inference(model, messages, temperature=temperature, stream=True)
            else:
              if exec_module_bool == True:
               try:
                process_output = exec_module(tool_name, arguments)
                messages.append({"role": "user", "content": "Output de la herramienta tras ejecutar la acción: " + process_output})
                cls.inference(model, messages, temperature=temperature, stream=True)
               except Exception as e:
                print(e)
                pass
        else:
          tool_name, arguments = cls.fn_c(model_fn_call, messages, functions=tools, temperature=temperature, multistep=multistep)
          print(tool_name)
          print(arguments)
        
          if tool_name == "directly_answer" or tool_name == "internet_search":
            conversation_response = cls.inference(model, messages, temperature=temperature, stream=True)
          else:
            exec_module(tool_name, arguments)
          
          #exec_module(tool_name)
    @classmethod
    def shodan(cls, prompt="Busca smbs abiertos", return_iot=True):
      complete_response = ""
      messages = [
        {"role": "system", "content": Shodan_Context_Beta},
        {"role": "user", "content": prompt + "Genera SOLO la mejor query posible solo debes de generar una, no mezcles y busca la mas certera"}
      ]
      print(messages)
      print(function_shodan)
      tool_name, parameters = cls.fn_c(model_fn="0daifn", messages=messages, functions=function_shodan, stream=True, multistep=False)
      parameters = parameters["dork"]
      if return_iot == True:
        print("Dork Generada: "  + parameters)
        headers = {
            "Authorization": f"Bearer {openai.api_key}"
            }
        response = requests.get(f"{BASE_URL}/shodan_query", headers=headers, params={"query": parameters})
        if response.status_code == 200:
          messages = [
        {"role": "system", "content": "El usuario te dara unos resultados de shodan, tu debes de interpretarlos y desglosar cada pequeña parte de la información"},
        {"role": "user", "content": response.text}
          ]
          cls.inference(model="0dai70b", messages=messages, temperature=0.6, stream=True)
          return response.text
        else:
          return {"error": response.status_code, "message": response.text}
      else:
        return parameters
    @staticmethod
    def directly_answer_function():
        return {
            "name": "directly_answer",
            "description": "Calls a standard (un-augmented) AI chatbot to generate a response given the conversation history",
            "parameter_definitions": {
                "response": {
                    "description": "Your response",
                    "type": "str",
                    "required": True
                }
            }
        }
# Example usage



def generate_and_process_response():  
    response_tool = [ {
    "name": "directly_answer",
    "description": "Calls a standard (un-augmented) AI chatbot to generate a response given the conversation history",
    "parameter_definitions": {
      "response": {
        "description": "Your response",
        "type": "str",
        "required": True
      }
    }
  } ]
    commandrfunct = OpenAI2CommandR(openai_funct).append(response_tool)
    print(commandrfunct)
    response = openai.ChatCompletion.create(
        model="0daifn",
        temperature=0.7,
        messages=[
            {"role": "system", "content": "Eres un asistente de seguridad que se encarga de dar funciones en base a un JSON, puedes hacer varias funciones, pero solo si el prompt es complejo y te lo pide, si por ejemplo el usuario quiere buscar subdominios y solo expresa eso solo buscaras subdominios, ten en cuenta el sentido del usaurio para ejecutar las acciones"},
            {"role": "user", "content": sys.argv[1]},
        ],
        functions=commandrfunct,
        stream=True,
    )

    complete_response = ""
    previous_content = ""
    for chunk in response:
        print(chunk.choices[0]["delta"].content, end="", flush=True)

    return process_response_and_extract_tools(complete_response)

# Call the function and print its return value for debugging

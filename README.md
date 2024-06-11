# Documentación de Zerodai

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

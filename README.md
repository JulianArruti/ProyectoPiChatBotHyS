# ProyectoPiChatBotHyS
 
Se propone diseñar un chatbot para proporcionar asistencia experta en normas ISO y seguridad laboral. En principio esta version seria mas de ayuda para personal de higiene y seguridad laboral (HyS) para consulta. Ya que las normas ISO son en principio muy generales ya que estan diseñadas para que cada empresa las adapte a sus necesidades. Pero la misma logica se podria aplicar cuando se tengan los protocolos especificos de la empresa. Por ejemplo, diseñar un protocolo para incendio, tratado correcto de residuos, etc. 

Me inspire en que en el lugar que trabajo a medio tiempo, estamos diseñando un sistema ERP y aplicacion movil para gestionar el flujo de trabajo para una empresa productora de carnicos en Salta. Y en este tipo de herramientas la adicion de un chatbot seria muy util para dar soporte a los usuarios si quieren implementar acreditacion ISO, la cuales no disponen y es un paso para la empresa muy dificil de implementar. En mi investigacion con gente del area de HyS, que requiere alrededor de 1000 horas para implementar en terminos de consultorias y capacitaciones. Ademas de los costos asociados, un chatbot podria ayudar a los usuarios a implementar las normas ISO de manera mas rapida y facil.

Tambien seria util para una empresa de logistica, me comentaban casos que hay protocolos y manuales para aplicar vidrios, paneles y otros materiales. Que tienen que ser especifico y se tira mucho material si se aplica mal. Podria hacerse la misma funcionalidad, la razon para priorizar la aplicacion de HyS es que los documentos son bastante estandarizado y siguen un mismo formato.


Resultados

Se logro implementar un chatbot que puede responder preguntas sobre seguridad laboral y normas ISO. El chatbot utiliza embeddings de documentos para generar respuestas basadas en el contenido de los documentos, en los cuales se realizo preprocesamiento para guardar el titulo y el contenido de los capitulos de las normas ISO.

Se eligio chunks acorde a que se tomara gran parte de las seccion, ya que usa informacion mas global de la norma. Se sumo a la obtencion de chunks como contexto, pautas profesionales como "safety_rules" en la cual se guardan las reglas de seguridad y terminologia especifica en la cual profesioales de HyS podrian aportar su parte para mejorar la funcionalidad del chatbot, la cual seria mas util en protocolos personalizados a la empresa.


Pendientes:

Se tenia la intencion de usar la tecnica Multi-Query y RAG-Fusion, la razon principal de elegir esta tecnica es pensando en el usuario final, donde no tendrian mucho conocimiento para realizar las preguntas en un formato abarcativo. No el inicial que serian los tecnicos y licenciados de HyS, sino los obreros que quieran realizar consultas sobre seguridad laboral y sobre los procedimientos vistos en las capacitaciones. Si hacen preguntas difusas por no conocer la terminologias, el multi-query y RAG-Fusion ayudarian a generar respuestas mas precisas, al generar preguntas mas especificas.

Controles de idiomas

Treshhold de similitud: Se eligio como inicial 0,7 ya que se queria que no respondiera preguntas sino tenia informacion correcta (dar informacion incorrecta de seguridad es un peligro en si tambien) pero no lograba que me diera respuestas al ser generales. Asi que lo baje a 0,1 para que responda preguntas mas generales. Se tendria que ajustar en cada caso

La idea completa era generar un sistema completo movil frontend-backend, donde el frontend seria una aplicacion movil, y el backend seria el chatbot, conectado a un login de usuario. Donde planeaba hacer tools para consultas de seguridad laboral, y de ISO. Ademas de que los gerentes podrian consultar informacion de asistencia de los empleados al trabajo y las capacitaciones que se realizan. Y por que no a mas areas como la de ventas y lineas de trabajo. Esta pensado para asistir y dar valor adicional a aplicaciones de gestion desarrolladas para la empresa.




Uso
Accede a los endpoints para cargar documentos, consultar documentos almacenados y realizar preguntas sobre seguridad laboral.
La aplicación procesa los documentos y genera respuestas basadas en el contenido y las normas ISO.

Deje una ISO sin cargar, que es la 14001 para que puedan chequear que se cargue (espero no me traicione el codigo 😂). Disculpen nuevamente que no pudiera presentarme a la defensa, estoy escribiendo esta parte a las 13:54, con lo justo termine de hacerlo "funcional".


Tecnologías Utilizadas
FastAPI: Framework para construir APIs rápidas y eficientes en Python.
Cohere: Plataforma de procesamiento de lenguaje natural utilizada para embeddings y generación de texto.
Langchain: Biblioteca para la integración de modelos de lenguaje y herramientas de recuperación de información.
ChromaDB: Almacenamiento de vectores para gestionar y consultar documentos procesados.
NumPy: Biblioteca para cálculos numéricos, utilizada para calcular similitudes entre embeddings.


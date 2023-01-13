# demanda-real
El proyecto descarga datos de la API de la red eléctrica española y los grafica. Posteriormente realiza un análisis frecuencial y lo grafica también.

# Instrucciones
Para utilizar el proyecto se debe obtener un token para la API de E-sios de la red eléctrica española. Se puede obtener en: https://api.esios.ree.es/
Este token debe guardarse en un archivo llamado `config.py` en la raíz del proyecto. Se debe guardar el token como un string llamado api_token. Ejemplo: `api_token = "sdfkjewrkamrkcmsfkl"`

Para ejecutar el proyecto en las mismas condiciones en las que ha sido realizado, se proporciona el archivo `requirements.txt` que puede ser cargado creando un entorno virtual con venv. Puedes ver cómo crear un entorno virtual con venv en mi web: https://todoia.es/entornos-virtuales-con-python/
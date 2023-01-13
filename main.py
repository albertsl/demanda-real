import requests
from config import api_token
from os import path, mkdir
from datetime import datetime

def _save_data_json(response):
    """Guarda los datos descargados de la API en un archivo. Primero comprueba si existe la carpeta data, si no existe la crea. Guarda los datos en esa carpeta, en un archivo con nombre la fecha y hora actual. Ejemplo: "13-01-2023 06-48-35.json"

    Args:
        response (dict): JSON de la respuesta de la API
    """
    if not path.isdir("data"):
        mkdir("data")

    dt = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    with open(f"data/{dt}.json", "w") as f:
        f.write(str(response))

def get_indicator(id_ree, start_date, end_date, token):
    """Descargar datos del indicador especificado con su id en un rango de datos concreto. Se utiliza el siguiente endpoint de la API de REE:
    https://api.esios.ree.es/indicator/getting_a_specific_indicator_filtering_values_by_a_date_range

    Args:
        id_ree (int): numero identificador de los datos
        start_date (str): fecha de inicio de los datos. Se debe introducir siguiendo el formato ISO 8601, yyyy-mm-ddThh:mm ejemplo: "2018-09-02T00%3A00"
        end_date (str): fecha de fin de los datos. Se debe introducir siguiendo el formato ISO 8601, yyyy-mm-ddThh:mm ejemplo: "2018-09-02T00%3A00"
        token (str): token de acceso a la API proporcionado por REE

    Returns:
        list: listado de valores del indicador. Está probado con el id 1293, otros datos es posible que tengan otro formato, habría que comprobarlo.
    """
    url = f"https://api.esios.ree.es/indicators/{id_ree}?start_date={start_date}&end_date={end_date}"
    headers = {"Accept": "application/json; application/vnd.esios-api-v1+json",
                "Content-Type": "application/json",
                "Host": "api.esios.ree.es",
                "Authorization": f"Token token=\"{token}\"",
                "Cookie": ""}
    response = requests.get(url, headers=headers)
    response_json = response.json()

    _save_data_json(response_json)

    value_list = response_json['indicator']['values']
    final_values = [i['value'] for i in value_list]

    return final_values

if __name__ == "__main__":
    #datos que queremos solicitar a la API de REE
    id_ree = 1293
    start_date = "2018-09-02T00%3A00" #formato ISO 8601
    end_date = "2018-10-06T00%3A00" #formato ISO 8601

    data = get_indicator(id_ree, start_date, end_date, api_token)
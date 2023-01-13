import requests
import matplotlib.pyplot as plt
import numpy as np
from config import api_token
from os import path, mkdir
from datetime import datetime
from scipy.fft import fft, fftfreq

def _save_data_json(response):
    """Guarda los datos descargados de la API en un archivo. Primero comprueba si existe la carpeta data, si no existe la crea. Guarda los datos en esa carpeta, en un archivo con nombre la fecha y hora actual. Ejemplo: "13-01-2023 06-48-35.json"

    Args:
        response (dict): JSON de la respuesta de la API
    """
    if not path.isdir("data"):
        mkdir("data")

    #se usa datetime.now() para dar nombre al archivo
    dt = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    with open(f"data/{dt}.json", "w") as f:
        f.write(str(response))

def get_indicator(id_ree, start_date, end_date, token):
    """Descargar datos del indicador especificado con su id en un rango de fechas concreto. Se utiliza el siguiente endpoint de la API de REE:
    https://api.esios.ree.es/indicator/getting_a_specific_indicator_filtering_values_by_a_date_range
    Se obtienen datos en el rango temporal indicado dividos en franjas de 5 minutos. 

    Args:
        id_ree (int): numero identificador de los datos
        start_date (str): fecha de inicio de los datos. Se debe introducir siguiendo el formato ISO 8601, yyyy-mm-ddThh:mm ejemplo: "2018-09-02T00%3A00"
        end_date (str): fecha de fin de los datos. Se debe introducir siguiendo el formato ISO 8601, yyyy-mm-ddThh:mm ejemplo: "2018-09-02T00%3A00"
        token (str): token de acceso a la API proporcionado por REE

    Returns:
        list: listado de valores del indicador. Está probado con el id 1293, otros datos es posible que tengan otro formato, habría que comprobarlo.
    """
    url = f"https://api.esios.ree.es/indicators/{id_ree}?start_date={start_date}&end_date={end_date}&time_trunc=five_minutes"
    headers = {"Accept": "application/json; application/vnd.esios-api-v1+json",
                "Content-Type": "application/json",
                "Host": "api.esios.ree.es",
                "Authorization": f"Token token=\"{token}\"",
                "Cookie": ""}
    response = requests.get(url, headers=headers)
    response_json = response.json()

    #se guardan los datos descargados
    _save_data_json(response_json)

    #seleccionamos unicamente los datos del valor del indicador
    value_list = response_json['indicator']['values']
    real_demand = [i['value'] for i in value_list]

    return real_demand

def freq_analysis(values):
    """Calcula usando la FFT, los valores que se pondrán en la gráfica del dominio frecuencial

    Args:
        values (list): listado de valores a los que hacer la FFT. Para que funcione correctamente han de venir muestreados a una muestra cada 5 minutos.

    Returns:
        positive_freqs (np.ndarray): Eje x para la gráfica
        positive_yf (np.ndarray): Eje y para la gráfica
    """
    #periodo de muestreo, cada x segundos. Como es cada 5 minutos, obtenemos una muestra cada 300 segundos. fs=1/Ts
    fs = 1/(5*60)

    #calculamos los valores del FFT, para graficar nos quedamos únicamente con las freq positivas.
    yf = fft(values)
    freqs = fftfreq(len(values), 1/fs)
    positive_freqs = freqs[np.where(freqs >= 0)]
    positive_yf = yf[np.where(freqs >= 0)]

    return positive_freqs, positive_yf

def generate_plots(real_demand, freqs, yf):
    """Genera el gráfico que muestra tanto el dominio temporal como el dominio frecuencial. Lo guarda en una carpeta y lo muestra por pantalla. No retorna nada.

    Args:
        real_demand (list): Valores para el eje y del dominio temporal
        freqs (np.ndarray): Valores para el eje x del dominio frecuencial
        yf (np.ndarray): Valores para el eje y del dominio frecuencial
    """
    #ax1 será dominio temporal, ax2 dominio frecuencial
    fig, (ax1, ax2) = plt.subplots(2,1)
    ax1.plot(real_demand, color="red")

    ax2.plot(freqs, np.abs(yf))
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Amplitude')
    ax2.axis(xmin=0, xmax=0.0001, ymin=0, ymax=0.2*1e8)
    plt.show()

if __name__ == "__main__":
    #datos que queremos solicitar a la API de REE
    id_ree = 1293
    start_date = "2018-09-02T00%3A00" #formato ISO 8601
    end_date = "2018-10-06T00%3A00" #formato ISO 8601

    real_demand = get_indicator(id_ree, start_date, end_date, api_token)
    freqs, yf = freq_analysis(real_demand)
    generate_plots(real_demand, freqs, yf)
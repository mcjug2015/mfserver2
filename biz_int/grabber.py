''' grabs meetings and puts them in res '''
import os
import requests


def get_json(url, output_name,
             output_dir=os.path.join(os.path.dirname(__file__), 'res')):
    ''' do a get against url and store resulting json in output '''
    response = requests.get(url)
    response.raise_for_status()
    output_handle = open(os.path.join(output_dir, output_name), 'wb')
    output_handle.write(response.content)
    output_handle.close()

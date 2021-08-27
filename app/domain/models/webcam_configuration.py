from app.domain.packs.json_pack import JsonPack
from app.domain.errors.app_error import AppError
from app.configuration import JSON_VIDEO_PARAMETERS_PATH, SEE_VIDEO_CONFIG, VIDEO_AUTO_CONFIGURATION
from app.configuration import VIDEO_CONFIG_ARG, VIDEO_CONFIG_INIT, VIDEO_DISABLE_CONFIGURATION
import subprocess
from time import sleep


command = []

class WebcamConfiguration:
    def __init__(self, current_port):
        self.current_port = current_port

    def apply_current_config(self):
        original_config = JsonPack.read(JSON_VIDEO_PARAMETERS_PATH)
        self.change_auto_configuration(enable=False)
        command = ''
        for index, key in enumerate(original_config.keys()):
            command += f'{VIDEO_CONFIG_INIT}{self.current_port}'
            command += f' {VIDEO_CONFIG_ARG}{key}={original_config[key]}'
            if index != len(original_config.keys()) - 1:
                command += ' && '
        subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None)

    def auto_config(self):
        self.change_auto_configuration(enable=True)
        sleep(15)
        self.change_auto_configuration(enable=False)
        self.save_new_configuration()

    def change_auto_configuration(self, enable):
        command = ''
        length = len(VIDEO_AUTO_CONFIGURATION)
        for index in range(length):
            command += f'{VIDEO_CONFIG_INIT}{self.current_port}'
            command += f' {VIDEO_CONFIG_ARG}{(VIDEO_AUTO_CONFIGURATION if enable else VIDEO_DISABLE_CONFIGURATION)[index]}'
            if index != length - 1:
                command += ' && '
        subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None)

    def save_new_configuration(self):
        command = f'{VIDEO_CONFIG_INIT}{self.current_port} {SEE_VIDEO_CONFIG}'
        response, _ = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
        if response is None:
            raise AppError('save_new_configuration', 'Resposta de configuração inválida')
        original_config = JsonPack.read(JSON_VIDEO_PARAMETERS_PATH)
        elements = list(filter(lambda x: x not in ['\t', '\n', '\r', ''], response.decode('utf-8').split('\n')))
        for key in original_config.keys():
            filtered = list(filter(lambda x: x.find(f'{key} ') != -1, elements))
            if len(filtered) != 0:
                original_config[key] = filtered[0].split('value=')[-1].split(' ')[0]
        JsonPack.write(JSON_VIDEO_PARAMETERS_PATH, original_config)


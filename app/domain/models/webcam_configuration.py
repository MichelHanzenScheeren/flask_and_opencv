import subprocess
from time import sleep
from app.domain.packs.json_pack import JsonPack
from app.domain.errors.app_error import AppError
import app.configuration as config


class WebcamConfiguration:
    def __init__(self, current_port):
        self.current_port = current_port

    def apply_current_config(self):
        original_config = JsonPack.read(config.JSON_VIDEO_PARAMETERS_PATH)
        self.change_auto_configuration(enable=False)
        command = ''
        for index, key in enumerate(original_config.keys()):
            command += f'{config.VIDEO_CONFIG_INIT}{self.current_port}'
            command += f' {config.VIDEO_CONFIG_ARG}{key}={original_config[key]}'
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
        length = len(config.VIDEO_ON_CONFIG)
        for index in range(length):
            command += f'{config.VIDEO_CONFIG_INIT}{self.current_port} {config.VIDEO_CONFIG_ARG}'
            command += f'{(config.VIDEO_ON_CONFIG if enable else config.VIDEO_OFF_CONFIG)[index]}'
            if index != length - 1:
                command += ' && '
        subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None)

    def save_new_configuration(self):
        command = f'{config.VIDEO_CONFIG_INIT}{self.current_port} {config.SEE_VIDEO_CONFIG}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        response, _ = process.communicate()
        if response is None:
            raise AppError('save_new_configuration', 'Resposta de configuração inválida')
        original_config = JsonPack.read(config.JSON_VIDEO_PARAMETERS_PATH)
        elements = list(filter(lambda x: x not in ['\t', '\n', '\r', ''], response.decode('utf-8').split('\n')))
        for key in original_config.keys():
            filtered = list(filter(lambda x: x.find(f'{key} ') != -1, elements))
            if len(filtered) != 0:
                original_config[key] = filtered[0].split('value=')[-1].split(' ')[0]
        JsonPack.write(config.JSON_VIDEO_PARAMETERS_PATH, original_config)

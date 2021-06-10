from flask import request, send_file


def configure_routes(app, valvesUseCase):
    """ Arquivo que cria e define as rotas relacionadas ao controle das válvulas.

    O decorator @app.route define a rota http, e o método que segue define a resposta.
    """
    @app.route('/submit_valves_config', methods=['POST'])
    def submit_valves_config():
        return valvesUseCase.submit_valves_config(request.json['valves'])

    @app.route('/submit_programming', methods=['POST'])
    def submit_programming():
        return valvesUseCase.submit_programming(request.json)

    @app.route('/upload_user_programming', methods=['POST'])
    def upload_user_programming():
        return valvesUseCase.upload_user_programming(request.json)

    @app.route('/download_programming', methods=['POST'])
    def download_programming():
        path = valvesUseCase.get_programming_path()
        return send_file(path, download_name='programming.json')

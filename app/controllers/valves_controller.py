from flask import request, render_template


def configure_routes(app, valvesUseCase):
    """ Arquivo que cria e define as rotas relacionadas ao controle das válvulas.

    O decorator @app.route define a rota http, e o método que segue define a resposta.
    """
    @app.route('/submit_valves_config', methods=['POST'])
    def submit_valves_config():
        return valvesUseCase.submit_valves_config(request.json['valves'])

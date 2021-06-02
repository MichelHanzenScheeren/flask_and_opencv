from flask import request, render_template


def configure_routes(app, valvesUseCase):
    """ Arquivo que cria e define as rotas relacionadas ao controle das válvulas.

    O decorator @app.route define a rota http, e o método que segue define a resposta.
    """
    @app.route('/test', methods=['GET'])
    def test():
        return 'OLA'

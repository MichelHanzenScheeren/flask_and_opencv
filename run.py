from app import create_app
from app.controllers.default import stop_stream


if __name__ == '__main__':
    create_app().run(debug=True, threaded=True, use_reloader=False)

# Parar Stream:
stop_stream()
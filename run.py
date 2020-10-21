import argparse
from app import create_app


if __name__ == '__main__':
    my_args = argparse.ArgumentParser()
    my_args.add_argument('--host', type=str, default='127.0.0.1', help='ip address. 0.0.0.0 to network local acces')
    my_args.add_argument('--port', type=int, default=5000, help='port number server')
    args = vars(my_args.parse_args())

    create_app().run(
        host=args['host'], 
        port=args['port'], 
        debug=True, 
        threaded=True, 
        use_reloader=True
    )

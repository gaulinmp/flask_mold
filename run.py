from baseapp import create_app

from config.logging_server import DevConfig

app = create_app(DevConfig)

if __name__ == '__main__':
    app.run()

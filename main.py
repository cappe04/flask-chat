import src.settings as settings

import src.app as app

if __name__ == "__main__":
    app.run(port=settings.PORT,
            host=settings.HOST,
            debug=True)
import app
import app.socketio

application = app.create_app()

if __name__ == "__main__":
    app.socketio.run(application,
                     port=app.settings.PORT,
                     host=app.settings.HOST,
                     debug=True)
from flask_backend import get_app

app = get_app()

if __name__ == '__main__':
    app.run(user_reloader=False, host='0.0.0.0', port=5000, threaded=True)

from flask_backend import get_app

app = get_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)

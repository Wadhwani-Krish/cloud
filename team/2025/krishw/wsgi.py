from modelEarth_login import create_app
app = create_app()

if __name__ == '__main__':
    app.run(port=5000, debug=True, ssl_context=("cert.pem","key.pem"))

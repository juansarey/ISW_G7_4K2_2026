from ecoharmony.web.app import crear_app

PUERTO = 5000

if __name__ == "__main__":
    crear_app().run(port=PUERTO, debug=True)

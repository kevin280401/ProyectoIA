from app import create_app

# Crea la instancia de la aplicación Flask
app = create_app()

# Verifica que el archivo se ejecute directamente
if __name__ == "__main__":
    app.run()

import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
from .models import Link, LinkList, User, db  # Importa db desde models
from .services import add_link_to_list, create_user, create_link_list, search_links_by_keyword

# Directorio donde se almacenarán los archivos subidos
UPLOAD_FOLDER = 'uploads/'

def init_routes(app):
    # Configurar la carpeta de uploads en la app
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Asegúrate de que la carpeta de uploads exista
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Ruta para subir archivos a almacenamiento local
    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return jsonify({"error": "No se encontró ningún archivo"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No se seleccionó ningún archivo"}), 400

        # Asegura que el nombre del archivo sea seguro para el sistema de archivos
        filename = secure_filename(file.filename)

        # Ruta completa donde se guardará el archivo
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Guarda el archivo en el almacenamiento local
        file.save(file_path)

        return jsonify({"message": "Archivo subido correctamente", "file_path": file_path}), 201

    # Ruta para eliminar un enlace por su ID
    @app.route('/api/links/<int:id>', methods=['DELETE'])
    def delete_link(id):
        link = Link.query.get_or_404(id)
        try:
            db.session.delete(link)
            db.session.commit()
            return jsonify({"message": "Link deleted successfully", "link_id": id}), 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error deleting link: {str(e)}'}), 500

    # Ruta para crear un nuevo usuario
    @app.route('/api/users', methods=['POST'])
    def create_new_user():
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        result = create_user(username, email, password)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 201

    # Ruta para crear una nueva lista de enlaces
    @app.route('/api/link-lists', methods=['POST'])
    def create_new_link_list():
        data = request.get_json()
        user_id = data.get('user_id')
        title = data.get('title')
        description = data.get('description', None)
        category = data.get('category', None)

        result = create_link_list(user_id, title, description, category)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 201

    # Ruta para agregar un enlace a una lista de enlaces
    @app.route('/api/link-lists/<int:link_list_id>/links', methods=['POST'])
    def add_new_link_to_list(link_list_id):
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "URL is required"}), 400

        result = add_link_to_list(link_list_id, url)
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "Link added successfully", "link": result}), 201

    # Ruta para buscar enlaces por palabra clave
    @app.route('/api/search-links', methods=['GET'])
    def search_links():
        user_id = request.args.get('user_id')
        keyword = request.args.get('keyword')

        if not user_id or not keyword:
            return jsonify({"error": "Both user_id and keyword are required"}), 400

        result = search_links_by_keyword(user_id, keyword)

        if not result:
            return jsonify({"message": "No links found for the given keyword"}), 404

        return jsonify(result), 200

    # Ruta para agregar un enlace a una lista predeterminada o la especificada
    @app.route('/api/links', methods=['POST'])
    def add_link():
        data = request.get_json()
        url = data.get('url')
        link_list_id = data.get('link_list_id', 1)  # Predetermina 1 si no se proporciona un link_list_id

        if not url:
            return jsonify({"error": "URL is required"}), 400

        # Agregar el enlace a la lista de enlaces con el ID proporcionado o el predeterminado
        result = add_link_to_list(link_list_id, url)

        if "error" in result:
            return jsonify(result), 500

        return jsonify(result), 201

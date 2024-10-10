import requests
from .models import db, User, LinkList, Link
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from newspaper import Article  # Para extraer metadatos de los enlaces
import re

# Importaciones adicionales para el modelo de clasificación
import tensorflow as tf
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk
from .inference import predict_category  # Importa la función de predicción

from flask import jsonify
from .models import Link, LinkList, User, db
from .inference import predict_category  # Asegúrate de que esta línea sea correcta
from newspaper import Article  # Para extraer metadatos de los enlaces

# Descargar recursos de NLTK (asegúrate de hacer esto una sola vez)
nltk.download('stopwords')
nltk.download('punkt')

# Cargar el modelo entrenado de clasificación
model = tf.keras.models.load_model('backend/models/website_classification_model.h5')

# Definir vocabulario y longitud de secuencia (deben coincidir con los usados en el entrenamiento)
vocab_size = 8000
len_sentence = 20

# Lista de categorías (debe coincidir con las utilizadas durante el entrenamiento)
categories = ["AI", "Travel", "Education", "General"]  # Ajusta esta lista según tus categorías reales

# Instancia del stemmer y stopwords
ps = PorterStemmer()
stopwords_set = set(stopwords.words("english"))

# Servicio para crear un nuevo usuario
def create_user(username, email, password):
    try:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully", "user_id": new_user.id}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}

# Servicio para crear una lista de enlaces para un usuario
def create_link_list(user_id, title, description=None, category=None):
    try:
        new_list = LinkList(user_id=user_id, title=title, description=description, category=category)
        db.session.add(new_list)
        db.session.commit()
        return {"message": "Link list created successfully", "list_id": new_list.id}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}

# Servicio para agregar un enlace a una lista de enlaces
def add_link_to_list(link_list_id, url):
    try:
        metadata = extract_metadata_from_url(url)
        if "error" in metadata:
            return {"error": metadata["error"]}, 400  # Manejar error al extraer metadatos

        # Usa el modelo para predecir la categoría del enlace automáticamente
        category = predict_category(metadata.get("description", ""))

        new_link = Link(
            link_list_id=link_list_id,
            url=url,
            title=metadata.get("title"),
            description=metadata.get("description"),
            image_url=metadata.get("image_url"),
            category=category
        )
        db.session.add(new_link)
        db.session.commit()
        return {"message": "Link added successfully", "link_id": new_link.id, "url": new_link.url, "category": new_link.category}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}, 500

# Servicio para buscar en las listas de enlaces de un usuario
def search_links_by_keyword(user_id, keyword):
    try:
        # Buscar en el título, descripción, o categoría de los enlaces
        results = Link.query.join(LinkList).filter(
            LinkList.user_id == user_id,
            (Link.title.ilike(f"%{keyword}%") | Link.description.ilike(f"%{keyword}%"))
        ).all()
        
        links_data = [
            {
                "url": link.url,
                "title": link.title,
                "description": link.description,
                "image_url": link.image_url,
                "category": link.category
            }
            for link in results
        ]
        return {"results": links_data}
    except SQLAlchemyError as e:
        return {"error": str(e)}

# Servicio para compartir una lista de enlaces (generar enlace público)
def share_link_list(link_list_id):
    # Puedes implementar la lógica para generar un enlace compartible o un token público
    # Aquí solo se retorna un ejemplo de respuesta
    return {"message": "List shared successfully", "shareable_link": f"/shared/{link_list_id}"}

# Función para preprocesar el texto (stemming y limpieza)
def preprocess_text(text):
    # Eliminar caracteres especiales y números
    text_cleaned = re.sub("[^a-zA-Z]", " ", text)
    text_cleaned = text_cleaned.lower().split()
    
    # Remover stopwords y aplicar stemming
    text_cleaned = [ps.stem(word) for word in text_cleaned if word not in stopwords_set]
    return ' '.join(text_cleaned)

# Servicio para inferir la categoría del enlace utilizando el modelo de clasificación
def infer_category_from_content(content):
    try:
        # Preprocesar el texto del contenido del enlace
        cleaned_content = preprocess_text(content)
        
        # Codificar el texto
        encoded_text = one_hot(cleaned_content, vocab_size)
        padded_text = pad_sequences([encoded_text], maxlen=len_sentence, padding='pre')
        
        # Clasificar usando el modelo
        prediction = model.predict(padded_text)
        predicted_category_index = prediction.argmax(axis=1)[0]
        
        # Obtener la categoría correspondiente
        predicted_category = categories[predicted_category_index]
        
        return predicted_category
    except Exception as e:
        return "General"  # Categoría predeterminada en caso de error

# Servicio para extraer metadata de un URL utilizando Newspaper3k y clasificar automáticamente
def extract_metadata_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()

        content = article.text
        category = infer_category_from_content(content)

        metadata = {
            "title": article.title,
            "description": article.meta_description,
            "image_url": article.top_image,
            "category": category
        }

        return metadata
    except Exception as e:
        return {"error": f"Failed to extract metadata: {str(e)}"}  # Asegúrate de que cualquier error se capture aquí
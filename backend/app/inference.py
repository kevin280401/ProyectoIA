# backend/app/inference.py

import tensorflow as tf
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import re
import nltk

# Asegúrate de que los recursos de NLTK estén descargados
nltk.download('stopwords')
nltk.download('punkt')

# Cargar el modelo entrenado de clasificación
model = tf.keras.models.load_model('models/website_classification_model.h5')  # Asegúrate de que la ruta sea correcta

# Definir vocabulario y longitud de secuencia
vocab_size = 8000
len_sentence = 20

# Lista de categorías
categories = ["AI", "Travel", "Education", "General"]

# Instancia del stemmer y stopwords
ps = PorterStemmer()
stopwords_set = set(stopwords.words("english"))

def clean_text(text):
    # Eliminar caracteres especiales y números
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)
    text = text.lower()
    # Tokenizar
    tokens = nltk.word_tokenize(text)
    # Eliminar stopwords y aplicar stemming
    filtered_tokens = [ps.stem(word) for word in tokens if word not in stopwords_set]
    return ' '.join(filtered_tokens)

def predict_category(url):
    try:
        # Extraer el contenido del artículo usando newspaper3k
        article = tf.keras.preprocessing.text.text_to_word_sequence(url)  # Esto es solo un placeholder
        # En una implementación real, extraerías el contenido del artículo
        # y lo limpiarías antes de pasar al modelo.
        
        # Por ejemplo:
        # article = Article(url)
        # article.download()
        # article.parse()
        # text = clean_text(article.text)
        
        # Aquí asumimos que 'text' es el contenido limpio del artículo
        text = clean_text(url)  # Reemplaza con el contenido real del artículo
        
        # Convertir el texto a secuencia
        encoded = one_hot(text, vocab_size)
        padded = pad_sequences([encoded], maxlen=len_sentence, padding='pre')
        
        # Realizar la predicción
        prediction = model.predict(padded)
        predicted_category = categories[prediction.argmax()]
        
        return predicted_category
    except Exception as e:
        return {"error": str(e)}

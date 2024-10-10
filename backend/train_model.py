import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Descargar recursos de NLTK
nltk.download('stopwords')
stopwords = set(stopwords.words("english"))
ps = PorterStemmer()

# Función de preprocesamiento
def preprocess_text(text):
    # Eliminar caracteres especiales y números
    text_cleaned = re.sub("[^a-zA-Z]", " ", text)
    text_cleaned = text_cleaned.lower().split()
    
    # Remover stopwords y aplicar stemming
    text_cleaned = [ps.stem(word) for word in text_cleaned if not word in stopwords]
    return ' '.join(text_cleaned)

# Cargar el dataset
df = pd.read_csv("C:\Users\Kevin\Desktop\Semestre\ProyectosIA\LinkScribe\backend\website_classification.csv")
df = df.dropna()

# Preprocesar el texto
df['cleaned_website_text'] = df['website_text'].apply(preprocess_text)

# Codificar las categorías
le = LabelEncoder()
df["Category"] = le.fit_transform(df["Category"])

# Definir vocabulario y longitud de secuencia
vocab_size = 8000
len_sentence = 20

# Codificar el texto
X = [one_hot(d, vocab_size) for d in df['cleaned_website_text']]
X = pad_sequences(X, maxlen=len_sentence, padding='pre')

# Definir el target
y = np.array(df["Category"])
y = to_categorical(y, num_classes=len(df["Category"].unique()))

# Dividir en entrenamiento y test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo
model = Sequential()
model.add(Dense(units=64, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=y_train.shape[1], activation='softmax'))

# Compilar el modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit(X_train, y_train, epochs=50)

# Guardar el modelo entrenado
model.save('website_classification_model.h5')
print("Modelo guardado en website_classification_model.h5")

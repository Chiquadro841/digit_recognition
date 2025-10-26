from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# Carica il modello salvato
model = load_model('cnn_model.h5')

# Nome del file immagine nella stessa directory
image_path = "test.png"  # Sostituisci con il nome dell'immagine

# Funzione per caricare e preprocessare l'immagine
def preprocess_image(image_path):
    try:
        # Apri l'immagine e convertila in scala di grigi
        image = Image.open(image_path).convert('L')

        # Ridimensiona l'immagine a 28x28 pixel
        image = image.resize((28, 28))

        # Converti l'immagine in un array numpy e normalizza
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=(0, -1))  # Aggiungi dimensioni batch e canale

        return image_array
    except Exception as e:
        print(f"Errore durante il caricamento dell'immagine: {e}")
        return None

# Preprocessa l'immagine
image_array = preprocess_image(image_path)

if image_array is not None:
    # Esegui la previsione
    prediction = model.predict(image_array)
    predicted_class = int(np.argmax(prediction))
    print(f"Il modello ha predetto la classe: {predicted_class}")
else:
    print("Non è stato possibile elaborare l'immagine.")

from flask import Flask, request, jsonify, render_template
import numpy as np
from PIL import Image
import base64
import io
import joblib
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
import base64
import csv
from io import BytesIO  # Importa BytesIO
from flask import Flask, request, jsonify
from PIL import Image

# Crea l'app Flask
app = Flask(__name__)

model = load_model('cnn_model.h5')


# Route per la pagina principale
@app.route('/')
def index():
    return render_template('index.html')  # Renderizza il template index.html


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Ottieni i dati JSON inviati dal client
        data = request.get_json()

        # Decodifica l'immagine base64
        image_data = data['image_base64'].split(',')[1]  # Rimuovi il prefisso 'data:image/png;base64,'
        image_bytes = base64.b64decode(image_data)

        # Carica l'immagine in PIL
        image = Image.open(io.BytesIO(image_bytes)).convert('L')  # Converti in scala di grigi

        # Ridimensiona l'immagine a 28x28 pixel
        image = image.resize((28, 28))

        # Converti l'immagine in array numpy e normalizza i valori tra 0 e 1
        image_array = np.array(image) / 255.0

        # Aggiungi una dimensione per rappresentare il batch (necessario per Keras)
        image_array = np.expand_dims(image_array, axis=(0, -1))

        # Fai la previsione con il modello
        prediction = model.predict(image_array)
        predicted_class = int(np.argmax(prediction))

        # Restituisci il risultato come JSON
        return jsonify({"predicted_class": predicted_class})

    except Exception as e:
        print("Errore:", e)
        return jsonify({"error": "Errore durante la previsione"}), 500

    except Exception as e:
        # Se c'è un errore, restituisci un errore
        return jsonify({"error": str(e)})
    
    
    
# Directory per salvare le immagini
SAVE_DIR = 'dataset'
CSV_FILE = 'records.csv'

# Crea il CSV nella directory principale se non esiste
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['pixel_values', 'target'])  # Intestazioni del CSV

@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.get_json()
    img_data = data.get('image')
    target = data.get('target')

    if img_data is None or target is None:
        return jsonify({'success': False, 'message': 'Missing image data or target'}), 400

    # Rimuovi il prefisso "data:image/png;base64,"
    img_data = img_data.split(',')[1]

    # Decodifica la stringa base64
    img_bytes = base64.b64decode(img_data)

    # Crea un'immagine a partire dai byte
    img = Image.open(BytesIO(img_bytes))

    # Ridimensiona l'immagine a 28x28
    img = img.resize((28, 28))

    # Ottieni i dati dei pixel dell'immagine ridimensionata
    image_data = img.convert("L")  # Converti l'immagine in scala di grigi
    pixels = list(image_data.getdata())  # Ottieni i valori dei pixel come lista

    # Salva l'immagine nella directory 'dataset/'
    img_filename = os.path.join(SAVE_DIR, 'image_{}.png'.format(len(os.listdir(SAVE_DIR)) + 1))
    #img.save(img_filename)

    # Salva i dati dei pixel e il target nel CSV nella directory principale
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Scrive i valori dei pixel e il target (convertiti in stringa per il CSV)
        writer.writerow([','.join(map(str, pixels)), target])

    return jsonify({'success': True, 'message': 'Image and data saved successfully', 'filename': img_filename})


if __name__ == '__main__':
    app.run(debug=True)

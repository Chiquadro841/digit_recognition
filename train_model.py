import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import accuracy_score
from sklearn import datasets
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense




# Leggi il CSV
df = pd.read_csv('records.csv')

# Converti la colonna 'pixel_values' in array numerici
df['pixel_values'] = df['pixel_values'].apply(lambda x: np.fromstring(x, sep=','))

# Estrai i dati e le etichette
X = np.stack(df['pixel_values'].values)  # Converte in un array 2D di shape (n_samples, 784)
y = df['target'].values

# Normalizzazione
X = X / 255.0

# Ridimensiona X per aggiungere il canale (necessario per Conv2D)
X = X.reshape(-1, 28, 28, 1)

# One-hot encoding delle etichette
y = to_categorical(y, num_classes=10)

# Dividiamo i dati in train e test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Creazione del modello
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Dropout(0.25),  # Spegne il 25% dei neuroni dopo il pooling

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),  # Spegne il 25% dei neuroni dopo il secondo blocco

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),  # Spegne il 50% dei neuroni nel layer denso
    Dense(10, activation='softmax')
])
# Compila il modello
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Addestramento
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.2)

# Valutazione
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Loss: {loss}, Accuracy: {accuracy}")


# Salva il modello
model.save('cnn_model.h5')
print("Modello salvato come digit_recognition_model.h5")

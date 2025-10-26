let isDrawing = false;
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

// Impostiamo le dimensioni dell'area di disegno
const canvasSize = 280; // Area di disegno è 280x280 pixel
const resizeSize = 28;  // Vogliamo ridurre l'immagine a 28x28 pixel

canvas.width = canvasSize;
canvas.height = canvasSize;

// Riempie il canvas con bianco
context.fillStyle = "white";
context.fillRect(0, 0, canvas.width, canvas.height);

// Impostiamo il colore del tratto a nero
context.strokeStyle = "black";

// Cambia lo spessore della linea quando viene modificato il valore dell'input
document.getElementById('lineWidthInput').addEventListener('input', (event) => {
    const lineWidth = parseInt(event.target.value, 10);
    if (!isNaN(lineWidth) && lineWidth > 0) {
        context.lineWidth = lineWidth; // Aggiorna lo spessore della linea
    }
});

// Gestione del disegno
canvas.addEventListener('mousedown', (event) => {
    isDrawing = true;
    context.beginPath(); // Inizia un nuovo percorso per il disegno
    draw(event);
});
canvas.addEventListener('mouseup', () => isDrawing = false);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseleave', () => isDrawing = false);

// Funzione per disegnare sul canvas
function draw(event) {
    if (!isDrawing) return;

    const x = event.offsetX;
    const y = event.offsetY;

    context.lineTo(x, y);  // Traccia una linea dal punto precedente
    context.stroke();      // Disegna la linea
    context.beginPath();   // Inizia un nuovo percorso per la linea successiva
    context.moveTo(x, y);  // Posiziona la penna dove è stato interrotto il disegno
}

// Funzione per riconoscere il numero (invio immagine base64 al server)
async function recognizeDigit() {
    const canvasData = canvas.toDataURL('image/png'); // Ottieni i dati del canvas come immagine base64

    // Prepara i dati da inviare al server
    const jsonData = JSON.stringify({ image_base64: canvasData });

    try {
        // Invia l'immagine al server
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: jsonData,
        });

        // Ricevi e mostra il risultato dal server
        const result = await response.json();

        if (result.predicted_class !== undefined) {
            document.getElementById('prediction').innerText = `Numero Riconosciuto: ${result.predicted_class}`;
        } else {
            document.getElementById('prediction').innerText = "Errore nella previsione";
        }
    } catch (error) {
        console.error("Errore durante la comunicazione con il server:", error);
        document.getElementById('prediction').innerText = "Errore nella previsione";
    }
}

// Funzione per pulire il canvas
function clearCanvas() {
    context.clearRect(0, 0, canvas.width, canvas.height);  // Pulisce il canvas
    context.fillStyle = "white";  // Imposta il colore di riempimento a bianco
    context.fillRect(0, 0, canvas.width, canvas.height); 
    document.getElementById('prediction').innerText = "?";  // Resetta il risultato
}

// Funzione per mostrare l'immagine ridimensionata
function showResizedCanvasImage() {
    const tempCanvas = document.createElement('canvas'); // Crea un canvas temporaneo
    const tempContext = tempCanvas.getContext('2d');
    tempCanvas.width = resizeSize;
    tempCanvas.height = resizeSize;

    // Disegniamo l'immagine ridimensionata sul canvas temporaneo
    tempContext.drawImage(canvas, 0, 0, resizeSize, resizeSize);

    // Otteniamo i dati dell'immagine ridimensionata in formato base64
    const imgData = tempCanvas.toDataURL('image/png');

    // Visualizziamo l'immagine in un elemento HTML
    const imgElement = document.getElementById('resizedImagePreview');
    imgElement.src = imgData;
}


// Funzione per salvare l'immagine 28x28
async function saveResizedImage() {
    const resizeSize = 28; // Dimensione desiderata
    const tempCanvas = document.createElement('canvas'); // Crea un canvas temporaneo
    const tempContext = tempCanvas.getContext('2d');
    tempCanvas.width = resizeSize;
    tempCanvas.height = resizeSize;

    

    // Disegniamo l'immagine ridimensionata sul canvas temporaneo
    tempContext.drawImage(canvas, 0, 0, resizeSize, resizeSize);

    // Otteniamo i dati dell'immagine ridimensionata in formato base64
    const imgData = tempCanvas.toDataURL('image/png');

    const target = document.getElementById('targetInput').value;
    const lineWidth = document.getElementById('lineWidthInput').value;

    // Salva i valori di Target e Line Width nel localStorage
    localStorage.setItem('savedTarget', target);
    localStorage.setItem('savedLineWidth', lineWidth);

    // Invia l'immagine al server per salvarla
    const response = await fetch('/save_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 

            image: imgData,
            target: target
        })
    });

    const result = await response.json();
    if (result.success) {
        alert('Immagine salvata con successo!');
        location.reload();

    } else {
        alert('Errore nel salvataggio dell\'immagine');
    }
}

window.addEventListener('DOMContentLoaded', () => {
    // Ripristina il valore del Target
    const savedTarget = localStorage.getItem('savedTarget');
    if (savedTarget) {
        document.getElementById('targetInput').value = savedTarget;
    }

    // Ripristina il valore dello spessore della linea
    const savedLineWidth = localStorage.getItem('savedLineWidth');
    if (savedLineWidth) {
        document.getElementById('lineWidthInput').value = savedLineWidth;
        context.lineWidth = parseInt(savedLineWidth, 10); // Aggiorna il contesto del canvas
    }
});

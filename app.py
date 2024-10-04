from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the pre-trained model
model = load_model('model/mnist_digit_recognizer.h5')

def preprocess_image(image, target_size):
    # Convert to grayscale
    image = image.convert('L')
    
    # Invert the colors if the image has white background and black digits
    image = Image.eval(image, lambda x: 255 - x)
    
    # Resize to 28x28 pixels
    image = image.resize((28, 28))
    
    # Convert to numpy array
    image = np.array(image)
    
    # Normalize pixel values to range [0, 1]
    image = image / 255.0
    
    # Reshape to (1, 28, 28, 1) for the model input
    image = image.reshape(1, 28, 28, 1)
    return image
    
    
    
    
    # image = image.convert("L")
    # image = image.resize(target_size)
    # image = np.array(image)
    # image = image / 255.0
    # image = image.reshape(1, 28, 28, 1)
    # return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file)

    processed_image = preprocess_image(image, target_size=(28, 28))

    predictions = model.predict(processed_image)
    predicted_digit = np.argmax(predictions)

    return jsonify({'digit': int(predicted_digit)})

if __name__ == '__main__':
    app.run(port=5000, debug=True)

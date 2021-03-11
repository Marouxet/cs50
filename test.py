# Test NN
import cv2
import numpy as np
import sys
import tensorflow as tf
import ast


IMG_WIDTH = 30
IMG_HEIGHT = 30


def load_img(path):

    images= (cv2.resize(cv2.imread(path)/255,(IMG_WIDTH,IMG_HEIGHT)))
    
    return images

# Dictionary to map every Label (1 to 42) to each String inicating the Label

def findSignal(prediction):

    file = open("keys.txt", "r")

    contents = file.read()
    dictionary = ast.literal_eval(contents)

    file.close()

    ubicacion = np.argmax(prediction)

    LabelsDict = {

    0:"Max 20 km/h",
    1:"Max 30 km/h",
    2:"Max 50 km/h",
    3:"Max 60 km/h",
    4:"Max 70 km/h",
    5:"Max 80 km/h",
    6:"End of Max 80 km/h",
    7:"Max 100 km/h",
    8:"Max 120 km/h",
    9:"Adelantarse c/ precaución ",
    10:"Adelantarse c/ precaución tránsito pesado",
    11: "Alien en el camino",
    12: "Rombo amarillo",
    13: "White signal (Triangular)",
    14: "STOP",
    15: "White Signal (Circle)",
    16: "Camion",
    17: "Contramano",
    18: "Attention Signal",
    19: "Turn left Signal - Routes",
    20: "Turn right Signal - Routes",
    21: "Camino Sinuoso",
    22: "Badén",
    23: "Peralte",
    24: "Reducción del camino",
    25: "Obras",
    26: "Semáforo",
    27: "Cruce peatonal",
    28: "Cruce de niños",
    29: "Bicicleta",
    30: "Hielo en el camino",
    31: "Animales sueltos",
    32: "Señal Tachada",
    33: "Curva a la derecha Urbana",
    34: "Curva a la izquierda, urbana",
    35: "Flecha hacia arriba",
    36: "Bifurcación Derecha",
    37: "Bifurcación Izquierda",
    38: "Indicación de Salida, Derecha",
    39: "Indicación de Salida, Izquierda", 
    40: "Rotonda",
    41: "No adelantarse",
    42: "No adelantarse tráfico pesado"
    }
    
    return LabelsDict[dictionary[ubicacion]]

def predict(image, model):
    prediction = model.predict(image, verbose=0)
    return prediction

def main():
     # Check command-line arguments
    if len(sys.argv) not in [2,3]:
        sys.exit("Usage: python run.py url")

    # Get image arrays and labels for all image files
    
    image= load_img(sys.argv[1])
    #image= load_img("stop.jpeg")
    cv2.imshow("Image", image)
    cv2.waitKey(2000)
    #Load Keras Model
    model = tf.keras.models.load_model(sys.argv[2])
    #model = tf.keras.models.load_model("model.h5")

    # Reshape Image to fit with imput model
    arrays = np.ndarray((1,IMG_WIDTH, IMG_HEIGHT,3))
    arrays[0] = image
    
    # Make Prediction
    prediction = predict(arrays, model)
    señal = findSignal(prediction)
    print(señal)

  
   



if __name__ == "__main__":
    main()

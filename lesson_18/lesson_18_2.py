import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"  # Включает старый режим Keras 2

from tf_keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input
import numpy as np

img_path = "../data/cat.png"
# img_path = "../data/dog.png"


img = image.load_img(img_path, target_size=(224, 224))

img_array = image.img_to_array(img)
img_batch = np.expand_dims(img_array, axis = 0)

from tensorflow.keras.applications.resnet50 import preprocess_input

img_preprocessed = preprocess_input(img_batch)

img = image.load_img(img_path, target_size=(224, 224))

model = load_model("../data/our_model.h5")

prediction = model.predict(img_preprocessed)

print(prediction)

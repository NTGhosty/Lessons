import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"  # Включает старый режим Keras 2

# 1. Загрузка изображения
# 2. Масштабирование
# 3. Нормализация
# 4. Выбор модели
# 5. Загрузка изображения в модель и получение предсказания

from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

img_path = "../data/dog.png"

img = image.load_img(img_path, target_size=(224, 224))

import numpy as np

# plt.imshow(img)
# plt.show()

img_array = image.img_to_array(img)
print(img_array.shape)

print(img_array[100, 100])

print(np.min(img_array))
print(np.max(img_array))

img_batch = np.expand_dims(img_array, axis=0)

from tensorflow.keras.applications.resnet50 import preprocess_input

img_preprocessed = preprocess_input(img_batch)
print(img_preprocessed.shape)

print(img_preprocessed[0, 100, 100])

print(np.min(img_preprocessed))
print(np.max(img_preprocessed))

from tensorflow.keras.applications.resnet50 import ResNet50

model = ResNet50()

prediction = model.predict(img_preprocessed)

from tensorflow.keras.applications.resnet50 import decode_predictions

print(decode_predictions(prediction))


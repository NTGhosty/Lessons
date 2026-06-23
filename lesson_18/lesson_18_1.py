import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"  # Включает старый режим Keras 2

# Название папок = название категории

TRAIN_DATA_DIR = "../data/train_data"
VALIDATION_DATA_DIR = "../data/val"
TRAIN_SAMPLES = 500
VALIDATION_SAMPLES = 500

# "кошка или собака" -> "кошка или НЕ кошка" - бинарная классификация
# "кошка или собака" - мультиклассовая классификация
NUM_CLASSES = 2

IMG_WIDTH = 224
IMG_HEIGHT = 224

# Сколько изображений модель при обучении принимает одновременно
BATCH_SIZE = 64

# Аугментация - процедура увеличения кол-ва данных путем их "искажения": повороты, сдвиги, масштабирования

from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input,
    Flatten,
    Dense,
    Dropout,
    GlobalAveragePooling2D,
)
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input
from tensorflow.keras.optimizers import Adam
import math

# Аугментация и Нормализация
train_datagen = image.ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=20, # 500 * 20 * 2 = 20 000
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
)
# Только нормализация
val_datagen = image.ImageDataGenerator(preprocessing_function=preprocess_input)

train_gen = train_datagen.flow_from_directory(
    TRAIN_DATA_DIR,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=1,
    class_mode="categorical",
)

val_gen = val_datagen.flow_from_directory(
    VALIDATION_DATA_DIR,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    shuffle=False,
    class_mode="categorical",
)

model = MobileNet(include_top = False, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))
for layer in model.layers[:]:
    layer.trainable = False

input = Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3))

custom_model = model(input)
custom_model = GlobalAveragePooling2D()(custom_model)
custom_model = Dense(64, activation="relu")(custom_model)
custom_model = Dropout(0.5)(custom_model)
prediction = Dense(NUM_CLASSES, activation="softmax")(custom_model)

target_model = Model(inputs=input, outputs=prediction)

target_model.compile(
    loss="categorical_crossentropy",
    optimizer=Adam(),
    metrics=["accuracy"]
)

num_steps = math.ceil(float(TRAIN_SAMPLES) / BATCH_SIZE)

target_model.fit(
    train_gen,
    steps_per_epoch=num_steps,
    epochs=7,
    validation_data=val_gen,
    validation_steps=num_steps,
)

print(val_gen.class_indices)

target_model.save("data/our_model.h5")

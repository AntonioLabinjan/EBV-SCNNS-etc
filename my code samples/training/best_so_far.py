from tensorflow import keras
from cnn2snn import check_model_compatibility, quantize, convert

# --- Load CIFAR-10 dataset ---
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
y_train = y_train.flatten()
y_test = y_test.flatten()

# --- Save raw test data for Akida runtime ---
raw_x_test = x_test.astype('uint8')
raw_y_test = y_test

# --- Rescale x-data ---
a, b = 255, 0
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train = (x_train - b) / a
x_test = (x_test - b) / a

# --- Data Augmentation ---
datagen = keras.preprocessing.image.ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True
)
datagen.fit(x_train)

# --- Keras model (optimized + Akida-compatible) ---
input_shape = x_train.shape[1:]  # (32,32,3)
model_keras = keras.models.Sequential([
    keras.layers.Conv2D(32, 3, strides=1, padding='same', input_shape=input_shape),
    keras.layers.BatchNormalization(),
    keras.layers.ReLU(),

    keras.layers.Conv2D(64, 3, strides=2, padding='same'),
    keras.layers.BatchNormalization(),
    keras.layers.ReLU(),

    keras.layers.Conv2D(128, 3, strides=2, padding='same'),
    keras.layers.BatchNormalization(),
    keras.layers.ReLU(),

    keras.layers.Flatten(),
    
    keras.layers.Dense(128),  # bez aktivacije
    keras.layers.BatchNormalization(),
    keras.layers.ReLU(),  # relu ide odvojeno, kao poseban sloj
    keras.layers.Dense(10)
    
], name='cifarnet_v2')

model_keras.summary()
print("Model compatible for Akida conversion:", check_model_compatibility(model_keras))

# --- Compile and train ---
lr_schedule = keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate=1e-3,
    decay_steps=10000,
    decay_rate=0.9
)
optimizer = keras.optimizers.Adam(learning_rate=lr_schedule)

model_keras.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=optimizer,
    metrics=['accuracy']
)

history = model_keras.fit(
    datagen.flow(x_train, y_train, batch_size=64),
    epochs=2, #40
    validation_data=(x_test, y_test)
)

score = model_keras.evaluate(x_test, y_test, verbose=0)
print('Test accuracy (before quantization):', score[1])

# --- Quantize ---
model_quantized = quantize(model_keras,
                           input_weight_quantization=8,
                           weight_quantization=4,
                           activ_quantization=4)
model_quantized.summary()

model_quantized.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer='adam',
    metrics=['accuracy']
)

score = model_quantized.evaluate(x_test, y_test, verbose=0)
print('Test accuracy after 8-4-4 quantization:', score[1])

# --- Fine-tune quantized model ---
model_quantized.fit(
    datagen.flow(x_train, y_train, batch_size=64),
    epochs=10,
    validation_data=(x_test, y_test)
)
score = model_quantized.evaluate(x_test, y_test, verbose=0)
print('Test accuracy after fine tuning:', score[1])

# --- Convert to Akida SNN ---
model_akida = convert(model_quantized, input_scaling=(a, b))
model_akida.summary()

raw_y_test_int32 = raw_y_test.astype('int32')
accuracy = model_akida.evaluate(raw_x_test, raw_y_test_int32)
print('Test accuracy after Akida conversion:', accuracy)

'''

Model: "cifarnet_v2"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 conv2d (Conv2D)             (None, 32, 32, 32)        896

 batch_normalization (Batch  (None, 32, 32, 32)        128
 Normalization)

 re_lu (ReLU)                (None, 32, 32, 32)        0

 conv2d_1 (Conv2D)           (None, 16, 16, 64)        18496

 batch_normalization_1 (Bat  (None, 16, 16, 64)        256
 chNormalization)

 re_lu_1 (ReLU)              (None, 16, 16, 64)        0

 conv2d_2 (Conv2D)           (None, 8, 8, 128)         73856

 batch_normalization_2 (Bat  (None, 8, 8, 128)         512
 chNormalization)

 re_lu_2 (ReLU)              (None, 8, 8, 128)         0

 flatten (Flatten)           (None, 8192)              0

 dense (Dense)               (None, 128)               1048704

 batch_normalization_3 (Bat  (None, 128)               512
 chNormalization)

 re_lu_3 (ReLU)              (None, 128)               0

 dense_1 (Dense)             (None, 10)                1290

=================================================================
Total params: 1144650 (4.37 MB)
Trainable params: 1143946 (4.36 MB)
Non-trainable params: 704 (2.75 KB)
_________________________________________________________________
1/1 [==============================] - 1s 581ms/step
Model compatible for Akida conversion: None
Epoch 1/2
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\utils\tf_utils.py:492: The name tf.ragged.RaggedTensorValue is deprecated. Please use tf.compat.v1.ragged.RaggedTensorValue instead.

WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\engine\base_layer_utils.py:384: The name tf.executing_eagerly_outside_functions is deprecated. Please use tf.compat.v1.executing_eagerly_outside_functions instead.

782/782 [==============================] - 156s 194ms/step - loss: 1.3539 - accuracy: 0.5110 - val_loss: 1.2989 - val_accuracy: 0.5457
Epoch 2/2
782/782 [==============================] - 150s 192ms/step - loss: 1.0229 - accuracy: 0.6370 - val_loss: 1.0594 - val_accuracy: 0.6271
Test accuracy (before quantization): 0.6270999908447266
Model: "sequential_1"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 conv2d (QuantizedConv2D)    (None, 32, 32, 32)        896

 re_lu (QuantizedReLU)       (None, 32, 32, 32)        0

 conv2d_1 (QuantizedConv2D)  (None, 16, 16, 64)        18496

 re_lu_1 (QuantizedReLU)     (None, 16, 16, 64)        0

 conv2d_2 (QuantizedConv2D)  (None, 8, 8, 128)         73856

 re_lu_2 (QuantizedReLU)     (None, 8, 8, 128)         0

 flatten (Flatten)           (None, 8192)              0

 dense (QuantizedDense)      (None, 128)               1048704

 re_lu_3 (QuantizedReLU)     (None, 128)               0

 dense_1 (QuantizedDense)    (None, 10)                1290

=================================================================
Total params: 1143242 (4.36 MB)
Trainable params: 1143242 (4.36 MB)
Non-trainable params: 0 (0.00 Byte)
_________________________________________________________________
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\optimizers\__init__.py:309: The name tf.train.Optimizer is deprecated. Please use tf.compat.v1.train.Optimizer instead.

Test accuracy after 8-4-4 quantization: 0.6021999716758728
Epoch 1/10
782/782 [==============================] - 194s 242ms/step - loss: 1.1109 - accuracy: 0.6093 - val_loss: 1.0111 - val_accuracy: 0.6532
Epoch 2/10
782/782 [==============================] - 196s 251ms/step - loss: 0.9623 - accuracy: 0.6630 - val_loss: 0.9271 - val_accuracy: 0.6855
Epoch 3/10
782/782 [==============================] - 184s 235ms/step - loss: 0.8963 - accuracy: 0.6847 - val_loss: 0.8517 - val_accuracy: 0.7042
Epoch 4/10
782/782 [==============================] - 184s 236ms/step - loss: 0.8564 - accuracy: 0.6988 - val_loss: 0.8345 - val_accuracy: 0.7123
Epoch 5/10
782/782 [==============================] - 195s 249ms/step - loss: 0.8131 - accuracy: 0.7134 - val_loss: 0.8089 - val_accuracy: 0.7267
Epoch 6/10
782/782 [==============================] - 225s 288ms/step - loss: 0.7899 - accuracy: 0.7217 - val_loss: 0.8073 - val_accuracy: 0.7225
Epoch 7/10
782/782 [==============================] - 232s 297ms/step - loss: 0.7583 - accuracy: 0.7315 - val_loss: 0.8114 - val_accuracy: 0.7208
Epoch 8/10
782/782 [==============================] - 230s 294ms/step - loss: 0.7416 - accuracy: 0.7389 - val_loss: 0.8040 - val_accuracy: 0.7304
Epoch 9/10
782/782 [==============================] - 233s 298ms/step - loss: 0.7192 - accuracy: 0.7466 - val_loss: 0.7861 - val_accuracy: 0.7374
Epoch 10/10
782/782 [==============================] - 229s 292ms/step - loss: 0.7042 - accuracy: 0.7534 - val_loss: 0.7768 - val_accuracy: 0.7420
Test accuracy after fine tuning: 0.7419999837875366
                Model Summary
______________________________________________
Input shape  Output shape  Sequences  Layers
==============================================
[32, 32, 3]  [1, 1, 10]    1          5
______________________________________________

______________________________________________________
Layer (type)         Output shape  Kernel shape

============ SW/conv2d-dense_1 (Software) ============

conv2d (InputConv.)  [32, 32, 32]  (3, 3, 3, 32)
______________________________________________________
conv2d_1 (Conv.)     [16, 16, 64]  (3, 3, 32, 64)
______________________________________________________
conv2d_2 (Conv.)     [8, 8, 128]   (3, 3, 64, 128)
______________________________________________________
dense (Fully.)       [1, 1, 128]   (1, 1, 8192, 128)
______________________________________________________
dense_1 (Fully.)     [1, 1, 10]    (1, 1, 128, 10)
______________________________________________________
Test accuracy after Akida conversion: 0.7402999997138977
'''

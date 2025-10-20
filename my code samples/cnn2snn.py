from tensorflow import keras

# --- Load MNIST dataset ---
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Reshape x-data
x_train = x_train.reshape(60000, 28, 28, 1)
x_test = x_test.reshape(10000, 28, 28, 1)

# Set aside raw test data for Akida runtime
raw_x_test = x_test.astype('uint8')
raw_y_test = y_test

# Rescale x-data
a = 255
b = 0
input_scaling = (a, b)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train = (x_train - b) / a
x_test = (x_test - b) / a

# --- Keras model compatible with BrainChip ---
model_keras = keras.models.Sequential([
    keras.layers.Conv2D(filters=32, kernel_size=3, strides=2, input_shape=(28,28,1)),
    keras.layers.BatchNormalization(),
    keras.layers.ReLU(),
    keras.layers.Conv2D(filters=64, kernel_size=3, strides=2, padding='same'),
    keras.layers.BatchNormalization(),
    keras.layers.ReLU(),
    keras.layers.Flatten(),
    keras.layers.Dense(10)
], name='mnistnet')

model_keras.summary()

from cnn2snn import check_model_compatibility, quantize, convert

print("Model compatible for Akida conversion:", check_model_compatibility(model_keras))

model_keras.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer='adam',
    metrics=['accuracy']
)

model_keras.fit(x_train, y_train, epochs=10, validation_split=0.1)

score = model_keras.evaluate(x_test, y_test, verbose=0)
print('Test accuracy:', score[1])

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

model_quantized.fit(x_train, y_train, epochs=5, validation_split=0.1)

score = model_quantized.evaluate(x_test, y_test, verbose=0)
print('Test accuracy after fine tuning:', score[1])

# --- Convert to Akida SNN ---
model_akida = convert(model_quantized, input_scaling=input_scaling)
model_akida.summary()
raw_y_test_int32 = raw_y_test.astype('int32')

accuracy = model_akida.evaluate(raw_x_test, raw_y_test_int32)
print('Test accuracy after conversion:', accuracy)

'''
Test accuracy after fine tuning: 0.9829000234603882
                Model Summary
______________________________________________
Input shape  Output shape  Sequences  Layers
==============================================
[28, 28, 1]  [1, 1, 10]    1          3
______________________________________________

_____________________________________________________
Layer (type)         Output shape  Kernel shape

============= SW/conv2d-dense (Software) ============

conv2d (InputConv.)  [13, 13, 32]  (3, 3, 1, 32)
_____________________________________________________
conv2d_1 (Conv.)     [7, 7, 64]    (3, 3, 32, 64)
_____________________________________________________
dense (Fully.)       [1, 1, 10]    (1, 1, 3136, 10)
_____________________________________________________
Test accuracy after conversion: 0.9829000234603882
'''

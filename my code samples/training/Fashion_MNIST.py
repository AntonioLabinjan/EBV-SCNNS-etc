from tensorflow import keras

# --- Load FASHION-MNIST dataset ---
(x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()

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
], name='fashionnet')

model_keras.summary()

from cnn2snn import check_model_compatibility, quantize, convert

print("Model compatible for Akida conversion:", check_model_compatibility(model_keras))

model_keras.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer='adam',
    metrics=['accuracy']
)

# Treniraj dulje jer je FashionMNIST teži od običnog MNIST-a
model_keras.fit(x_train, y_train, epochs=15, validation_split=0.1)

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

# Fine-tune kvantizirani model
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
(brainchip) C:\Users\Korisnik\Desktop\cnn2snnTEST>python mnist_brainchip.py
2025-10-21 09:13:47.769001: I tensorflow/core/util/port.cc:113] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\losses.py:2976: The name tf.losses.sparse_softmax_cross_entropy is deprecated. Please use tf.compat.v1.losses.sparse_softmax_cross_entropy instead.

WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\backend.py:873: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.

2025-10-21 09:14:02.598029: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE SSE2 SSE3 SSE4.1 SSE4.2 AVX2 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\layers\normalization\batch_normalization.py:979: The name tf.nn.fused_batch_norm is deprecated. Please use tf.compat.v1.nn.fused_batch_norm instead.

Model: "fashionnet"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 conv2d (Conv2D)             (None, 13, 13, 32)        320

 batch_normalization (Batch  (None, 13, 13, 32)        128
 Normalization)

 re_lu (ReLU)                (None, 13, 13, 32)        0

 conv2d_1 (Conv2D)           (None, 7, 7, 64)          18496

 batch_normalization_1 (Bat  (None, 7, 7, 64)          256
 chNormalization)

 re_lu_1 (ReLU)              (None, 7, 7, 64)          0

 flatten (Flatten)           (None, 3136)              0

 dense (Dense)               (None, 10)                31370

=================================================================
Total params: 50570 (197.54 KB)
Trainable params: 50378 (196.79 KB)
Non-trainable params: 192 (768.00 Byte)
_________________________________________________________________
C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\onnxscript\converter.py:816: FutureWarning: 'onnxscript.values.Op.param_schemas' is deprecated in version 0.1 and will be removed in the future. Please use '.op_signature' instead.
  param_schemas = callee.param_schemas()
1/1 [==============================] - 0s 388ms/step
Model compatible for Akida conversion: None
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\optimizers\__init__.py:309: The name tf.train.Optimizer is deprecated. Please use tf.compat.v1.train.Optimizer instead.

Epoch 1/15
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\utils\tf_utils.py:492: The name tf.ragged.RaggedTensorValue is deprecated. Please use tf.compat.v1.ragged.RaggedTensorValue instead.

WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\engine\base_layer_utils.py:384: The name tf.executing_eagerly_outside_functions is deprecated. Please use tf.compat.v1.executing_eagerly_outside_functions instead.

1688/1688 [==============================] - 34s 18ms/step - loss: 0.4205 - accuracy: 0.8495 - val_loss: 0.4194 - val_accuracy: 0.8487
Epoch 2/15
1688/1688 [==============================] - 27s 16ms/step - loss: 0.2885 - accuracy: 0.8950 - val_loss: 0.3129 - val_accuracy: 0.8875
Epoch 3/15
1688/1688 [==============================] - 30s 18ms/step - loss: 0.2479 - accuracy: 0.9106 - val_loss: 0.2960 - val_accuracy: 0.8937
Epoch 4/15
1688/1688 [==============================] - 25s 15ms/step - loss: 0.2185 - accuracy: 0.9199 - val_loss: 0.2815 - val_accuracy: 0.8982
Epoch 5/15
1688/1688 [==============================] - 28s 17ms/step - loss: 0.1956 - accuracy: 0.9291 - val_loss: 0.2848 - val_accuracy: 0.8975
Epoch 6/15
1688/1688 [==============================] - 29s 17ms/step - loss: 0.1763 - accuracy: 0.9361 - val_loss: 0.2961 - val_accuracy: 0.9012
Epoch 7/15
1688/1688 [==============================] - 28s 16ms/step - loss: 0.1604 - accuracy: 0.9406 - val_loss: 0.2912 - val_accuracy: 0.8993
Epoch 8/15
1688/1688 [==============================] - 28s 16ms/step - loss: 0.1471 - accuracy: 0.9475 - val_loss: 0.3448 - val_accuracy: 0.8800
Epoch 9/15
1688/1688 [==============================] - 27s 16ms/step - loss: 0.1361 - accuracy: 0.9506 - val_loss: 0.3145 - val_accuracy: 0.8992
Epoch 10/15
1688/1688 [==============================] - 28s 17ms/step - loss: 0.1243 - accuracy: 0.9559 - val_loss: 0.3141 - val_accuracy: 0.8987
Epoch 11/15
1688/1688 [==============================] - 27s 16ms/step - loss: 0.1141 - accuracy: 0.9594 - val_loss: 0.3187 - val_accuracy: 0.9073
Epoch 12/15
1688/1688 [==============================] - 26s 16ms/step - loss: 0.1059 - accuracy: 0.9619 - val_loss: 0.3355 - val_accuracy: 0.8952
Epoch 13/15
1688/1688 [==============================] - 28s 16ms/step - loss: 0.0986 - accuracy: 0.9646 - val_loss: 0.3812 - val_accuracy: 0.8870
Epoch 14/15
1688/1688 [==============================] - 27s 16ms/step - loss: 0.0911 - accuracy: 0.9673 - val_loss: 0.3619 - val_accuracy: 0.8977
Epoch 15/15
1688/1688 [==============================] - 26s 15ms/step - loss: 0.0850 - accuracy: 0.9698 - val_loss: 0.3717 - val_accuracy: 0.8967
Test accuracy: 0.9028000235557556
Model: "sequential_1"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 conv2d (QuantizedConv2D)    (None, 13, 13, 32)        320

 re_lu (QuantizedReLU)       (None, 13, 13, 32)        0

 conv2d_1 (QuantizedConv2D)  (None, 7, 7, 64)          18496

 re_lu_1 (QuantizedReLU)     (None, 7, 7, 64)          0

 flatten (Flatten)           (None, 3136)              0

 dense (QuantizedDense)      (None, 10)                31370

=================================================================
Total params: 50186 (196.04 KB)
Trainable params: 50186 (196.04 KB)
Non-trainable params: 0 (0.00 Byte)
_________________________________________________________________
Test accuracy after 8-4-4 quantization: 0.6699000000953674
Epoch 1/5
1688/1688 [==============================] - 32s 16ms/step - loss: 0.2106 - accuracy: 0.9305 - val_loss: 0.5158 - val_accuracy: 0.8832
Epoch 2/5
1688/1688 [==============================] - 28s 16ms/step - loss: 0.1876 - accuracy: 0.9376 - val_loss: 0.5153 - val_accuracy: 0.8885
Epoch 3/5
1688/1688 [==============================] - 29s 17ms/step - loss: 0.1788 - accuracy: 0.9408 - val_loss: 0.5320 - val_accuracy: 0.8843
Epoch 4/5
1688/1688 [==============================] - 28s 16ms/step - loss: 0.1707 - accuracy: 0.9426 - val_loss: 0.5113 - val_accuracy: 0.8872
Epoch 5/5
1688/1688 [==============================] - 28s 17ms/step - loss: 0.1687 - accuracy: 0.9424 - val_loss: 0.5443 - val_accuracy: 0.8815
Test accuracy after fine tuning: 0.8747000098228455
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
Test accuracy after conversion: 0.8744000196456909
'''

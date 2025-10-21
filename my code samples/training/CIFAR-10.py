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

# --- Keras model compatible with BrainChip ---
input_shape = x_train.shape[1:]  # (32,32,3)
model_keras = keras.models.Sequential([
    keras.layers.Conv2D(32, kernel_size=3, strides=2, input_shape=input_shape),
    keras.layers.BatchNormalization(),
    keras.layers.ReLU(),
    keras.layers.Conv2D(64, kernel_size=3, strides=2, padding='same'),
    keras.layers.BatchNormalization(),
    keras.layers.ReLU(),
    keras.layers.Flatten(),
    keras.layers.Dense(10)
], name='cifarnet')

model_keras.summary()
print("Model compatible for Akida conversion:", check_model_compatibility(model_keras))

# --- Compile and train ---
model_keras.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer='adam',
    metrics=['accuracy']
)
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

# --- Fine-tune quantized model ---
model_quantized.fit(x_train, y_train, epochs=5, validation_split=0.1)
score = model_quantized.evaluate(x_test, y_test, verbose=0)
print('Test accuracy after fine tuning:', score[1])

# --- Convert to Akida SNN ---
model_akida = convert(model_quantized, input_scaling=(a, b))
model_akida.summary()

raw_y_test_int32 = raw_y_test.astype('int32')
accuracy = model_akida.evaluate(raw_x_test, raw_y_test_int32)
print('Test accuracy after conversion:', accuracy)

'''
(brainchip) C:\Users\Korisnik\Desktop\cnn2snnTEST>python mnist_brainchip.py
2025-10-21 11:19:38.664606: I tensorflow/core/util/port.cc:113] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\losses.py:2976: The name tf.losses.sparse_softmax_cross_entropy is deprecated. Please use tf.compat.v1.losses.sparse_softmax_cross_entropy instead.

2025-10-21 11:19:53.229965: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE SSE2 SSE3 SSE4.1 SSE4.2 AVX2 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\onnxscript\converter.py:816: FutureWarning: 'onnxscript.values.Op.param_schemas' is deprecated in version 0.1 and will be removed in the future. Please use '.op_signature' instead.
  param_schemas = callee.param_schemas()
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\backend.py:873: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.

WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\layers\normalization\batch_normalization.py:979: The name tf.nn.fused_batch_norm is deprecated. Please use tf.compat.v1.nn.fused_batch_norm instead.

Model: "cifarnet"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 conv2d (Conv2D)             (None, 15, 15, 32)        896

 batch_normalization (Batch  (None, 15, 15, 32)        128
 Normalization)

 re_lu (ReLU)                (None, 15, 15, 32)        0

 conv2d_1 (Conv2D)           (None, 8, 8, 64)          18496

 batch_normalization_1 (Bat  (None, 8, 8, 64)          256
 chNormalization)

 re_lu_1 (ReLU)              (None, 8, 8, 64)          0

 flatten (Flatten)           (None, 4096)              0

 dense (Dense)               (None, 10)                40970

=================================================================
Total params: 60746 (237.29 KB)
Trainable params: 60554 (236.54 KB)
Non-trainable params: 192 (768.00 Byte)
_________________________________________________________________
1/1 [==============================] - 0s 397ms/step
Model compatible for Akida conversion: None
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\optimizers\__init__.py:309: The name tf.train.Optimizer is deprecated. Please use tf.compat.v1.train.Optimizer instead.

Epoch 1/15
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\utils\tf_utils.py:492: The name tf.ragged.RaggedTensorValue is deprecated. Please use tf.compat.v1.ragged.RaggedTensorValue instead.

WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\engine\base_layer_utils.py:384: The name tf.executing_eagerly_outside_functions is deprecated. Please use tf.compat.v1.executing_eagerly_outside_functions instead.

1407/1407 [==============================] - 32s 21ms/step - loss: 1.4402 - accuracy: 0.4941 - val_loss: 1.2755 - val_accuracy: 0.5540
Epoch 2/15
1407/1407 [==============================] - 30s 21ms/step - loss: 1.0795 - accuracy: 0.6204 - val_loss: 1.1345 - val_accuracy: 0.6044
Epoch 3/15
1407/1407 [==============================] - 27s 19ms/step - loss: 0.9374 - accuracy: 0.6730 - val_loss: 1.1052 - val_accuracy: 0.6142
Epoch 4/15
1407/1407 [==============================] - 30s 21ms/step - loss: 0.8458 - accuracy: 0.7065 - val_loss: 1.1371 - val_accuracy: 0.6206
Epoch 5/15
1407/1407 [==============================] - 27s 19ms/step - loss: 0.7744 - accuracy: 0.7306 - val_loss: 1.0842 - val_accuracy: 0.6396
Epoch 6/15
1407/1407 [==============================] - 28s 20ms/step - loss: 0.7097 - accuracy: 0.7526 - val_loss: 1.0234 - val_accuracy: 0.6600
Epoch 7/15
1407/1407 [==============================] - 29s 21ms/step - loss: 0.6576 - accuracy: 0.7729 - val_loss: 1.1898 - val_accuracy: 0.6192
Epoch 8/15
1407/1407 [==============================] - 28s 20ms/step - loss: 0.6116 - accuracy: 0.7864 - val_loss: 1.0661 - val_accuracy: 0.6594
Epoch 9/15
1407/1407 [==============================] - 29s 21ms/step - loss: 0.5718 - accuracy: 0.8013 - val_loss: 1.1265 - val_accuracy: 0.6482
Epoch 10/15
1407/1407 [==============================] - 28s 20ms/step - loss: 0.5381 - accuracy: 0.8134 - val_loss: 1.1389 - val_accuracy: 0.6536
Epoch 11/15
1407/1407 [==============================] - 28s 20ms/step - loss: 0.5042 - accuracy: 0.8238 - val_loss: 1.0943 - val_accuracy: 0.6714
Epoch 12/15
1407/1407 [==============================] - 27s 19ms/step - loss: 0.4744 - accuracy: 0.8348 - val_loss: 1.2285 - val_accuracy: 0.6410
Epoch 13/15
1407/1407 [==============================] - 29s 21ms/step - loss: 0.4473 - accuracy: 0.8421 - val_loss: 1.2369 - val_accuracy: 0.6458
Epoch 14/15
1407/1407 [==============================] - 29s 20ms/step - loss: 0.4258 - accuracy: 0.8496 - val_loss: 1.3305 - val_accuracy: 0.6430
Epoch 15/15
1407/1407 [==============================] - 30s 21ms/step - loss: 0.4048 - accuracy: 0.8567 - val_loss: 1.2907 - val_accuracy: 0.6450
Test accuracy: 0.6363000273704529
Model: "sequential_1"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 conv2d (QuantizedConv2D)    (None, 15, 15, 32)        896

 re_lu (QuantizedReLU)       (None, 15, 15, 32)        0

 conv2d_1 (QuantizedConv2D)  (None, 8, 8, 64)          18496

 re_lu_1 (QuantizedReLU)     (None, 8, 8, 64)          0

 flatten (Flatten)           (None, 4096)              0

 dense (QuantizedDense)      (None, 10)                40970

=================================================================
Total params: 60362 (235.79 KB)
Trainable params: 60362 (235.79 KB)
Non-trainable params: 0 (0.00 Byte)
_________________________________________________________________
Test accuracy after 8-4-4 quantization: 0.5590999722480774
Epoch 1/5
1407/1407 [==============================] - 36s 23ms/step - loss: 0.8600 - accuracy: 0.7332 - val_loss: 1.7267 - val_accuracy: 0.6020
Epoch 2/5
1407/1407 [==============================] - 32s 23ms/step - loss: 0.7974 - accuracy: 0.7509 - val_loss: 1.7442 - val_accuracy: 0.6110
Epoch 3/5
1407/1407 [==============================] - 32s 22ms/step - loss: 0.7726 - accuracy: 0.7546 - val_loss: 1.7126 - val_accuracy: 0.6146
Epoch 4/5
1407/1407 [==============================] - 32s 23ms/step - loss: 0.7281 - accuracy: 0.7669 - val_loss: 1.7547 - val_accuracy: 0.6226
Epoch 5/5
1407/1407 [==============================] - 31s 22ms/step - loss: 0.7228 - accuracy: 0.7710 - val_loss: 1.7711 - val_accuracy: 0.6256
Test accuracy after fine tuning: 0.6065999865531921
                Model Summary
______________________________________________
Input shape  Output shape  Sequences  Layers
==============================================
[32, 32, 3]  [1, 1, 10]    1          3
______________________________________________

_____________________________________________________
Layer (type)         Output shape  Kernel shape

============= SW/conv2d-dense (Software) ============

conv2d (InputConv.)  [15, 15, 32]  (3, 3, 3, 32)
_____________________________________________________
conv2d_1 (Conv.)     [8, 8, 64]    (3, 3, 32, 64)
_____________________________________________________
dense (Fully.)       [1, 1, 10]    (1, 1, 4096, 10)
_____________________________________________________
Test accuracy after conversion: 0.6065999865531921
'''

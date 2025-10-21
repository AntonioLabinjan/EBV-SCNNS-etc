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

''' MNIST
(brainchip) C:\Users\Korisnik\Desktop\cnn2snnTEST>python mnist_brainchip.py
2025-10-21 08:53:26.444075: I tensorflow/core/util/port.cc:113] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\losses.py:2976: The name tf.losses.sparse_softmax_cross_entropy is deprecated. Please use tf.compat.v1.losses.sparse_softmax_cross_entropy instead.

WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\backend.py:873: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.

2025-10-21 08:53:41.009693: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE SSE2 SSE3 SSE4.1 SSE4.2 AVX2 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\layers\normalization\batch_normalization.py:979: The name tf.nn.fused_batch_norm is deprecated. Please use tf.compat.v1.nn.fused_batch_norm instead.

Model: "mnistnet"
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
1/1 [==============================] - 0s 337ms/step
Model compatible for Akida conversion: None
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\optimizers\__init__.py:309: The name tf.train.Optimizer is deprecated. Please use tf.compat.v1.train.Optimizer instead.

Epoch 1/10
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\utils\tf_utils.py:492: The name tf.ragged.RaggedTensorValue is deprecated. Please use tf.compat.v1.ragged.RaggedTensorValue instead.

WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\engine\base_layer_utils.py:384: The name tf.executing_eagerly_outside_functions is deprecated. Please use tf.compat.v1.executing_eagerly_outside_functions instead.

1688/1688 [==============================] - 29s 15ms/step - loss: 0.1470 - accuracy: 0.9547 - val_loss: 0.0918 - val_accuracy: 0.9752
Epoch 2/10
1688/1688 [==============================] - 26s 16ms/step - loss: 0.0626 - accuracy: 0.9803 - val_loss: 0.0551 - val_accuracy: 0.9865
Epoch 3/10
1688/1688 [==============================] - 29s 17ms/step - loss: 0.0433 - accuracy: 0.9862 - val_loss: 0.0537 - val_accuracy: 0.9867
Epoch 4/10
1688/1688 [==============================] - 25s 15ms/step - loss: 0.0341 - accuracy: 0.9894 - val_loss: 0.0591 - val_accuracy: 0.9835
Epoch 5/10
1688/1688 [==============================] - 27s 16ms/step - loss: 0.0258 - accuracy: 0.9918 - val_loss: 0.0611 - val_accuracy: 0.9862
Epoch 6/10
1688/1688 [==============================] - 29s 17ms/step - loss: 0.0207 - accuracy: 0.9933 - val_loss: 0.0591 - val_accuracy: 0.9865
Epoch 7/10
1688/1688 [==============================] - 28s 16ms/step - loss: 0.0162 - accuracy: 0.9947 - val_loss: 0.0565 - val_accuracy: 0.9868
Epoch 8/10
1688/1688 [==============================] - 26s 15ms/step - loss: 0.0137 - accuracy: 0.9953 - val_loss: 0.0521 - val_accuracy: 0.9875
Epoch 9/10
1688/1688 [==============================] - 26s 15ms/step - loss: 0.0109 - accuracy: 0.9963 - val_loss: 0.0536 - val_accuracy: 0.9878
Epoch 10/10
1688/1688 [==============================] - 26s 15ms/step - loss: 0.0092 - accuracy: 0.9967 - val_loss: 0.0961 - val_accuracy: 0.9798
Test accuracy: 0.9804999828338623
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
Test accuracy after 8-4-4 quantization: 0.8414000272750854
Epoch 1/5
1688/1688 [==============================] - 30s 16ms/step - loss: 0.0210 - accuracy: 0.9928 - val_loss: 0.0756 - val_accuracy: 0.9858
Epoch 2/5
1688/1688 [==============================] - 28s 17ms/step - loss: 0.0137 - accuracy: 0.9951 - val_loss: 0.0739 - val_accuracy: 0.9862
Epoch 3/5
1688/1688 [==============================] - 27s 16ms/step - loss: 0.0118 - accuracy: 0.9956 - val_loss: 0.0686 - val_accuracy: 0.9885
Epoch 4/5
1688/1688 [==============================] - 29s 17ms/step - loss: 0.0134 - accuracy: 0.9954 - val_loss: 0.0757 - val_accuracy: 0.9872
Epoch 5/5
1688/1688 [==============================] - 30s 18ms/step - loss: 0.0111 - accuracy: 0.9961 - val_loss: 0.0803 - val_accuracy: 0.9872
Test accuracy after fine tuning: 0.9853000044822693
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
Test accuracy after conversion: 0.9850000143051147


'''

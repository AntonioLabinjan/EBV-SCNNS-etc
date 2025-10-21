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
    epochs=50,
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
    epochs=15, # ovo je dodatni fitting modela; dovoljno je manje epoha nego u prvoj
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
(brainchip) C:\Users\Korisnik\Desktop\cnn2snnTEST>python mnist_brainchip.py
2025-10-21 19:42:04.312369: I tensorflow/core/util/port.cc:113] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\losses.py:2976: The name tf.losses.sparse_softmax_cross_entropy is deprecated. Please use tf.compat.v1.losses.sparse_softmax_cross_entropy instead.

2025-10-21 19:42:21.149462: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE SSE2 SSE3 SSE4.1 SSE4.2 AVX2 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\onnxscript\converter.py:816: FutureWarning: 'onnxscript.values.Op.param_schemas' is deprecated in version 0.1 and will be removed in the future. Please use '.op_signature' instead.
  param_schemas = callee.param_schemas()
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\backend.py:873: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.

WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\layers\normalization\batch_normalization.py:979: The name tf.nn.fused_batch_norm is deprecated. Please use tf.compat.v1.nn.fused_batch_norm instead.

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
1/1 [==============================] - 1s 903ms/step
Model compatible for Akida conversion: None
Epoch 1/50
WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\utils\tf_utils.py:492: The name tf.ragged.RaggedTensorValue is deprecated. Please use tf.compat.v1.ragged.RaggedTensorValue instead.

WARNING:tensorflow:From C:\Users\Korisnik\miniconda3\envs\brainchip\lib\site-packages\keras\src\engine\base_layer_utils.py:384: The name tf.executing_eagerly_outside_functions is deprecated. Please use tf.compat.v1.executing_eagerly_outside_functions instead.

782/782 [==============================] - 165s 204ms/step - loss: 1.3678 - accuracy: 0.5070 - val_loss: 2.6271 - val_accuracy: 0.3471
Epoch 2/50
782/782 [==============================] - 145s 185ms/step - loss: 1.0420 - accuracy: 0.6316 - val_loss: 0.9249 - val_accuracy: 0.6755
Epoch 3/50
782/782 [==============================] - 145s 185ms/step - loss: 0.9078 - accuracy: 0.6790 - val_loss: 1.0337 - val_accuracy: 0.6496
Epoch 4/50
782/782 [==============================] - 143s 183ms/step - loss: 0.8201 - accuracy: 0.7103 - val_loss: 0.9964 - val_accuracy: 0.6668
Epoch 5/50
782/782 [==============================] - 148s 189ms/step - loss: 0.7673 - accuracy: 0.7326 - val_loss: 0.9107 - val_accuracy: 0.6936
Epoch 6/50
782/782 [==============================] - 146s 187ms/step - loss: 0.7202 - accuracy: 0.7475 - val_loss: 0.9728 - val_accuracy: 0.6726
Epoch 7/50
782/782 [==============================] - 143s 183ms/step - loss: 0.6838 - accuracy: 0.7588 - val_loss: 0.7766 - val_accuracy: 0.7298
Epoch 8/50
782/782 [==============================] - 144s 184ms/step - loss: 0.6569 - accuracy: 0.7695 - val_loss: 0.7879 - val_accuracy: 0.7299
Epoch 9/50
782/782 [==============================] - 140s 179ms/step - loss: 0.6296 - accuracy: 0.7786 - val_loss: 0.7346 - val_accuracy: 0.7493
Epoch 10/50
782/782 [==============================] - 141s 180ms/step - loss: 0.6044 - accuracy: 0.7891 - val_loss: 0.7317 - val_accuracy: 0.7538
Epoch 11/50
782/782 [==============================] - 143s 182ms/step - loss: 0.5878 - accuracy: 0.7957 - val_loss: 0.9627 - val_accuracy: 0.7024
Epoch 12/50
782/782 [==============================] - 139s 178ms/step - loss: 0.5629 - accuracy: 0.8034 - val_loss: 0.6008 - val_accuracy: 0.7987
Epoch 13/50
782/782 [==============================] - 147s 188ms/step - loss: 0.5490 - accuracy: 0.8073 - val_loss: 0.7606 - val_accuracy: 0.7554
Epoch 14/50
782/782 [==============================] - 141s 180ms/step - loss: 0.5353 - accuracy: 0.8122 - val_loss: 0.8461 - val_accuracy: 0.7212
Epoch 15/50
782/782 [==============================] - 140s 179ms/step - loss: 0.5196 - accuracy: 0.8185 - val_loss: 0.6753 - val_accuracy: 0.7725
Epoch 16/50
782/782 [==============================] - 142s 182ms/step - loss: 0.5038 - accuracy: 0.8235 - val_loss: 0.5613 - val_accuracy: 0.8138
Epoch 17/50
782/782 [==============================] - 140s 178ms/step - loss: 0.4892 - accuracy: 0.8303 - val_loss: 0.6319 - val_accuracy: 0.7871
Epoch 18/50
782/782 [==============================] - 143s 183ms/step - loss: 0.4787 - accuracy: 0.8322 - val_loss: 0.6269 - val_accuracy: 0.7917
Epoch 19/50
782/782 [==============================] - 148s 190ms/step - loss: 0.4717 - accuracy: 0.8358 - val_loss: 0.7027 - val_accuracy: 0.7684
Epoch 20/50
782/782 [==============================] - 145s 186ms/step - loss: 0.4595 - accuracy: 0.8385 - val_loss: 0.6175 - val_accuracy: 0.7992
Epoch 21/50
782/782 [==============================] - 142s 181ms/step - loss: 0.4506 - accuracy: 0.8416 - val_loss: 0.7059 - val_accuracy: 0.7846
Epoch 22/50
782/782 [==============================] - 141s 180ms/step - loss: 0.4414 - accuracy: 0.8447 - val_loss: 0.6423 - val_accuracy: 0.7885
Epoch 23/50
782/782 [==============================] - 140s 178ms/step - loss: 0.4331 - accuracy: 0.8471 - val_loss: 0.5962 - val_accuracy: 0.8016
Epoch 24/50
782/782 [==============================] - 142s 182ms/step - loss: 0.4274 - accuracy: 0.8510 - val_loss: 0.6341 - val_accuracy: 0.7958
Epoch 25/50
782/782 [==============================] - 145s 186ms/step - loss: 0.4170 - accuracy: 0.8542 - val_loss: 0.6324 - val_accuracy: 0.7981
Epoch 26/50
782/782 [==============================] - 140s 179ms/step - loss: 0.4121 - accuracy: 0.8549 - val_loss: 0.6792 - val_accuracy: 0.7844
Epoch 27/50
782/782 [==============================] - 143s 183ms/step - loss: 0.4014 - accuracy: 0.8596 - val_loss: 0.6452 - val_accuracy: 0.7952
Epoch 28/50
782/782 [==============================] - 144s 185ms/step - loss: 0.3967 - accuracy: 0.8624 - val_loss: 0.6680 - val_accuracy: 0.7878
Epoch 29/50
782/782 [==============================] - 143s 183ms/step - loss: 0.3894 - accuracy: 0.8634 - val_loss: 0.7229 - val_accuracy: 0.7696
Epoch 30/50
782/782 [==============================] - 144s 184ms/step - loss: 0.3827 - accuracy: 0.8641 - val_loss: 0.5982 - val_accuracy: 0.8118
Epoch 31/50
782/782 [==============================] - 143s 183ms/step - loss: 0.3789 - accuracy: 0.8680 - val_loss: 0.6613 - val_accuracy: 0.7959
Epoch 32/50
782/782 [==============================] - 144s 184ms/step - loss: 0.3675 - accuracy: 0.8698 - val_loss: 0.5613 - val_accuracy: 0.8194
Epoch 33/50
782/782 [==============================] - 140s 179ms/step - loss: 0.3663 - accuracy: 0.8702 - val_loss: 0.7028 - val_accuracy: 0.7866
Epoch 34/50
782/782 [==============================] - 141s 180ms/step - loss: 0.3628 - accuracy: 0.8721 - val_loss: 0.6081 - val_accuracy: 0.8041
Epoch 35/50
782/782 [==============================] - 143s 182ms/step - loss: 0.3550 - accuracy: 0.8755 - val_loss: 0.6333 - val_accuracy: 0.8039
Epoch 36/50
782/782 [==============================] - 141s 181ms/step - loss: 0.3471 - accuracy: 0.8765 - val_loss: 0.8010 - val_accuracy: 0.7613
Epoch 37/50
782/782 [==============================] - 144s 184ms/step - loss: 0.3419 - accuracy: 0.8815 - val_loss: 0.6079 - val_accuracy: 0.8143
Epoch 38/50
782/782 [==============================] - 146s 187ms/step - loss: 0.3428 - accuracy: 0.8791 - val_loss: 0.6847 - val_accuracy: 0.7999
Epoch 39/50
782/782 [==============================] - 141s 181ms/step - loss: 0.3384 - accuracy: 0.8798 - val_loss: 0.6337 - val_accuracy: 0.8019
Epoch 40/50
782/782 [==============================] - 144s 184ms/step - loss: 0.3304 - accuracy: 0.8845 - val_loss: 0.5868 - val_accuracy: 0.8198
Epoch 41/50
782/782 [==============================] - 144s 184ms/step - loss: 0.3235 - accuracy: 0.8863 - val_loss: 0.6123 - val_accuracy: 0.8094
Epoch 42/50
782/782 [==============================] - 145s 185ms/step - loss: 0.3228 - accuracy: 0.8860 - val_loss: 0.6453 - val_accuracy: 0.8052
Epoch 43/50
782/782 [==============================] - 143s 183ms/step - loss: 0.3160 - accuracy: 0.8891 - val_loss: 0.5567 - val_accuracy: 0.8328
Epoch 44/50
782/782 [==============================] - 144s 184ms/step - loss: 0.3163 - accuracy: 0.8884 - val_loss: 0.5931 - val_accuracy: 0.8157
Epoch 45/50
782/782 [==============================] - 141s 181ms/step - loss: 0.3122 - accuracy: 0.8902 - val_loss: 0.6287 - val_accuracy: 0.8148
Epoch 46/50
782/782 [==============================] - 142s 181ms/step - loss: 0.3070 - accuracy: 0.8896 - val_loss: 0.5817 - val_accuracy: 0.8235
Epoch 47/50
782/782 [==============================] - 140s 179ms/step - loss: 0.3018 - accuracy: 0.8935 - val_loss: 0.6843 - val_accuracy: 0.7992
Epoch 48/50
782/782 [==============================] - 143s 183ms/step - loss: 0.2954 - accuracy: 0.8962 - val_loss: 0.6035 - val_accuracy: 0.8164
Epoch 49/50
782/782 [==============================] - 144s 183ms/step - loss: 0.2948 - accuracy: 0.8953 - val_loss: 0.6710 - val_accuracy: 0.8030
Epoch 50/50
782/782 [==============================] - 142s 182ms/step - loss: 0.2950 - accuracy: 0.8957 - val_loss: 0.5724 - val_accuracy: 0.8293
Test accuracy (before quantization): 0.8292999863624573
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

Test accuracy after 8-4-4 quantization: 0.7501000165939331
Epoch 1/15
782/782 [==============================] - 179s 225ms/step - loss: 0.8335 - accuracy: 0.7289 - val_loss: 1.0676 - val_accuracy: 0.7163
Epoch 2/15
782/782 [==============================] - 179s 228ms/step - loss: 0.7897 - accuracy: 0.7378 - val_loss: 1.0953 - val_accuracy: 0.7018
Epoch 3/15
782/782 [==============================] - 178s 227ms/step - loss: 0.7576 - accuracy: 0.7475 - val_loss: 0.9311 - val_accuracy: 0.7370
Epoch 4/15
782/782 [==============================] - 179s 228ms/step - loss: 0.7255 - accuracy: 0.7576 - val_loss: 0.8858 - val_accuracy: 0.7407
Epoch 5/15
782/782 [==============================] - 197s 252ms/step - loss: 0.6972 - accuracy: 0.7639 - val_loss: 0.7605 - val_accuracy: 0.7696
Epoch 6/15
782/782 [==============================] - 174s 223ms/step - loss: 0.6781 - accuracy: 0.7696 - val_loss: 0.7722 - val_accuracy: 0.7584
Epoch 7/15
782/782 [==============================] - 179s 229ms/step - loss: 0.6508 - accuracy: 0.7774 - val_loss: 0.8113 - val_accuracy: 0.7471
Epoch 8/15
782/782 [==============================] - 178s 227ms/step - loss: 0.6298 - accuracy: 0.7832 - val_loss: 0.7534 - val_accuracy: 0.7709
Epoch 9/15
782/782 [==============================] - 178s 228ms/step - loss: 0.6088 - accuracy: 0.7896 - val_loss: 0.7329 - val_accuracy: 0.7738
Epoch 10/15
782/782 [==============================] - 177s 227ms/step - loss: 0.5997 - accuracy: 0.7944 - val_loss: 0.6922 - val_accuracy: 0.7858
Epoch 11/15
782/782 [==============================] - 177s 227ms/step - loss: 0.5879 - accuracy: 0.7959 - val_loss: 0.7429 - val_accuracy: 0.7723
Epoch 12/15
782/782 [==============================] - 178s 228ms/step - loss: 0.5779 - accuracy: 0.8002 - val_loss: 0.6817 - val_accuracy: 0.7865
Epoch 13/15
782/782 [==============================] - 179s 228ms/step - loss: 0.5668 - accuracy: 0.8038 - val_loss: 0.7809 - val_accuracy: 0.7636
Epoch 14/15
782/782 [==============================] - 179s 229ms/step - loss: 0.5585 - accuracy: 0.8050 - val_loss: 0.6680 - val_accuracy: 0.7896
Epoch 15/15
782/782 [==============================] - 178s 227ms/step - loss: 0.5507 - accuracy: 0.8083 - val_loss: 0.7088 - val_accuracy: 0.7782
Test accuracy after fine tuning: 0.7781999707221985
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
Test accuracy after Akida conversion: 0.7797999978065491

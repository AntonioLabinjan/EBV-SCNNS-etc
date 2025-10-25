# 60 epoha je bolje nego 50

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
    epochs=60,
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


(venv_mnist) (base) C:\Users\Korisnik\Desktop\cnn2snnTEST>python mnist_brainchip.py
2025-10-25 12:29:27.899193: I tensorflow/core/util/port.cc:113] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
WARNING:tensorflow:From C:\Users\Korisnik\Desktop\cnn2snnTEST\venv_mnist\lib\site-packages\keras\src\losses.py:2976: The name tf.losses.sparse_softmax_cross_entropy is deprecated. Please use tf.compat.v1.losses.sparse_softmax_cross_entropy instead.

2025-10-25 12:29:32.950337: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE SSE2 SSE3 SSE4.1 SSE4.2 AVX2 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
C:\Users\Korisnik\Desktop\cnn2snnTEST\venv_mnist\lib\site-packages\onnxscript\converter.py:816: FutureWarning: 'onnxscript.values.Op.param_schemas' is deprecated in version 0.1 and will be removed in the future. Please use '.op_signature' instead.
  param_schemas = callee.param_schemas()
WARNING:tensorflow:From C:\Users\Korisnik\Desktop\cnn2snnTEST\venv_mnist\lib\site-packages\keras\src\backend.py:873: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.

WARNING:tensorflow:From C:\Users\Korisnik\Desktop\cnn2snnTEST\venv_mnist\lib\site-packages\keras\src\layers\normalization\batch_normalization.py:979: The name tf.nn.fused_batch_norm is deprecated. Please use tf.compat.v1.nn.fused_batch_norm instead.

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
1/1 [==============================] - 0s 356ms/step
Model compatible for Akida conversion: None
Epoch 1/60
WARNING:tensorflow:From C:\Users\Korisnik\Desktop\cnn2snnTEST\venv_mnist\lib\site-packages\keras\src\utils\tf_utils.py:492: The name tf.ragged.RaggedTensorValue is deprecated. Please use tf.compat.v1.ragged.RaggedTensorValue instead.

WARNING:tensorflow:From C:\Users\Korisnik\Desktop\cnn2snnTEST\venv_mnist\lib\site-packages\keras\src\engine\base_layer_utils.py:384: The name tf.executing_eagerly_outside_functions is deprecated. Please use tf.compat.v1.executing_eagerly_outside_functions instead.

782/782 [==============================] - 50s 62ms/step - loss: 1.3490 - accuracy: 0.5154 - val_loss: 1.2424 - val_accuracy: 0.5623
Epoch 2/60
782/782 [==============================] - 77s 98ms/step - loss: 1.0291 - accuracy: 0.6364 - val_loss: 0.9701 - val_accuracy: 0.6509
Epoch 3/60
782/782 [==============================] - 117s 150ms/step - loss: 0.9094 - accuracy: 0.6792 - val_loss: 0.8643 - val_accuracy: 0.6983
Epoch 4/60
782/782 [==============================] - 120s 153ms/step - loss: 0.8307 - accuracy: 0.7077 - val_loss: 0.8473 - val_accuracy: 0.7072
Epoch 5/60
782/782 [==============================] - 124s 158ms/step - loss: 0.7753 - accuracy: 0.7269 - val_loss: 0.8061 - val_accuracy: 0.7182
Epoch 6/60
782/782 [==============================] - 123s 158ms/step - loss: 0.7219 - accuracy: 0.7473 - val_loss: 0.8386 - val_accuracy: 0.7122
Epoch 7/60
782/782 [==============================] - 123s 157ms/step - loss: 0.6893 - accuracy: 0.7565 - val_loss: 0.8071 - val_accuracy: 0.7294
Epoch 8/60
782/782 [==============================] - 125s 159ms/step - loss: 0.6571 - accuracy: 0.7705 - val_loss: 0.9702 - val_accuracy: 0.6614
Epoch 9/60
782/782 [==============================] - 127s 163ms/step - loss: 0.6345 - accuracy: 0.7765 - val_loss: 0.7256 - val_accuracy: 0.7533
Epoch 10/60
782/782 [==============================] - 128s 164ms/step - loss: 0.6023 - accuracy: 0.7890 - val_loss: 0.7416 - val_accuracy: 0.7516
Epoch 11/60
782/782 [==============================] - 120s 154ms/step - loss: 0.5861 - accuracy: 0.7945 - val_loss: 0.7459 - val_accuracy: 0.7501
Epoch 12/60
782/782 [==============================] - 103s 131ms/step - loss: 0.5690 - accuracy: 0.8008 - val_loss: 0.7523 - val_accuracy: 0.7456
Epoch 13/60
782/782 [==============================] - 61s 78ms/step - loss: 0.5510 - accuracy: 0.8049 - val_loss: 0.6928 - val_accuracy: 0.7632
Epoch 14/60
782/782 [==============================] - 60s 77ms/step - loss: 0.5347 - accuracy: 0.8139 - val_loss: 0.6196 - val_accuracy: 0.7872
Epoch 15/60
782/782 [==============================] - 61s 77ms/step - loss: 0.5228 - accuracy: 0.8178 - val_loss: 0.7253 - val_accuracy: 0.7558
Epoch 16/60
782/782 [==============================] - 64s 82ms/step - loss: 0.5121 - accuracy: 0.8207 - val_loss: 0.5654 - val_accuracy: 0.8057
Epoch 17/60
782/782 [==============================] - 66s 84ms/step - loss: 0.4998 - accuracy: 0.8248 - val_loss: 0.5884 - val_accuracy: 0.7990
Epoch 18/60
782/782 [==============================] - 66s 84ms/step - loss: 0.4862 - accuracy: 0.8301 - val_loss: 0.6739 - val_accuracy: 0.7819
Epoch 19/60
782/782 [==============================] - 65s 83ms/step - loss: 0.4743 - accuracy: 0.8324 - val_loss: 0.7463 - val_accuracy: 0.7568
Epoch 20/60
782/782 [==============================] - 65s 83ms/step - loss: 0.4680 - accuracy: 0.8362 - val_loss: 0.6600 - val_accuracy: 0.7868
Epoch 21/60
782/782 [==============================] - 65s 83ms/step - loss: 0.4550 - accuracy: 0.8411 - val_loss: 0.7407 - val_accuracy: 0.7639
Epoch 22/60
782/782 [==============================] - 66s 84ms/step - loss: 0.4449 - accuracy: 0.8460 - val_loss: 0.6112 - val_accuracy: 0.8011
Epoch 23/60
782/782 [==============================] - 66s 84ms/step - loss: 0.4391 - accuracy: 0.8456 - val_loss: 0.7516 - val_accuracy: 0.7519
Epoch 24/60
782/782 [==============================] - 65s 84ms/step - loss: 0.4318 - accuracy: 0.8498 - val_loss: 0.5693 - val_accuracy: 0.8033
Epoch 25/60
782/782 [==============================] - 66s 84ms/step - loss: 0.4268 - accuracy: 0.8515 - val_loss: 0.5837 - val_accuracy: 0.8049
Epoch 26/60
782/782 [==============================] - 66s 84ms/step - loss: 0.4179 - accuracy: 0.8533 - val_loss: 0.6110 - val_accuracy: 0.8048
Epoch 27/60
782/782 [==============================] - 66s 84ms/step - loss: 0.4084 - accuracy: 0.8571 - val_loss: 0.5714 - val_accuracy: 0.8119
Epoch 28/60
782/782 [==============================] - 65s 84ms/step - loss: 0.3987 - accuracy: 0.8589 - val_loss: 0.6036 - val_accuracy: 0.8049
Epoch 29/60
782/782 [==============================] - 65s 84ms/step - loss: 0.3955 - accuracy: 0.8602 - val_loss: 0.6146 - val_accuracy: 0.8039
Epoch 30/60
782/782 [==============================] - 66s 84ms/step - loss: 0.3871 - accuracy: 0.8635 - val_loss: 0.6156 - val_accuracy: 0.8080
Epoch 31/60
782/782 [==============================] - 66s 84ms/step - loss: 0.3834 - accuracy: 0.8659 - val_loss: 0.6194 - val_accuracy: 0.7995
Epoch 32/60
782/782 [==============================] - 70s 90ms/step - loss: 0.3785 - accuracy: 0.8662 - val_loss: 0.7812 - val_accuracy: 0.7667
Epoch 33/60
782/782 [==============================] - 60s 77ms/step - loss: 0.3694 - accuracy: 0.8690 - val_loss: 0.5747 - val_accuracy: 0.8165
Epoch 34/60
782/782 [==============================] - 62s 79ms/step - loss: 0.3686 - accuracy: 0.8701 - val_loss: 0.6047 - val_accuracy: 0.8081
Epoch 35/60
782/782 [==============================] - 61s 78ms/step - loss: 0.3612 - accuracy: 0.8715 - val_loss: 0.5940 - val_accuracy: 0.8134
Epoch 36/60
782/782 [==============================] - 62s 79ms/step - loss: 0.3595 - accuracy: 0.8726 - val_loss: 0.5992 - val_accuracy: 0.8108
Epoch 37/60
782/782 [==============================] - 62s 79ms/step - loss: 0.3509 - accuracy: 0.8765 - val_loss: 0.6089 - val_accuracy: 0.8066
Epoch 38/60
782/782 [==============================] - 62s 79ms/step - loss: 0.3472 - accuracy: 0.8778 - val_loss: 0.5691 - val_accuracy: 0.8209
Epoch 39/60
782/782 [==============================] - 62s 79ms/step - loss: 0.3409 - accuracy: 0.8795 - val_loss: 0.6134 - val_accuracy: 0.8096
Epoch 40/60
782/782 [==============================] - 61s 78ms/step - loss: 0.3381 - accuracy: 0.8811 - val_loss: 0.6615 - val_accuracy: 0.8025
Epoch 41/60
782/782 [==============================] - 98s 125ms/step - loss: 0.3339 - accuracy: 0.8822 - val_loss: 0.6177 - val_accuracy: 0.8111
Epoch 42/60
782/782 [==============================] - 128s 164ms/step - loss: 0.3274 - accuracy: 0.8835 - val_loss: 0.6217 - val_accuracy: 0.8069
Epoch 43/60
782/782 [==============================] - 119s 152ms/step - loss: 0.3255 - accuracy: 0.8856 - val_loss: 0.6161 - val_accuracy: 0.8103
Epoch 44/60
782/782 [==============================] - 117s 150ms/step - loss: 0.3167 - accuracy: 0.8886 - val_loss: 0.5832 - val_accuracy: 0.8208
Epoch 45/60
782/782 [==============================] - 65s 84ms/step - loss: 0.3116 - accuracy: 0.8913 - val_loss: 0.5969 - val_accuracy: 0.8205
Epoch 46/60
782/782 [==============================] - 112s 144ms/step - loss: 0.3087 - accuracy: 0.8910 - val_loss: 0.5914 - val_accuracy: 0.8196
Epoch 47/60
782/782 [==============================] - 126s 161ms/step - loss: 0.3075 - accuracy: 0.8911 - val_loss: 0.5952 - val_accuracy: 0.8213
Epoch 48/60
782/782 [==============================] - 120s 154ms/step - loss: 0.3057 - accuracy: 0.8929 - val_loss: 0.6439 - val_accuracy: 0.8021
Epoch 49/60
782/782 [==============================] - 122s 156ms/step - loss: 0.3005 - accuracy: 0.8939 - val_loss: 0.6040 - val_accuracy: 0.8248
Epoch 50/60
782/782 [==============================] - 117s 150ms/step - loss: 0.2973 - accuracy: 0.8933 - val_loss: 0.6694 - val_accuracy: 0.7971
Epoch 51/60
782/782 [==============================] - 66s 84ms/step - loss: 0.2985 - accuracy: 0.8937 - val_loss: 0.6091 - val_accuracy: 0.8202
Epoch 52/60
782/782 [==============================] - 61s 78ms/step - loss: 0.2890 - accuracy: 0.8976 - val_loss: 0.6075 - val_accuracy: 0.8161
Epoch 53/60
782/782 [==============================] - 112s 143ms/step - loss: 0.2842 - accuracy: 0.8990 - val_loss: 0.5697 - val_accuracy: 0.8252
Epoch 54/60
782/782 [==============================] - 125s 160ms/step - loss: 0.2853 - accuracy: 0.8980 - val_loss: 0.5983 - val_accuracy: 0.8217
Epoch 55/60
782/782 [==============================] - 127s 162ms/step - loss: 0.2839 - accuracy: 0.9003 - val_loss: 0.6401 - val_accuracy: 0.8152
Epoch 56/60
782/782 [==============================] - 122s 155ms/step - loss: 0.2784 - accuracy: 0.9030 - val_loss: 0.6310 - val_accuracy: 0.8159
Epoch 57/60
782/782 [==============================] - 119s 153ms/step - loss: 0.2742 - accuracy: 0.9037 - val_loss: 0.6812 - val_accuracy: 0.8064
Epoch 58/60
782/782 [==============================] - 126s 162ms/step - loss: 0.2723 - accuracy: 0.9038 - val_loss: 0.5892 - val_accuracy: 0.8268
Epoch 59/60
782/782 [==============================] - 123s 157ms/step - loss: 0.2718 - accuracy: 0.9040 - val_loss: 0.6535 - val_accuracy: 0.8088
Epoch 60/60
782/782 [==============================] - 86s 110ms/step - loss: 0.2671 - accuracy: 0.9056 - val_loss: 0.5632 - val_accuracy: 0.8373
Test accuracy (before quantization): 0.8373000025749207
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
WARNING:tensorflow:From C:\Users\Korisnik\Desktop\cnn2snnTEST\venv_mnist\lib\site-packages\keras\src\optimizers\__init__.py:309: The name tf.train.Optimizer is deprecated. Please use tf.compat.v1.train.Optimizer instead.

Test accuracy after 8-4-4 quantization: 0.748199999332428
Epoch 1/15
782/782 [==============================] - 98s 122ms/step - loss: 0.8524 - accuracy: 0.7268 - val_loss: 0.9682 - val_accuracy: 0.7275
Epoch 2/15
782/782 [==============================] - 81s 103ms/step - loss: 0.8198 - accuracy: 0.7307 - val_loss: 1.0180 - val_accuracy: 0.7178
Epoch 3/15
782/782 [==============================] - 81s 104ms/step - loss: 0.7895 - accuracy: 0.7396 - val_loss: 0.8121 - val_accuracy: 0.7467
Epoch 4/15
782/782 [==============================] - 82s 104ms/step - loss: 0.7502 - accuracy: 0.7520 - val_loss: 0.9854 - val_accuracy: 0.7204
Epoch 5/15
782/782 [==============================] - 80s 103ms/step - loss: 0.7196 - accuracy: 0.7586 - val_loss: 0.8039 - val_accuracy: 0.7560
Epoch 6/15
782/782 [==============================] - 76s 97ms/step - loss: 0.6929 - accuracy: 0.7636 - val_loss: 0.8216 - val_accuracy: 0.7555
Epoch 7/15
782/782 [==============================] - 79s 101ms/step - loss: 0.6619 - accuracy: 0.7725 - val_loss: 0.9744 - val_accuracy: 0.7214
Epoch 8/15
782/782 [==============================] - 78s 99ms/step - loss: 0.6413 - accuracy: 0.7818 - val_loss: 0.7760 - val_accuracy: 0.7538
Epoch 9/15
782/782 [==============================] - 78s 99ms/step - loss: 0.6264 - accuracy: 0.7849 - val_loss: 0.7624 - val_accuracy: 0.7639
Epoch 10/15
782/782 [==============================] - 81s 104ms/step - loss: 0.6103 - accuracy: 0.7877 - val_loss: 0.7316 - val_accuracy: 0.7728
Epoch 11/15
782/782 [==============================] - 79s 101ms/step - loss: 0.6037 - accuracy: 0.7900 - val_loss: 0.7413 - val_accuracy: 0.7716
Epoch 12/15
782/782 [==============================] - 80s 102ms/step - loss: 0.5883 - accuracy: 0.7945 - val_loss: 0.7122 - val_accuracy: 0.7735
Epoch 13/15
782/782 [==============================] - 81s 104ms/step - loss: 0.5921 - accuracy: 0.7932 - val_loss: 0.7089 - val_accuracy: 0.7794
Epoch 14/15
782/782 [==============================] - 80s 102ms/step - loss: 0.5704 - accuracy: 0.8017 - val_loss: 0.7158 - val_accuracy: 0.7761
Epoch 15/15
782/782 [==============================] - 79s 102ms/step - loss: 0.5698 - accuracy: 0.8007 - val_loss: 0.6766 - val_accuracy: 0.7801
Test accuracy after fine tuning: 0.7800999879837036
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
Test accuracy after Akida conversion: 0.7785999774932861

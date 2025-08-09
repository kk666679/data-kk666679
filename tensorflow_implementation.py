# tensorflow_implementation.py
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, datasets, callbacks
import numpy as np
import matplotlib.pyplot as plt

def mnist_classification():
    """Basic image classification with MNIST"""
    print("\n=== MNIST Classification ===")
    
    # Load and preprocess data
    (x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()
    x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
    x_test = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0
    
    # Build model
    model = keras.Sequential([
        layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(10)
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    
    # Train
    history = model.fit(
        x_train, y_train,
        batch_size=64,
        epochs=5,
        validation_split=0.2
    )
    
    # Evaluate
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"\nTest accuracy: {test_acc:.4f}")
    
    # Plot training history
    plt.figure(figsize=(10, 5))
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Training History')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

def fashion_mnist_cnn():
    """CNN for Fashion MNIST with callbacks"""
    print("\n=== Fashion MNIST CNN ===")
    
    # Load data
    (x_train, y_train), (x_test, y_test) = datasets.fashion_mnist.load_data()
    x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
    x_test = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0
    
    # Build model
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10)
    ])
    
    model.compile(
        optimizer='adam',
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    
    # Callbacks
    early_stopping = callbacks.EarlyStopping(monitor='val_loss', patience=2)
    model_checkpoint = callbacks.ModelCheckpoint(
        'best_model.h5',
        save_best_only=True,
        monitor='val_accuracy'
    )
    
    # Train
    history = model.fit(
        x_train, y_train,
        epochs=10,
        batch_size=64,
        validation_split=0.2,
        callbacks=[early_stopping, model_checkpoint]
    )
    
    # Evaluate
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"\nTest accuracy: {test_acc:.4f}")

def cifar10_resnet():
    """ResNet style model for CIFAR-10"""
    print("\n=== CIFAR-10 ResNet ===")
    
    # Load data
    (x_train, y_train), (x_test, y_test) = datasets.cifar10.load_data()
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    
    # ResNet block
    def resnet_block(x, filters, kernel_size=3):
        # Shortcut
        shortcut = x
        
        # Main path
        x = layers.Conv2D(filters, kernel_size, padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        
        x = layers.Conv2D(filters, kernel_size, padding='same')(x)
        x = layers.BatchNormalization()(x)
        
        # Add shortcut if dimensions match
        if shortcut.shape[-1] != filters:
            shortcut = layers.Conv2D(filters, 1)(shortcut)
        
        x = layers.add([x, shortcut])
        x = layers.Activation('relu')(x)
        return x
    
    # Build model
    inputs = keras.Input(shape=(32, 32, 3))
    x = layers.Conv2D(32, 3, padding='same')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)
    
    x = resnet_block(x, 32)
    x = layers.MaxPooling2D(2)(x)
    
    x = resnet_block(x, 64)
    x = layers.MaxPooling2D(2)(x)
    
    x = resnet_block(x, 128)
    x = layers.GlobalAveragePooling2D()(x)
    
    outputs = layers.Dense(10)(x)
    
    model = keras.Model(inputs, outputs)
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    
    # Train
    history = model.fit(
        x_train, y_train,
        batch_size=64,
        epochs=10,
        validation_split=0.2
    )
    
    # Evaluate
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"\nTest accuracy: {test_acc:.4f}")

def text_classification():
    """Text classification with IMDB reviews"""
    print("\n=== IMDB Text Classification ===")
    
    # Load data
    (x_train, y_train), (x_test, y_test) = datasets.imdb.load_data(num_words=10000)
    
    # Preprocess
    x_train = keras.preprocessing.sequence.pad_sequences(x_train, maxlen=256)
    x_test = keras.preprocessing.sequence.pad_sequences(x_test, maxlen=256)
    
    # Build model
    model = keras.Sequential([
        layers.Embedding(10000, 16),
        layers.GlobalAveragePooling1D(),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    # Train
    history = model.fit(
        x_train, y_train,
        epochs=10,
        batch_size=512,
        validation_split=0.2
    )
    
    # Evaluate
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"\nTest accuracy: {test_acc:.4f}")

def main():
    # Run all examples
    mnist_classification()
    fashion_mnist_cnn()
    cifar10_resnet()
    text_classification()

if __name__ == "__main__":
    # Configure TensorFlow to use GPU if available
    physical_devices = tf.config.list_physical_devices('GPU')
    if physical_devices:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
    
    main()

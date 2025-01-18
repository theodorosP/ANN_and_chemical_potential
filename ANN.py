import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Simulated dataset (replace with actual data)
X = np.random.rand(10000, 180)  # Features
y = np.random.rand(10000, 1)    # Targets

# Normalize the data
scaler = StandardScaler()

# Define hyperparameters
layer_configs = [
    [64],          # Single hidden layer
    [128, 64],     # Two hidden layers
    [128, 64, 32]  # Three hidden layers
]
dropout_rates = [0.0, 0.2, 0.4]  # Dropout rates
learning_rate = 0.001
batch_size = 32
epochs = 100

# Split into train+val and test sets
X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define callbacks
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=1e-6
)

# Function to build a model
def build_model(layer_config, dropout_rate):
    """Builds a neural network with the specified layer configuration and dropout."""
    model = Sequential()
    for i, neurons in enumerate(layer_config):
        if i == 0:
            model.add(Dense(neurons, activation='relu', input_shape=(X.shape[1],)))
        else:
            model.add(Dense(neurons, activation='relu'))
        if dropout_rate > 0.0:
            model.add(Dropout(dropout_rate))
    model.add(Dense(1))  # Output layer for regression
    model.compile(optimizer=Adam(learning_rate=learning_rate), loss='mse', metrics=['mae'])  # Add MAE metric
    return model

# Hyperparameter tuning with k-fold cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
results = []

for layer_config in layer_configs:
    for dropout_rate in dropout_rates:
        fold_mse = []  # Store MSE for each fold
        for train_idx, val_idx in kf.split(X_train_val):
            # Split into training and validation for this fold
            X_train, X_val = X_train_val[train_idx], X_train_val[val_idx]
            y_train, y_val = y_train_val[train_idx], y_train_val[val_idx]

            # Normalize the data
            X_train = scaler.fit_transform(X_train)
            X_val = scaler.transform(X_val)

            # Build and train the model
            model = build_model(layer_config, dropout_rate)
            history = model.fit(
                X_train, y_train,
                validation_data=(X_val, y_val),
                batch_size=batch_size,
                epochs=epochs,
                verbose=0,
                callbacks=[early_stopping, reduce_lr]
            )

            # Evaluate on validation set
            val_mse = model.evaluate(X_val, y_val, verbose=0)
            fold_mse.append(val_mse)

        # Average MSE for this configuration
        avg_mse = np.mean(fold_mse)
        results.append({
            'layers': layer_config,
            'dropout_rate': dropout_rate,
            'avg_mse': avg_mse
        })
        print(f"Layers: {layer_config}, Dropout: {dropout_rate}, Avg MSE: {avg_mse}")

# Select the best configuration
best_model_config = min(results, key=lambda x: x['avg_mse'])
print(f"Best Model Configuration: {best_model_config}")

# Split train+val into train and val for final training
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.2, random_state=42)

# Normalize the data
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Train the final model with the best configuration
final_model = build_model(best_model_config['layers'], best_model_config['dropout_rate'])
history = final_model.fit(
    X_train_scaled, y_train,
    validation_data=(X_val_scaled, y_val),  # Include validation data during training
    batch_size=batch_size,
    epochs=epochs,
    callbacks=[early_stopping, reduce_lr],
    verbose=1
)

# Evaluate the final model on the test set
test_mse = final_model.evaluate(X_test_scaled, y_test, verbose=1)
print(f"Test MSE: {test_mse}")

# Plot the training and validation loss (MSE and MAE)
plt.figure(figsize=(14, 6))

# Plot MSE
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training MSE')
plt.plot(history.history['val_loss'], label='Validation MSE')
plt.title('Training and Validation MSE')
plt.xlabel('Epochs')
plt.ylabel('MSE')
plt.legend()

# Plot MAE
plt.subplot(1, 2, 2)
plt.plot(history.history['mae'], label='Training MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.title('Training and Validation MAE')
plt.xlabel('Epochs')
plt.ylabel('MAE')
plt.legend()

# Show plots
plt.tight_layout()
plt.show()

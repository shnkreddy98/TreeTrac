import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import pickle

def evaluate_metrics(y_test, y_pred, model):
    # Calculate Evaluation Metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Print the Metrics
    print(f"{model} - Mean Squared Error (MSE): {mse}")
    print(f"{model} - Root Mean Squared Error (RMSE): {rmse}")
    print(f"{model} - Mean Absolute Error (MAE): {mae}")
    print(f"{model} - R2 Score: {r2}")

    return mse, rmse, mae, r2


def flatten_arrays(y_test, y_pred):
    # If y_test is already a NumPy array, no need to convert
    if isinstance(y_test, pd.Series):
        y_test = y_test.to_numpy()

    # Flatten both y_test and y_pred to ensure they are 1D arrays
    y_pred = y_pred.flatten()  
    y_test = y_test.flatten()
    return y_test, y_pred

def save_models(model):
    pickle.dump(model, open(f"/model_results/{model}", 'wb'))

def loss_curve(history, model_name):
    # Plotting Loss vs. Validation Loss for Improved ANN Model
    plt.figure(figsize=(8, 6))
    plt.plot(history.history['loss'], label='Training Loss', color='blue')
    plt.plot(history.history['val_loss'], label='Validation Loss', color='orange')
    plt.xlabel('Epochs')
    plt.ylabel('Loss (MAE)')
    plt.title('Training vs Validation Loss Curve (Improved ANN)')
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig(f'{MODEL}.png')
    plt.close()

def post_model(y_test, y_pred, history, model_obj, model_name):
    evaluate_metrics(y_test, y_pred, model_name)
    loss_curve(history, model_name)
    save_models(model_obj)
    y_test, y_pred = flatten_arrays(y_test, y_pred)


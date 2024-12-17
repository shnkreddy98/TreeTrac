import numpy as np
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.neighbors import KNeighborsRegressor

from evaluatemodel import post_model

MODEL = 'CFR-Eco Ensemble Model'

class CFREcoEnsemble():
    def model(input_shape):
        model = Sequential()
        model.add(Dense(16, activation='sigmoid', input_shape=(input_shape,)))
        model.add(Dense(8, activation='sigmoid'))
        model.add(Dense(1, activation='linear'))
        model.compile(optimizer=Adam(learning_rate=0.0001), loss='mean_squared_error', metrics=['mae'])
        return model

    def build(X_train, X_test, X_val,
              y_train, y_test, y_val):
    
        noise_factor = 0.9
        y_train_noisy = y_train + noise_factor * np.random.normal(size=y_train.shape)

        baseann = CFREcoEnsemble.model(input_shape=X_train.shape[1])
        history_ann = baseann.fit(X_train, y_train_noisy, epochs=30, batch_size=32, validation_data=(X_val, y_val), verbose=1)

        y_pred_ann_train = baseann.predict(X_train).flatten()
        y_pred_ann_val = baseann.predict(X_val).flatten()
        y_pred_ann_test = baseann.predict(X_test).flatten()

        rf_model = RandomForestRegressor(n_estimators=100, min_samples_split=10, min_samples_leaf=5, random_state=42)
        rf_model.fit(X_train, y_train_noisy)
        y_pred_rf_train = rf_model.predict(X_train)
        y_pred_rf_val = rf_model.predict(X_val)
        y_pred_rf_test = rf_model.predict(X_test)

        X_meta_train = np.column_stack((y_pred_ann_train, y_pred_rf_train))
        X_meta_val = np.column_stack((y_pred_ann_val, y_pred_rf_val))
        X_meta_test = np.column_stack((y_pred_ann_test, y_pred_rf_test))
        
        meta_learner = KNeighborsRegressor(n_neighbors=1)
        meta_learner.fit(X_meta_train, y_train)

        y_pred = meta_learner.predict(X_meta_test)

        post_model(y_test, y_pred, history_ann, meta_learner, MODEL)

        return y_pred
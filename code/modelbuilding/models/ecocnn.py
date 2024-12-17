from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv1D
from keras.layers import GlobalMaxPooling1D
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau

from evaluatemodel import post_model

MODEL = 'Eco-CNN Model'

class EcoCNN():

    def model(input_shape, learning_rate=0.00003, l2_lambda=0.0001, dropout_rate=0.9):
        model = Sequential()
        model.add(Conv1D(64, kernel_size=2, activation='relu', kernel_regularizer=l2(l2_lambda), input_shape=(input_shape, 1)))
        model.add(GlobalMaxPooling1D())
        model.add(Dense(128, activation='relu', kernel_regularizer=l2(l2_lambda)))
        model.add(Dropout(dropout_rate))
        model.add(Dense(64, activation='relu', kernel_regularizer=l2(l2_lambda)))
        model.add(Dense(1, activation='linear'))
        optimizer = Adam(learning_rate=learning_rate)
        model.compile(optimizer=optimizer, loss='mean_absolute_error', metrics=['mae'])
        return model
    
    def build(X_train, X_test, X_val,
              y_train, y_test, y_val):

        X_train_cnn = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_val_cnn = X_val.reshape((X_val.shape[0], X_val.shape[1], 1))
        X_test_cnn = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6, verbose=1)

        ecocnn = EcoCNN.model(input_shape=X_train_cnn.shape[1])
        history = ecocnn.fit(X_train_cnn, y_train,
                                         epochs=40,
                                         batch_size=128,
                                         validation_data=(X_val_cnn, y_val),
                                         callbacks=[lr_scheduler],
                                         verbose=1
                                        )

        y_pred = ecocnn.predict(X_test_cnn)

        post_model(y_test, y_pred, history, ecocnn, MODEL)
        
        return y_pred
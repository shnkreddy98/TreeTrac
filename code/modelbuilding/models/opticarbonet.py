from evaluatemodel import post_model

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau

MODEL = 'Opti-Carbon Net Model'

class OptiCarboNet():

    def model(input_shape, learning_rate=0.00005, l2_lambda=0.01):
        model = Sequential()
        
        # FC 1
        model.add(Dense(128, activation='relu', kernel_regularizer=l2(l2_lambda), input_shape=(input_shape,)))
        model.add(BatchNormalization())  # BN 1
        
        # FC 2
        model.add(Dense(64, activation='relu', kernel_regularizer=l2(l2_lambda)))
        model.add(BatchNormalization())  # BN 2
        
        # FC 3
        model.add(Dense(32, activation='relu', kernel_regularizer=l2(l2_lambda)))
        
        # FC 4 - Final output layer
        model.add(Dense(1, activation='linear'))
        
        # Compile the model with Adam optimizer and MAE loss
        optimizer = Adam(learning_rate=learning_rate)
        model.compile(optimizer=optimizer, loss='mean_absolute_error', metrics=['mae'])
        
        return model
    
    def build(X_train, X_test, 
              X_val, y_train, 
              y_test, y_val):

        lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6, verbose=1)

        input_shape = X_train.shape[1]
        opticarbonet = OptiCarboNet.model(input_shape)

        history = opticarbonet.fit(X_train,
                                   y_train,
                                   epochs=30,
                                   batch_size=256,
                                   validation_data=(X_val, y_val),
                                   callbacks=[lr_scheduler],
                                   verbose=1
                                   )

        y_pred = opticarbonet.predict(X_test)

        post_model(y_test, y_pred, history, opticarbonet, MODEL)

        return y_pred

        


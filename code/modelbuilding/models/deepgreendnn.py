from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.layers import Input, Add
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model

from evaluatemodel import post_model

MODEL = 'DeepGreen-DNN Model'

class DeepGreenDNN():
    def model(input_shape, learning_rate=0.000015, l2_lambda=0.001, dropout_rate=0.3):
        inputs = Input(shape=(input_shape,))
        
        # First Residual Block
        x = Dense(64, activation='relu', kernel_regularizer=l2(l2_lambda))(inputs)
        x = BatchNormalization()(x)
        x = Dropout(dropout_rate)(x)
        x = Dense(64, activation='relu', kernel_regularizer=l2(l2_lambda))(x)
        x = BatchNormalization()(x)

        residual = Dense(64, activation='linear')(inputs)
        x = Add()([x, residual])
        x = Dropout(dropout_rate)(x)
        
        # Second Residual Block
        x = Dense(128, activation='relu', kernel_regularizer=l2(l2_lambda))(x)
        x = BatchNormalization()(x)
        x = Dropout(dropout_rate)(x)
        x = Dense(128, activation='relu', kernel_regularizer=l2(l2_lambda))(x)
        x = BatchNormalization()(x)

        residual = Dense(128, activation='linear')(x)
        x = Add()([x, residual])

        # Output Layer
        outputs = Dense(1, activation='linear')(x)
        
        # Compile model
        model = Model(inputs, outputs)
        optimizer = Adam(learning_rate=learning_rate)
        model.compile(optimizer=optimizer, loss='mean_absolute_error', metrics=['mae'])
        
        return model

    def build(X_train, X_test, X_val,
              y_train, y_test, y_val):

        input_shape = X_train.shape[1]
        deepgreen = DeepGreenDNN.model(input_shape=input_shape)

        history = deepgreen.fit(X_train, y_train,
                                epochs=50,
                                batch_size=128,
                                validation_data=(X_val, y_val),
                                verbose=1
                                )

        y_pred = deepgreen.predict(X_test)

        post_model(y_test, y_pred, history, deepgreen, MODEL)
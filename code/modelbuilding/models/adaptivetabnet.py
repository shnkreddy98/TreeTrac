from pytorch_tabnet.tab_model import TabNetRegressor
import torch

from evaluatemodel import post_model

MODEL = 'Adaptive TabNet Model'

class AdaptiveTabNet():
    def model(X_train):
        model = TabNetRegressor(optimizer_fn=torch.optim.Adam, optimizer_params=dict(lr=0.0008))
        return model

    def build(X_train, X_test, X_val, 
              y_train, y_test, y_val):

        tabnet = AdaptiveTabNet.model(X_train)

        y_train = y_train.values.reshape(-1, 1)
        y_val = y_val.values.reshape(-1, 1)

        history = tabnet.fit(X_train=X_train, y_train=y_train,
                             eval_set=[(X_train, y_train), (X_val, y_val)],
                             eval_name=['train', 'valid'],
                             eval_metric=['mae'],
                             max_epochs=25,
                             batch_size=512,
                             virtual_batch_size=128,
                             patience=10
                            )

        y_pred = tabnet.predict(X_test)

        post_model(y_test, y_pred, history, tabnet, MODEL)
from __future__ import absolute_import
from celery import shared_task
from keras.models import Sequential
from keras.layers import Dense
from NNModelManager.util import task_callbacks
from datetime import datetime
import numpy as np
import pandas
import os
import json
from django.conf import settings

np.random.seed(27)

@shared_task
def trainNetworkByName(model_obj, job_id):
    '''
    Async task of training a neuron network
    '''
    # read params
    num_layers = model_obj.num_layers
    layer_neurons = [int(item) for item in model_obj.num_neurons_layer_str.split(",")]
    b_size = model_obj.batch_size
    optim = model_obj.optim_func
    loss = model_obj.loss_func
    headers = model_obj.current_data_header
    target = model_obj.target_col_name

    # load data
    data_file_path = os.path.join(settings.NN_MODEL_DATA_PATH, model_obj.data_file_path)
    data = pandas.read_csv(data_file_path, delimiter=',', header=None)
    data_set = data.values
    index_of_target = headers.index(target)
    Y = data_set[:, index_of_target]
    X = np.delete(data_set, index_of_target, 1)

    # config model
    model = Sequential()
    num_input = len(X[0, :])
    model.add(Dense(layer_neurons[0], input_dim=num_input, activation='sigmoid'))
    for ind in range(0,num_layers-1):
        model.add(Dense(layer_neurons[ind+1], input_dim=layer_neurons[ind], activation='sigmoid'))
    model.add(Dense(1, input_dim=layer_neurons[-1], activation='sigmoid'))
    model.compile(loss=loss, optimizer=optim, metrics=['mape'])

    # fit model with input and output
    history = model.fit(X, Y, epochs=1000, batch_size=b_size)
    min_error = min(history.history['mean_absolute_percentage_error'])
    model_json = model.to_json()
    weights = model.get_weights()
    weights_aslist = []
    for numpy_weight_array in weights:
        weights_aslist.append(numpy_weight_array.tolist())

    weights_json = json.dumps(weights_aslist)
    model_obj.weights_json = weights_json
    model_obj.min_train_err = min_error
    model_obj.save()
    task_callbacks.onTrainingCompeted(job_id, True, weights_json)


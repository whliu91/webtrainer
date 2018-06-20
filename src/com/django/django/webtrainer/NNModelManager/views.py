from django.shortcuts import render
from django.http import HttpResponse
import json
from datetime import datetime
from users.models import User
from NNModelManager.models import NNModelHistory
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    if request.method == 'POST':
        model_json = json.loads(request.body)
        if (model_json['command'] == "save_json_model"):
            model_user = request.user.email
            print("[DEBUG] POST: new model save POST request from: " + model_user)
            model_company = request.user.company
            model_name = model_json['model_name']
            model_num_input = int(model_json['num_input'])
            model_num_layers = int(model_json['num_layers'])
            model_num_neuron_layer_str = model_json['num_neuron_layer_str']
            model_optim_func = model_json['optimise_function']
            model_src_date = datetime.now()
            # check model existance
            if NNModelHistory.objects.filter(model_name=model_name).exists():
                print("[DEBUG] error: model name exists in db")
                return HttpResponse(1)
            else:
                # TODO: change these default values to user selected values
                newRow = NNModelHistory.objects.create(
                    src_date = model_src_date,
                    user_created = model_user,
                    company_created = model_company,
                    model_name = model_name,
                    input_size = model_num_input,
                    batch_size = 32,
                    optim_func = model_optim_func,
                    loss_func = 'adam',
                    epoch_size = 1000,
                    num_layers = model_num_layers,
                    num_neurons_layer_str = model_num_neuron_layer_str,
                    weights_json = None,
                    min_train_err = None,
                    data_file = None
                )
                print("[DEBUG] successfully saved model")
                return HttpResponse(0)

    return render(request, 'index.html')

def dataManage(request):
    return render(request, 'data_management.html')

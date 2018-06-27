from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse  
from django.shortcuts import redirect 
import json
from django.core import serializers
from datetime import datetime
from users.models import User
from NNModelManager.models import NNModelHistory
from django.views.decorators.csrf import csrf_exempt
from util.DataConversion import QuerySetValuesToDictionOfStrings


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

        elif (model_json['command'] == "get_history_model"):
            print("[DEBUG] query all history models")
            all_models = NNModelHistory.objects.values(
                "model_name",
                "num_layers",
                "min_train_err",
                "src_date",
                "user_created"
            )
            ret = {
                "header": "all models",
                "result": "success",
                "records": QuerySetValuesToDictionOfStrings(all_models)
            }
            return JsonResponse(ret)

        elif (model_json['command'] == "delete_model"):
            model_name = model_json['model_name']
            print("[DEBUG] delete model request: " + model_name)
            NNModelHistory.objects.filter(model_name=model_name).delete()
            return HttpResponse("model deleted from database: " + model_name)
        
        elif (model_json['command'] == "user_select_model"):
            model_name = model_json['model_name']
            print("[DEBUG] select model request: " + model_name)
            user_profile_toChange = User.objects.get(email=request.user.email)
            user_profile_toChange.current_selected_model_name = model_name
            user_profile_toChange.save()
            return HttpResponseRedirect('/NNModelManager/dataManage/')

    return render(request, 'index.html')


@csrf_exempt
def dataManage(request):
    if request.method == 'POST':
        model_json = json.loads(request.body)
        if (model_json['command'] == "check_model"):
            model = request.user.current_selected_model_name
            if not model:
                return HttpResponse(1)
            else:
                target_model_obj = NNModelHistory.objects.get(model_name=model)
                ret = {
                    "header": "selected model",
                    "result": "success",
                    "records": [{
                        "model_name": str(model),
                        "src_date": str(target_model_obj.src_date.strftime('%Y-%m-%d')),
                        "num_layers": str(target_model_obj.num_layers),
                        "input_size": str(target_model_obj.input_size),
                    }]
                }
                return JsonResponse(ret)

    return render(request, 'data_management.html')

def operations(request):
    return render(request, 'operations.html')

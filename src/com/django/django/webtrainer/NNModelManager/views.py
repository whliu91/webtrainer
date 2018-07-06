from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse  
from django.shortcuts import redirect 
import json
from django.core import serializers
from datetime import datetime
from users.models import User
from NNModelManager.models import NNModelHistory
from NNModelManager.util import trainer_util
from django.views.decorators.csrf import csrf_exempt
from util.DataConversion import QuerySetValuesToDictionOfStrings

from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def index(request):
    if request.method == 'POST':
        logger.info("POST request from user: " + request.user.email)
        model_json = json.loads(request.body)
        if (model_json['command'] == "save_json_model"):
            model_user = request.user.email
            logger.info("POST: new model save POST request from: " + model_user)
            model_company = request.user.company
            model_name = model_json['model_name']
            model_num_input = int(model_json['num_input'])
            model_num_layers = int(model_json['num_layers'])
            model_num_neuron_layer_str = model_json['num_neuron_layer_str']
            model_optim_func = model_json['optimise_function']
            model_src_date = datetime.now()
            # create DIR for upload files
            model_data_dir= os.path.join(settings.MEDIA_ROOT, 'uploads', model_name)
            os.makedirs(model_data_dir, exist_ok=True)
            # check model existance
            if NNModelHistory.objects.filter(model_name=model_name).exists():
                logger.warning("model name exists in db! model: " + model_name)
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
                    data_file_path = None
                )
                logger.info("successfully saved model: " + model_name)
                return HttpResponse(0)

        elif (model_json['command'] == "get_history_model"):
            logger.info("backend query all history models!")
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
            logger.info("delete model request, model: " + model_name)
            NNModelHistory.objects.filter(model_name=model_name).delete()
            return HttpResponse("model deleted from database: " + model_name)
        
        elif (model_json['command'] == "user_select_model"):
            model_name = model_json['model_name']
            logger.info("select model request, model: " + model_name)
            user_profile_toChange = User.objects.get(email=request.user.email)
            user_profile_toChange.current_selected_model_name = model_name
            user_profile_toChange.save()
            return HttpResponseRedirect('/NNModelManager/dataManage/')

    return render(request, 'index.html')


@csrf_exempt
def dataManage(request):
    if request.method == 'POST':
        logger.info("POST request from user: " + request.user.email)
        model_json = json.loads(request.body)
        if (model_json['command'] == "check_model"):
            model = request.user.current_selected_model_name
            logger.info("check model history data request, model: " + model)
            if not model:
                logger.warning("no model name provided!")
                return HttpResponse(1)
            else:
                logger.info("validation model from history db, model: " + model)
                target_model_obj = NNModelHistory.objects.get(model_name=model)
                trainer_util.validDataRecords(target_model_obj)
                logger.info("validation completed, model: " + model)
                ret = {
                    "header": "selected model",
                    "result": "success",
                    "records": [{
                        "model_name": str(model),
                        "src_date": str(target_model_obj.src_date.strftime('%Y-%m-%d')),
                        "num_layers": str(target_model_obj.num_layers),
                        "input_size": str(target_model_obj.input_size),
                    }],
                    "data_headers": target_model_obj.current_data_header,
                    "target_col_name": target_model_obj.target_col_name,
                    "data_rows": str(target_model_obj.data_rows)
                }
                return JsonResponse(ret)
            
        elif (model_json['command'] == "change_target_col"):
            model = request.user.current_selected_model_name
            logger.info("change target column name request, model: " + model)
            if not model:
                logger.warning("no model name provided!")
                return HttpResponse(1)
            else:
                logger.info("validation model from history db, model: " + model)
                target_model_obj = NNModelHistory.objects.get(model_name=model)
                current_data_header = target_model_obj.current_data_header
                header_list = current_data_header.split(',')
                target_col_name = model_json['target_col_name']
                if target_col_name in current_data_header:
                    target_model_obj.target_col_name = target_col_name
                    target_model_obj.save()
                    logger.info("changed target column: " + target_col_name)
                    return HttpResponse(0)
                else:
                    logger.error("col does not exist: " + target_col_name)
                    return HttpResponse(2)

    return render(request, 'data_management.html')


@csrf_exempt
def acceptDataUpload(request):
    if request.method == 'POST':
        logger.info("POST request from user: " + request.user.email)
        model_name = request.POST["model_name"]
        uploaded_file = request.FILES['file']
        if (request.POST["command"] == "upload"):
            logger.info("upload request for file: {} and model name: {}".format(uploaded_file.name, model_name))
            save_path = os.path.join(settings.BASE_DIR, 'uploads\\temp', model_name)
            final_path = os.path.join(settings.BASE_DIR, 'uploads\\data', model_name)
            fs = FileSystemStorage(location=save_path)
            filename = fs.save(model_name + "_data.csv", uploaded_file)
            if not os.path.exists(final_path):
                os.makedirs(final_path)
            if(trainer_util.acceptNewDataFile(model_name, os.path.join(save_path, filename))):
                os.remove(os.path.join(save_path, filename))
                return HttpResponse(1)
            else:
                os.remove(os.path.join(save_path, filename))
                return HttpResponse("unknown")
        
        elif (request.POST["command"] == "insert"):
            logger.info("insert request for file: {} and model name: {}".format(uploaded_file.name, model_name))
            save_path = os.path.join(settings.BASE_DIR, 'uploads\\temp', model_name)
            fs = FileSystemStorage(location=save_path)
            filename = fs.save(model_name + "_data.csv", uploaded_file)
            if(trainer_util.acceptNewInsert(model_name, os.path.join(save_path, filename))):
                os.remove(os.path.join(save_path, filename))
                return HttpResponse(1)
            else:
                os.remove(os.path.join(save_path, filename))
                return HttpResponse("unknown")

    logger.error("unknown http request from user: " + request.user.email)
    return HttpResponse("unknown")


@csrf_exempt
def operations(request):
    if request.method == 'POST':
        logger.info("POST request from user: " + request.user.email)
        if (request.POST["command"] == "submit_job"):
            model_name = request.user.current_selected_model_name
            logger.info("Training request for model: " + model_name)
            success = trainer_util.submitTrainingJob(model_name)
            if success:
                logger.info("submit request succeed")
                return HttpResponse(0)
            else:
                logger.error("submit request failed")
                return HttpResponse(1)

    return render(request, 'operations.html')

import csv
import numpy as np
from NNModelManager.models import NNModelHistory, NNJobHistory
from NNModelManager.util import plotNN, async_task
from datetime import datetime
from util import DataConversion
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


# TODO: data related process will be time consuming, consider migrate
# to Celery when it is deployed.

def validDataRecords(model_obj):
    '''
    Validate data record, try to match file content and db
    results in case there is a change in file.
    '''
    header_str = model_obj.current_data_header
    data_rows = model_obj.data_rows
    if (not model_obj.data_file_path):
        logger.info("data file does not exist, model: " + model_obj.model_name)
        model_obj.data_rows = 0
        model_obj.current_data_header = None
        model_obj.data_file_path = None
        model_obj.save()
        return

    data_file_path = os.path.join(settings.NN_MODEL_DATA_PATH, model_obj.data_file_path)
    if (bool(data_file_path) & os.path.exists(data_file_path)):
        logger.info("data file exist, matching content, model: " + model_obj.model_name)
        with open(data_file_path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            count = 0
            for line in spamreader:
                count += 1

        if (data_rows != count):
            model_obj.data_rows = count

        model_obj.save()
        logger.info("validate completed, model: " + model_obj.model_name)
        return True

    else:
        logger.warning("recorded data file missing, clear history, model: " + model_obj.model_name)
        model_obj.data_rows = 0
        model_obj.current_data_header = None
        model_obj.data_file_path = None
        model_obj.save()
        return False


def acceptNewDataFile(model_name, temp_file_path):
    '''
    Accept a new data file for a model that has no previous record
    '''
    logger.info("new data file created for model: " + model_name)
    with open(temp_file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        temp_lst = []
        for line in spamreader:
            temp_lst.append(line)
        # sort list by header
        temp_lst = sortListByFirstRow(temp_lst)
        data_lst = temp_lst[1:]
        count = len(data_lst)
        if count > 0:
            data_file_path = os.path.join('uploads', 'data', model_name, model_name + "_data.csv")
            if appendToCsvFile(data_file_path, data_lst):
                header_str = ','.join(temp_lst[0])
                modelHistory = NNModelHistory.objects.get(model_name=model_name)
                modelHistory.data_rows = count
                modelHistory.current_data_header = header_str
                modelHistory.data_file_path = os.path.join(model_name, model_name + "_data.csv")
                modelHistory.save()
                logger.info("model data saved, model: " + model_name)
                return True
        else:
            logger.warning("new data file contains 0 rows!, model: " + model_name)
            return False
    
    logger.error("cannot open data file! for file: " + file_path)
    return False

def acceptNewInsert(model_name, temp_file_path):
    '''
    Accept a new inserted data file with comparison on the header first
    '''
    logger.info("new data insertation for model: " + model_name)
    target_model_obj = NNModelHistory.objects.get(model_name=model_name)
    current_data_header = target_model_obj.current_data_header
    current_count = target_model_obj.data_rows
    with open(temp_file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        temp_list = []
        for line in spamreader:
            temp_list.append(line)
        temp_list = sortListByFirstRow(temp_list)
        data_list = temp_list[1:]
        header_str = ','.join(temp_list[0])
        count = len(data_list)
        if (count > 0) & (header_str == current_data_header):
            data_file_path = os.path.join('uploads', 'data', model_name, model_name + "_data.csv")
            if appendToCsvFile(data_file_path, data_list):
                target_model_obj.data_rows = current_count + count
                target_model_obj.save()
                logger.info("insertation success, model: " + model_name)
                return True
        else:
            logger.error("header of insert file does not match previous file!")
    
    return False

def sortListByFirstRow(lst):
    '''
    Assume the first row of a list is header, and sort the columns of the list by
    header, return the sorted list.
    '''
    data = np.array(lst)
    data = data[:, np.argsort(data[0])]
    lst = list(data)
    ret = []
    for item in lst:
        ret.append(list(item))

    return ret

def appendToCsvFile(filename, lst):
    '''
    Append new line to old csv, check header matching before calling this
    function
    '''
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(lst)
        return True
    
    return False


def getModelStruct(model_name):
    '''
    Create png for model structure for a specific model
    Return the path to the created file.
    '''
    target_model_obj = NNModelHistory.objects.get(model_name=model_name)
    num_neurons = target_model_obj.num_neurons_layer_str
    num_neurons_arr = [int(item) for item in num_neurons.split(",")]
    model_param = [target_model_obj.input_size] + num_neurons_arr + [1]
    # model path
    base_path = os.path.join(settings.BASE_DIR, 'figures', model_name)
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    model_struct_img_path = os.path.join(base_path, model_name + '.png')
    if os.path.exists(model_struct_img_path):
        os.remove(model_struct_img_path)

    network = plotNN.DrawNN(model_param)
    network.draw(model_struct_img_path)
    return model_struct_img_path


def submitTrainingJob(model_name, user_obj):
    '''
    Submit a training job for the selected model
    '''
    job_id = DataConversion.removeCharFromEmail(user_obj.email) + datetime.now().strftime('%Y%m%d_%H%M%S')
    job_obj = NNJobHistory.objects.create(
        job_id = job_id,
        job_start_time = datetime.now(),
        job_status = 'RUNNING',
        user_created = user_obj.email,
        model_name = model_name
    )
    user_obj.current_running_job_id = job_id
    user_obj.save()
    async_task.trainNetworkByName.delay(NNModelHistory.objects.get(model_name=model_name), job_id)
    return True
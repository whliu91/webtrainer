import csv
from NNModelManager.models import NNModelHistory
import os
import logging

logger = logging.getLogger(__name__)


def validDataRecords(model_obj):
    '''
    Validate data record, try to match file content and db
    results in case there is a change in file.
    '''
    header_str = model_obj.current_data_header
    data_rows = model_obj.data_rows
    data_file_path = model_obj.data_file_path
    if (bool(data_file_path) & os.path.exists(data_file_path)):
        logger.info("data file exist, matching content, model: " + model_obj.model_name)
        with open(data_file_path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            count = 0
            for line in spamreader:
                count += 1
                if count == 1:
                    header_row = line
            count = count - 1
            header_str_ref = ','.join(header_row)
        if (data_rows != count):
            model_obj.data_rows = count
        if (header_str != header_str_ref):
            model_obj.current_data_header = header_str_ref
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


def acceptNewDataFile(model_name, file_path):
    '''
    Accept a new data file for a model that has no previous record
    '''
    logger.info("new data file created for model: " + model_name)
    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        count = 0
        for line in spamreader:
            count += 1
            if count == 1:
                header_row = line
        count = count - 1
        if count > 0:
            logger.info("")
            header_str = ','.join(header_row)
            modelHistory = NNModelHistory.objects.get(model_name=model_name)
            modelHistory.data_rows = count
            modelHistory.current_data_header = header_str
            modelHistory.data_file_path = file_path
            modelHistory.save()
            logger.info("model data saved, model: " + model_name)
            return True
        else:
            logger.warning("new data file contains 0 rows!, model: " + model_name)
            return False
    
    logger.error("cannot open data file! for file: " + file_path)
    return False
import csv
from NNModelManager.models import NNModelHistory
import os


def acceptNewDataFile(model_name, file_path):
    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        count = 0
        for line in spamreader:
            count += 1
            if count == 1:
                header_row = line
        count = count - 1
        header_str = ','.join(header_row)
        modelHistory = NNModelHistory.objects.get(model_name=model_name)
        modelHistory.data_rows = count
        modelHistory.current_data_header = header_str
        modelHistory.save()
        return True
    
    return False
from datetime import datetime

def QuerySetValuesToDictionOfStrings(querySet):
    '''
    Cast a Django Queryset object to a list of rows, where each row is
    a dictionary (key, value pair) for value from database.
    '''
    querySet_list = list(querySet)
    for row_dict in querySet_list:
        for key, value in row_dict.items():
            if isinstance(value, datetime):
                row_dict[key] = value.strftime('%Y-%m-%d')
            else:
                row_dict[key] = str(value)
    
    return querySet_list

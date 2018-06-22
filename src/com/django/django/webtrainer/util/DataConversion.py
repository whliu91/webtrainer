from datetime import datetime

def QuerySetValuesToDictionOfStrings(querySet):
    querySet_list = list(querySet)
    for row_dict in querySet_list:
        for key, value in row_dict.items():
            if isinstance(value, datetime):
                row_dict[key] = value.strftime('%Y-%m-%d')
            else:
                row_dict[key] = str(value)
    
    return querySet_list
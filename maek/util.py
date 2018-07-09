def dict_replace(data: dict, current_value: str, new_value: str):
    """
    Replace {{ PROJECT_PATH }} with the path
    :param data:
    :param current_value:
    :param new_value:
    :return:
    """
    new_data = dict()

    for k, v in data.items():
        if isinstance(v, dict):
            new_data[k] = dict_replace(v, current_value, new_value)
        elif isinstance(v, list):
            new_list = list()
            for value in v:
                new_list.append(value.replace(current_value, new_value))
            new_data[k] = new_list
        elif isinstance(v, str):
            new_data[k] = v.replace(current_value, new_value)
        else:
            new_data[k] = v

    return new_data

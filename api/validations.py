def empty_record_fields(red_flag_latitude, red_flag_longitude, red_flag_desc, user_id, status):
    error = {}
    if not red_flag_latitude:
        error['red_flag_latitude'] = 'Latitude field is missing'
    if not red_flag_longitude:
        error['red_flag_longitude'] = 'Longitude field is missing'
    if not red_flag_desc:
        error['red_flag_desc'] = 'Description cannot be empty'
    if not user_id:
        error['user_id'] = 'user_id field is missing'
    if not status:
        error['status'] = 'Status field is missing'
    return error


def invalid_input_types(red_flag_latitude, red_flag_longitude, red_flag_desc, user_id, status):
    error = {}
    if not isinstance(red_flag_latitude, int):
        error['red_flag_latitude'] = 'should be an integer'
    if not isinstance(red_flag_longitude, int):
        error['red_flag_longitude'] = 'should be an integer'
    if not isinstance(red_flag_desc, str):
        error['red_flag_desc'] = 'should be a string'
    if not isinstance(user_id, int):
        error['user_id'] = 'user_id should be an integer'
    if not isinstance(status, str):
        error['status'] = 'status should be a string'
    return error


def empty_strings_add_red_flag(red_flag_latitude, red_flag_longitude, red_flag_desc, user_id, status):
    error = {}
    if red_flag_latitude == " ":
        error['red_flag_latitude'] = 'Latitude can not be empty'
    if red_flag_longitude == " ":
        error['red_flag_longitude'] = 'Longitude can not be empty'
    if red_flag_desc == " ":
        error['red_flag_description'] = 'Description cannot be empty'
    if status == " ":
        error['status'] = 'Status can not be empty'
    if red_flag_desc ==" ":
        error['red_flag_desc'] = 'Description cant be empty'
    if user_id < 0:
        error['user_id'] = 'user_id cant be less than 0'
    return error

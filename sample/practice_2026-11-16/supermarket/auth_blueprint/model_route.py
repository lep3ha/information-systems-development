from dataclasses import dataclass
from flask import session
from database_clone.select import select_list, select_dict

@dataclass
class ResultInfo:
    result: list
    status: bool
    err_message: str

def define_user(user_input, provider):
    internal_sql = provider.get('internal_user.sql')
    user_info = select_dict(internal_sql, user_input)
    return user_info


def model_route(provider, user_input):
    user_info = define_user(user_input, provider)
    if user_info:
        user_dict = user_info[0]
        session['user_id'] = user_dict['user_id']
        session['user_group'] = user_dict['user_group']
        session.permanent = True
        return ResultInfo(result='OK', status=True, err_message='')
    else:
        return ResultInfo(result='NOT_OK', status=False, err_message='USER_NOT_FOUND')

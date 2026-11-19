from dataclasses import dataclass
from flask import session
from database_clone.select import select_list, select_dict

@dataclass
class ResultInfo:
    result: list
    status: bool
    err_message: str


def model_route(provider, user_dict):
    err_message = ''
    sql = provider.get('internal_user.sql')
    result = select_dict(sql, user_dict)

    if result:
        user_dict = result[0]
        session['user_id'] = user_dict['user_id']
        session['user_group'] = user_dict['user_group']
        session.permanent = True
        return ResultInfo(result=result, status=True, err_message=err_message)
    else:
        return ResultInfo(result=result, status=False, err_message='Данные не получены')
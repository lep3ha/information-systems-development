from dataclasses import dataclass
from database_clone.select import select_list, select_dict

@dataclass
class ResultInfo:
    result: list
    status: bool
    err_message: str


def model_route(provider, user_dict):
    err_message = ''
    sql = provider.get('product.sql')
    result = select_dict(sql, user_dict)

    if result:
        return ResultInfo(result=result, status=True, err_message=err_message)
    else:
        return ResultInfo(result=result, status=False, err_message='Данные не получены')

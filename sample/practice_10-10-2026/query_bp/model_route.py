from dataclasses import dataclass
from database.select import select_dict

@dataclass
class ResultInfo:
    result: list
    status: bool
    err_message: str


def model_route(provider, params):
    q = provider.get('product.sql')
    result = select_dict(q, params)
    err_message = ''

    if result:
        return ResultInfo(result=result, status=True, err_message=err_message)
    else:
        return ResultInfo(result=None, status=False, err_message='Что-то пошло не так')
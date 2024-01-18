import inspect

from exceptions.http import InvalidRequestException


class BaseCRUD():
    def _check_status_code(self, status_code: int):
        method = inspect.stack()[1][3]
        method = " ".join(method.split('_')).title()
        
        if status_code >= 400:
            raise InvalidRequestException(
                prefix=method,
                status_code=status_code
            )

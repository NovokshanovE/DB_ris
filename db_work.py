from typing import Tuple, List
from db_context_manager import DBContextManager


def select(db_config: dict, sql: str) -> Tuple[Tuple, List[str]]:
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.
    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Кортеж с результатом запроса и описанеим колонок запроса.
    """
    result = tuple()
    schema = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)#Метод cursor.execute() выполняет команду SQL.
        # Команды SQL могут быть параметризованными, то есть передаются заполнители вместо литералов SQL.
        schema = [column[0] for column in cursor.description]#Предоставляет имена столбцов последнего запроса.
        # Чтобы оставаться совместимым с API-интерфейсом Python DB,
        # он возвращает кортеж из 7 элементов для каждого столбца,
        # где последние шесть элементов каждого кортежа равны None.
        result = cursor.fetchall()#выбирает все оставшиеся строки результата запроса, возвращая список.
    return result, schema

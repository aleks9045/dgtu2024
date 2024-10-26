from typing import Union, Any, List, Dict

from sqlalchemy import inspect, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute

from database import db_session

Base = db_session.base


class BaseQuery:
    @classmethod
    def get_columns_names(cls, model: Base) -> list[str]:
        inspect_data = inspect(model)
        col_names = [c_attr.key for c_attr in inspect_data.mapper.column_attrs]
        return col_names

    @classmethod
    async def make_one_dict_from_schema(cls, model: Base, schema: dict[str, Any]) -> dict[str, str]:
        data = {}
        col_names = cls.get_columns_names(model)
        for col_name in col_names:
            try:
                data[col_name] = schema[col_name]
            except KeyError:
                continue
        return data

    @classmethod
    async def make_list_of_dicts(cls, data: (), col_names: ()) -> List[Dict[str, Any]]:
        res_lst, temp_dct = [], {}
        for data_row in data:
            for col_num in range(len(col_names)):
                temp_dct[col_names[col_num]] = data_row[col_num]
            res_lst.append(temp_dct)
            temp_dct = {}
        return res_lst

    @classmethod
    async def make_dict(cls, data: (), col_names: ()) -> Dict[str, str]:
        res_dct = {}
        for col_num in range(len(col_names)):
            res_dct[col_names[col_num]] = str(data[col_num])
        return res_dct


class SelectQuery(BaseQuery):

    @classmethod
    async def select(cls, columns: Base, condition: bool,
                     session: AsyncSession) -> Dict[str, str]:
        result = await session.execute(select(columns).where(condition))
        col_names = tuple([*result._metadata.keys])
        data = result.fetchone()
        return await cls.make_dict(data, col_names)

    @classmethod
    async def select_all(cls, columns: Base,
                         order_column: Union[InstrumentedAttribute, Any],
                         session: AsyncSession) -> List[Dict[str, str]]:
        result = await session.execute(select(columns).where(True).order_by(order_column))
        col_names = tuple([*result._metadata.keys])
        data = tuple(result.fetchall())
        return await cls.make_list_of_dicts(data, col_names)

    @classmethod
    async def join_two(cls, model1: Base, model2: Base, condition: bool,
                       col1: Union[InstrumentedAttribute, Any], col2: Union[InstrumentedAttribute, Any],
                       session: AsyncSession, columns1: tuple = (), columns2: tuple = ()):
        if columns1 and columns2:  # if not empty
            query = select(*columns1, *columns2).where(condition).join(model1, col1 == col2)
        elif columns1 and not columns2:
            query = select(*columns1, *model2.__table__.columns).where(condition).join(model1, col1 == col2)
        elif not columns1 and columns2:
            query = select(*model1.__table__.columns, *columns2).where(condition).join(model1, col1 == col2)
        else:
            query = select(*model1.__table__.columns, *model2.__table__.columns).where(condition).join(model1,
                                                                                                       col1 == col2)
        result = await session.execute(query)
        col_names = tuple([*result._metadata.keys])
        data = tuple(result.fetchall())
        return await cls.make_list_of_dicts(data, col_names)

    @classmethod
    async def join_three(cls, session: AsyncSession,
                         model1: Base, model2: Base, model3: Base,
                         condition: bool,

                         col1: Union[InstrumentedAttribute, Any],
                         col2: Union[InstrumentedAttribute, Any],

                         col2_2: Union[InstrumentedAttribute, Any],
                         col2_3: Union[InstrumentedAttribute, Any],
                          columns1: tuple = (), columns2: tuple = (), columns3=()):

        result = await session.execute(select(*columns1, *columns2, *columns3).where(condition).join(model2, col1 == col2).join(model3,
                                                                                                         col2_2 == col2_3))

        col_names = tuple([*result._metadata.keys])
        data = tuple(result.fetchall())
        print(data)
        return await cls.make_list_of_dicts(data, col_names)

    @classmethod
    async def exists(cls, columns: Base, condition: bool, session: AsyncSession) -> bool:
        result = await session.execute(select(columns).where(condition))

        if not result.scalars().all():  # if result is empty
            return False
        return True


class DeleteQuery(BaseQuery):
    @classmethod
    async def delete(cls, model: Base, condition: bool, session: AsyncSession):
        await session.execute(delete(model).where(condition))

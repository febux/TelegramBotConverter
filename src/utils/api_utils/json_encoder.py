import dataclasses
import decimal
from datetime import date, datetime
from enum import Enum
from json import JSONEncoder
from typing import Dict, Any, Union, List, Optional
from uuid import UUID

from pydantic import BaseModel


def to_dict(obj: Any) -> Optional[Dict[str, Any]]:
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, tuple) and hasattr(obj, '_asdict'):  # NamedTuple
        return obj._asdict()  # type: ignore
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    return None


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj: object) -> Union[str, Dict[str, Any], List[Any], None]:
        if isinstance(obj, (decimal.Decimal)):
            return str(obj)
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        if isinstance(obj, datetime):
            return str(obj.isoformat())
        if isinstance(obj, date):
            return str(obj.isoformat())
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Enum):
            return str(obj.value)
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

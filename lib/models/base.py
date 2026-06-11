from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        validate_default=True,
        extra="ignore",
        use_enum_values=True,
        str_strip_whitespace=True,
    )

    def to_dict(self, exclude_none: bool = False, by_alias: bool = True) -> Dict[str, Any]:
        return self.model_dump(exclude_none=exclude_none, by_alias=by_alias)


class BaseRequestSchema(BaseSchema):
    pass

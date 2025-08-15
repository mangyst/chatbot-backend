from pydantic import BaseModel, constr


class DialogNameSchema(BaseModel):
    dialog_name: constr(min_length=3, max_length=20)


class DialogSchema(BaseModel):
    dialog_id: int


class UserDialogMessage(BaseModel):
    dialog_id: int
    text_user: constr(min_length=1, max_length=2000)


class DialogSchemaRename(DialogSchema):
    dialog_name: constr(min_length=3, max_length=20)

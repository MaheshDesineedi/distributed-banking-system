from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BankRequest(_message.Message):
    __slots__ = ("interface", "money", "id")
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    interface: str
    money: int
    id: int
    def __init__(self, interface: _Optional[str] = ..., money: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class BankResponse(_message.Message):
    __slots__ = ("result", "balance", "branch")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    result: str
    balance: int
    branch: int
    def __init__(self, result: _Optional[str] = ..., balance: _Optional[int] = ..., branch: _Optional[int] = ...) -> None: ...

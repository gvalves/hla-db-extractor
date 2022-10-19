from __future__ import annotations

import typing
from typing import Generic, Protocol, Tuple, TypeVar, Union


T = TypeVar('T')


class ListFindPredicate(Protocol, Generic[T]):
    def __call__(self, value: T, index: int, this_list: List[T]) -> bool:
        pass


class List(typing.List[T], Generic[T]):
    def find(self, predicate: ListFindPredicate[T]) -> Union[T, None]:
        for i, v in enumerate(self):
            if predicate(v, i, self):
                return v

    def find_index(self, predicate: ListFindPredicate[T]) -> Union[int, None]:
        for i, v in enumerate(self):
            if predicate(v, i, self):
                return i

    def copy(self) -> List[T]:
        return List[T](self)

    def index(self, value: T) -> Tuple[int, bool]:
        try:
            index = super().index(value)
            exists = True
        except:
            index = 0
            exists = False

        return index, exists

    def contains(self, value: T) -> bool:
        __, exists = self.index(value)
        return exists


class SetFindPredicate(Protocol, Generic[T]):
    def __call__(self, value: T, index: int, this_set: Set[T]) -> bool:
        pass


class SetToDictKeyGen(Protocol, Generic[T]):
    def __call__(self, value: T) -> str:
        pass


class SetFilterPredicate(Protocol, Generic[T]):
    def __call__(self, value: T, index: int, this_set: Set[T]) -> bool:
        pass


class Set(typing.Set[T], Generic[T]):
    def add(self, value: T) -> T:
        super().add(value)
        return self.find(lambda v, __, ___: value == v)

    def find(self, predicate: SetFindPredicate[T]) -> Union[T, None]:
        for i, v in enumerate(self):
            if predicate(v, i, self):
                return v

    def to_dict(self, keygen: SetToDictKeyGen[T]) -> Dict[T]:
        new_dict = Dict[T]()

        for v in self:
            new_dict[keygen(v)] = v

        return new_dict

    def filter(self, predicate: SetFilterPredicate[T]) -> Set[T]:
        new_set = Set[T]()

        for i, v in enumerate(self):
            if predicate(v, i, self):
                new_set.add(v)

        return new_set


class Dict(typing.Dict[str, T], Generic[T]):
    pass

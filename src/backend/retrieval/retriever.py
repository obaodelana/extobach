from abc import ABC, abstractmethod


class Retriever(ABC):
    def __init__(self, product_name: str, release_date: int) -> None:
        assert type(product_name) is str
        assert type(release_date) is int

        self.product_name = product_name
        self.release_date = release_date

    @abstractmethod
    def retrieve(self) -> dict:
        pass

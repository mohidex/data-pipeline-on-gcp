from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime
from .validators import validate_positive_price, validate_non_empty_string

@dataclass
class Product:
    key: str
    name: str
    price: float = field(metadata={'validator': validate_positive_price})
    source: str = field(metadata={'validator': validate_non_empty_string})
    date: datetime = field(default_factory=datetime.now)
    # Product ID attribute with a default value set to a new UUID
    product_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        # Call the validation function after the object is initialized
        self._validate()

    def _validate(self):
        # Validation logic for price and source attributes
        if 'price' in self.__dict__:
            validate_positive_price(self.price)
        if 'source' in self.__dict__:
            validate_non_empty_string(self.source)

    def to_dict(self):
        product_dict = vars(self)

        # parse date that can be easily parsable for go struct marshal
        go_parsable_date = self.date.strftime('%Y-%m-%dT%H:%M:%SZ')
        product_dict.update({'date': go_parsable_date})
        return product_dict
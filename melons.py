"""Classes for melon orders."""
import random
from datetime import datetime


class TooManyMelonsError(ValueError):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class AbstractMelonOrder(object):
    """An abstract base class that other Melon Orders inherit from. """

    def __init__(self, species, qty):
        """Initialize melon order attributes."""

        self.species = species
        self.qty = qty
        self.shipped = False
        if self.qty > 100:
            raise TooManyMelonsError('No more than 100 melons!')

    def get_base_price(self):
        """Generate random base price between $5-9"""
        base_price = random.randint(5, 9)
        now = datetime.now()
        if now.weekday() < 5 and (now.hour >= 8 and now.hour <= 11):
            base_price += 4.00
        return base_price

    def get_total(self):
        """Calculate price, including tax."""
        base_price = self.get_base_price()
        total = (1 + self.tax) * self.qty * base_price

        return total

    def mark_shipped(self):
        """Record the fact than an order has been shipped."""

        self.shipped = True


class DomesticMelonOrder(AbstractMelonOrder):
    """A melon order within the USA."""

    order_type = "domestic"
    tax = 0.08


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""

    order_type = "international"
    tax = 0.17

    def __init__(self, species, qty, country_code):
        """Initialize melon order attributes."""
        super(InternationalMelonOrder, self).__init__(species, qty)
        self.country_code = country_code

    def get_country_code(self):
        """Return the country code."""

        return self.country_code

    def get_total(self):
        """Add $3 if quantity of melons is less than 10"""
        if self.qty < 10:
            super(InternationalMelonOrder, self).get_total() + 3.00
        else:
            super(InternationalMelonOrder, self).get_total()


class GovernmentMelonOrder(AbstractMelonOrder):
    passed_inspection = False
    tax = 0

    def mark_inspection(self, passed):
        """Changes passed_inspection to true if inspection passed"""
        self.passed_inspection = passed

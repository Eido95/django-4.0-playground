import datetime

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class PhysicalAddress:
    """Physical address details"""
    def __init__(self, country, city, street, number):
        self.country, self.city, self.street = country, city, street
        self.number = number

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street}, {self.number}"

    def pretty_print(self):
        return f"{self.number} {self.street}, {self.city}, {self.country}"


class PhysicalAddressField(models.Field):
    description = _("Physical address details "
                    "(Up to: %(max_length)s, excludes: %(separator)s)")

    def __init__(self, separator=",", *args, **kwargs):
        self.separator = separator
        kwargs["max_length"] = 200
        kwargs["help_text"] = self._get_help_text(separator, kwargs)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Drops it from the keyword arguments for readability
        del kwargs["help_text"]
        del kwargs["max_length"]

        # Only include kwarg if it's not the default
        if self.separator != ",":
            kwargs['separator'] = self.separator

        return name, path, args, kwargs

    def from_db_value(self, value: str, expression, connection):
        return value if not value else self._parse_address(value)

    def get_prep_value(self, value):
        # If you override from_db_value() you also have to override
        # get_prep_value() to convert Python objects back to query values.
        return value if not value else self.separator.join(
            [value.country, value.city, value.street, value.number]
        )

    def get_internal_type(self):
        return models.CharField.__name__

    def to_python(self, value: str):
        if isinstance(value, PhysicalAddress) or not value:
            return value
        else:
            return self._parse_address(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def _parse_address(self, address_string: str) -> PhysicalAddress:
        args = address_string.split(self.separator)

        if any(self.separator in arg for arg in args):
            raise ValidationError(
                _(f"Separator ({self.separator}) is not allowed into "
                  f"PhysicalAddress instance")
            )

        args = [arg.strip() for arg in args]

        return PhysicalAddress(*args)

    def _get_help_text(self, separator, kwargs):
        separator += " "
        help_text = "For example: "
        help_text += separator.join(["Israel", "Jerusalem", "Main St.", "30"])
        help_text += f" (Up to {kwargs['max_length']} characters)"

        return help_text

    # You can implement the db_type() method when you’ve created a
    # database custom type.

    # rel_db_type() method is called by fields such as ForeignKey and
    # OneToOneField that point to another field to determine
    # their database column data types

    # get_db_prep_value() is the method where conversions are made to
    # some data types (e.g., dates) that need to be in a specific format
    # before they can be used by a database backend

    # get_db_prep_save() used in case that your custom field needs
    # a special conversion when being saved that is not the same as the
    # conversion used for normal query parameters

    # Use pre_save() If you want to preprocess the value just before saving.

    # To customize the form field used by ModelForm, you can
    # override formfield().


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    opened = models.BooleanField(default=True)
    address = PhysicalAddressField(blank=True)

    def __str__(self):
        return self.question_text

    @admin.display(boolean=True, ordering='pub_date', description='Published recently?')
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

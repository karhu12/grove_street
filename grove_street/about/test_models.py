import pytest

from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from test_utils import create_experience_item, create_expertise_item


@pytest.mark.django_db
@pytest.mark.parametrize(
    "parameter,expected_error",
    [
        ("title", IntegrityError),
        ("role", IntegrityError),
        ("description", IntegrityError),
        ("start_date", IntegrityError),
        ("end_date", None),
        ("category", IntegrityError),
    ],
)
def test_creating_experience_item_without_parameter(
    parameter: str, expected_error: Exception | None
):
    """Attempt to create an experience item without a given parameter."""
    if expected_error is None:
        create_experience_item(**{parameter: None})
    else:
        with pytest.raises(expected_error):
            create_experience_item(**{parameter: None})


class ExperienceItemTestCase(TestCase):
    """Tests related to ExperienceItem model."""

    def test_creating(self):
        """Attempt to create an experience item with necessary information."""
        item = create_experience_item()
        self.assertEqual(item.end_date, None)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "parameter,expected_error",
    [
        ("title", IntegrityError),
        ("category", IntegrityError),
        ("experience_months", IntegrityError),
    ],
)
def test_creating_expertise_item_without_parameter(
    parameter: str, expected_error: Exception | None
):
    """Attempt to create an expertise item without a given parameter."""
    if expected_error is None:
        create_expertise_item(**{parameter: None})
    else:
        with pytest.raises(expected_error):
            create_expertise_item(**{parameter: None})

class ExpertiseItemTestCase(TestCase):
    """Tests related to ExpertiseItem model."""

    def test_creating(self):
        """Attempt to create an expertise item with necessary infomration."""
        item = create_expertise_item()
        self.assertNotEqual(item, None)

    def test_invalid_experience(self):
        """Tests that item with 0 or negative experience can not be created."""
        with transaction.atomic():
            self.assertRaises(IntegrityError, create_expertise_item, experience_months=0)

        with transaction.atomic():
            self.assertRaises(IntegrityError, create_expertise_item, experience_months=-1)

import pytest

from django.test import TestCase
from django.db.utils import IntegrityError

from test_utils import create_experience_item


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

import pytest
from django.test import TestCase

from users.factories import UserFactory


@pytest.mark.django_db
def test_user_is_staff():
    user = UserFactory()
    assert user.is_staff

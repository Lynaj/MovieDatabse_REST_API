from django.test import TestCase

from apps.users.models import User

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        # Set up non-modified User object used by all test methods
        self.test_first_name = "Joe"
        self.test_last_name = "Mark"
        self.test_email = "k23@d.asd"
        self.test_password = "ko12k399asd"

        User.objects.create(
            first_name=self.test_first_name,
            last_name=self.test_last_name,
            email=self.test_email,
            password=self.test_password
        )

    def test_first_name_label(self):
        raise NotImplementedError()

    def test_last_name_label(self):
        raise NotImplementedError()

    def test_mail_label(self):
        raise NotImplementedError()

    def test_first_name_max_length(self):
        raise NotImplementedError()

    def test_last_name_max_length(self):
        raise NotImplementedError()

    def test_email_max_length(self):
        raise NotImplementedError()

    def test_email_format(self):
        raise NotImplementedError()

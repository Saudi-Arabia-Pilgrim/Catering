from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        email = None
        username = "root"
        password = "1"
        full_name = "Super User"

        super_user = get_user_model().objects.create_superuser(
            email=email,
            username=username,
            password=password,
            fullname=full_name,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{super_user} user created successfully"
                f"email = {email}"
                f"username = {username}"
                f"password = {password}"
            )
        )


from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials'

    def handle(self, *args, **options):
        User = get_user_model()
        
        username = 'Mit'
        password = 'mit123'
        email = 'mit@admin.com'
        
        try:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created superuser: {username}')
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Email: {email}')
                )
                self.stdout.write(
                    self.style.SUCCESS('You can now login to Django admin with these credentials')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Superuser {username} already exists - skipping creation')
                )
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {e}')
            )
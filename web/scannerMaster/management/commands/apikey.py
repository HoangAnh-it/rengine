from typing import Any
from rest_framework_api_key.models import APIKey
from django.core.management.base import BaseCommand, CommandError, CommandParser
import uuid


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--create",
            help="Create new api key",
            type=str,
        )

        parser.add_argument(
            "--replace",
            help="Replace existing api key",
            action="store_true",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        create_name = options.get("create", "")

        if not create_name or not create_name.strip():
            self.stderr.write(self.style.ERROR("Error: Name cannot be empty."))
            raise CommandError("Name cannot be empty.")

        create_name = create_name.strip()
        replace = options["replace"]
        if APIKey.objects.filter(name=create_name).exists():
            if replace:
                APIKey.objects.filter(name=create_name).delete()
            else:
                self.stdout.write(self.style.ERROR('API KEY named "%s" already existed' % create_name))
                return

        api_key, generated_key = APIKey.objects.create_key(name=create_name)
        self.stdout.write(self.style.SUCCESS('Create API KEY "%s"' % generated_key))

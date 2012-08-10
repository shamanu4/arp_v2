# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = "Run builtin dhcp server"
    def handle(self, *args, **options):
        from dhcpd import main
        main.run()

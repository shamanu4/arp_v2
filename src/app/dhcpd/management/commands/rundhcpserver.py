# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = "This doesn't do anything yet"
    def handle(self, *args, **options):
        from dhcpd import main
        main.run()
        print 'greatcmd was called'
        # other fancy code here
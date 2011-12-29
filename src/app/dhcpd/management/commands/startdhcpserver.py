# -*- encoding: utf-8 -*-

'''
Created on 22.12.2011

@author: maxim
'''

from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = "This doesn't do anything yet"
    def handle(self, *args, **options):
        from dhcpd import main
        main.run()
        print 'greatcmd was called'
        # other fancy code here
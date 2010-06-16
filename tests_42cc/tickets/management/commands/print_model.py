from django.core.management.base import NoArgsCommand
from django.db import models

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for model in models.get_models():
            print "%s.%s (%d)" % (model.__module__, model.__name__, model._default_manager.count())
            
        


from django.db import models
from tests_42cc.tickets.models import ModelActionLogEntry

MODEL_TRACKER_IGNORE_LIST = ['ModelActionLogEntry', 'HttpRequestLogEntry']

def check_instance(instance):
    return not (instance.__class__.__name__ in MODEL_TRACKER_IGNORE_LIST)
    
def model_object_changed_handler(instance, created, **kwargs):
    if not check_instance(instance):
        return
        
    action_log = ModelActionLogEntry(
        model_class=instance.__class__.__name__,
        model_module=instance.__class__.__module__,
        model_id=instance.pk)
    
    if created:
        action_log.action = ModelActionLogEntry.ACTION_INSERT
    else:
        action_log.action = ModelActionLogEntry.ACTION_EDIT
        
    action_log.save()
        
def model_object_delete_handler(instance, **kwargs):
    if not check_instance(instance):
        return
        
    action_log = ModelActionLogEntry(
        model_class=instance.__class__.__name__,
        model_module=instance.__class__.__module__,
        model_id=instance.pk,
        action=ModelActionLogEntry.ACTION_DELETE)
    action_log.save()
        


def start_default_listening():
    models.signals.post_save.connect(model_object_changed_handler)
    models.signals.post_delete.connect(model_object_delete_handler)
    

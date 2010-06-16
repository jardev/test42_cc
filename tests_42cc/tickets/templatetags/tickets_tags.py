from django import template
from django.core.urlresolvers import reverse

register = template.Library()

def build_object_link(value):
    url = reverse('admin:%s_%s_change' % (value._meta.app_label,  value._meta.module_name),  args=[value.id])
    return u'<a href="%s">Edit %s</a>' % (url, value.__unicode__())
    
class BuildObjectLinkNode(template.Node):
    def __init__(self, object):
        self.object = template.Variable(object)
        
    def render(self, context):
        try:
            actual_object = self.object.resolve(context)
            return build_object_link(actual_object)
        except:
            return 'error'
            
@register.tag
def edit_object(parser, token):
    try:
        tag_name, object = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return BuildObjectLinkNode(object)
  


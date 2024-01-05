from django import template

register = template.Library()

@register.filter(name='add_default')
def add_default(value):
    if value == None or value == '':
        value = 0
    else:
        pass
    
    return value

@register.filter(name='devide')
def devide(a,b):
    return a/b
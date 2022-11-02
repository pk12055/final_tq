from django import template
import ast

register = template.Library()

@register.filter(name='split')
def split(value, key):
  """
    Returns the value turned into a list.
  """
  return value.split(key)


@register.filter(name='dict')
def dict(value):
  """
    Returns the value turned into a list.
  """
  return ast.literal_eval(value)


@register.filter(name='value')
def value(dictionary, key):
    return dictionary.get(key)
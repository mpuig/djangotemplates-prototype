from django import template
import random

register = template.Library()

@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return [`num` for num in range( 1, value+1 )]
  
class ImageNode(template.Node):
  def __init__(self, width, height):
      self.width, self.height = width, height

  def render(self, context):
      return u'<img src="/static/img/img%d.jpeg" width=%s height=%s />' % (random.randint(1, 5), self.width, self.height)
      
def image(parser, token):
  """
  Creates random Latin text useful for providing test data in templates.

  Usage format::

      {% image [width] [height] %}

  ``width`` is the image width, in pixels (default is 100).

  ``height`` is the image height, in pixels (default is 100).

  Examples:
      * ``{% image %}`` will output the default 100x100 image
      * ``{% lorem 300 %}`` will output a 300x100 image
      * ``{% lorem 300 500 %}`` will output a 300x500 image
  """
  
  bits = list(token.split_contents())
  tagname = bits[0]
  width = bits[1]
  height = bits[2]
  
  if len(bits) != 3:
      raise template.TemplateSyntaxError("Incorrect format for %r tag" % tagname)
  return ImageNode(width, height)
image = register.tag(image)

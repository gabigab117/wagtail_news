from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Advert(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    text = models.TextField()

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
        FieldPanel("text")
    ]

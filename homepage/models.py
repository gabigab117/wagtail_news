from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class IndexPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("body")
    ]

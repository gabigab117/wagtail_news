from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")


class FormPage(AbstractEmailForm):
    thank_you_text = RichTextField()

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('form_fields', label="Champs"),
        FieldPanel("thank_you_text"),

        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("from_address", classname="col6"),
                FieldPanel("to_address", classname="col6"),
            ]),
            FieldPanel("subject"),
        ], "Email"),
    ]

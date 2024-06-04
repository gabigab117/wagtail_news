from django.db import models
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index


class ArticleIndexPage(Page):
    intro = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("intro")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        articles = ArticlePage.objects.child_of(self).live().order_by("-date")
        context["articles"] = articles
        return context


class ArticlePage(Page):
    date = models.DateField(verbose_name="Date de publication")
    intro = RichTextField()
    body = StreamField([
        ("paragraphe", blocks.RichTextBlock()),
        ("image", ImageChooserBlock()),
        ("url", blocks.URLBlock()),
        ("citation", blocks.BlockQuoteBlock())
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body")
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
        index.SearchField("intro")
    ]

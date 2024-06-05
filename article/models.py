from django.db import models
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page, ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


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


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey("ArticlePage", related_name="tagged_items", on_delete=models.CASCADE)


class ArticlePage(Page):
    date = models.DateField(verbose_name="Date de publication")
    intro = RichTextField()
    body = StreamField([
        ("paragraphe", blocks.RichTextBlock()),
        ("image", ImageChooserBlock()),
        ("url", blocks.URLBlock()),
        ("citation", blocks.BlockQuoteBlock())
    ], use_json_field=True)
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    advert = models.ForeignKey("advert.Advert", null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="+")

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("tags"),
        FieldPanel("advert")
    ]

    search_fields = Page.search_fields + [
        index.SearchField("body"),
        index.SearchField("intro")
    ]


class ArticleTagIndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        tag = request.GET.get("tag")
        articlepages = ArticlePage.objects.filter(tags__name=tag)
        context = super().get_context(request, *args, **kwargs)
        context["articlepages"] = articlepages
        return context

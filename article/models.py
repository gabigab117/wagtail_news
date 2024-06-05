from django.db import models
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page, ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.snippets.models import register_snippet

User = get_user_model()


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

    def serve(self, request, *args, **kwargs):
        from .forms import CommentForm

        comments = self.comments.all()

        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user, comment.page = request.user, self
                comment.save()
                return HttpResponseRedirect(request.path)
        else:
            form = CommentForm()
        return render(request, "article/article_page.html", context={"page": self, "form": form,
                                                                     "comments": comments})


class ArticleTagIndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        tag = request.GET.get("tag")
        articlepages = ArticlePage.objects.filter(tags__name=tag)
        context = super().get_context(request, *args, **kwargs)
        context["articlepages"] = articlepages
        return context


@register_snippet
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    page = models.ForeignKey("article.ArticlePage", on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(verbose_name="Commentaire")

    def __str__(self):
        return f"{self.user} - {self.page.title}"

    panels = [
        FieldPanel("user"),
        FieldPanel("text"),
        FieldPanel("page")
    ]

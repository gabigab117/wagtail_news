from django.shortcuts import render

from wagtail.models import Page
from wagtail.contrib.search_promotions.models import Query


def search_view(request):
    search_query = request.GET.get('query', None)
    if search_query:
        search_results = Page.objects.live().search(search_query)
    else:
        search_results = Page.objects.none()

    return render(request, "search/search.html", context={"search_query": search_query,
                                                          "search_results": search_results})

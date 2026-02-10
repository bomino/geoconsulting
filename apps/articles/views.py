from django.views.generic import DetailView, ListView

from apps.articles.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "articles/list.html"
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):
        return Article.objects.filter(published=True)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.filter(published=True)

from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from codeshare.models import Snippet
from django.urls import path


snippet_info = {'queryset': Snippet.objects.all()}
urlpatterns = [
    #path('', snippets.snippets_list, name="codeshare_snippet_list"),
    path('', object_list, dict(snippet_info, paginate_by=20),
         name='codeshare_snippet_list'),
    #path('<int:snippet_id>/', snippets.snippet_detail, name='cab_snippet_delatil')
    path('<int:object_id>/', object_detail,
         snippet_info, name='codeshare_detail'),
]

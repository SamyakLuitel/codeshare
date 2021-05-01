from django.shortcuts import get_object_or_404

from .models import Language as Language
from django.views.generic.list_detail import object_list


def language_details(reuest, slug):
    language = get_object_or_404(Language, slug=slug)
    return object_list(request, queryst=language.snippet_set.all(), paginate_by=20, template_name='codeshare/lanuage_detail.html', extra_content={'laguage': language})

from django.db import models
from pygments import lexers, formatters, highlight
# from tagging.fields import TagField
# tagging module is depricated
from taggit.managers import TaggableManager
# do not forget to add this to installed app in settings
from django.contrib.auth.models import User
from markdown import markdown
import datetime

from django.urls import reverse
# Create your models here.

'''pygments works by reading through a piece of text while using a specialized piece
of code called a lexer, which knows the rules of the particular programming language the text
is written in.'''


class Language(models.Model):
    '''the language model is present to identify different programming languags  '''
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    # A slug is the last part of the url containing a unique string which
    # identifies the resource being served by the web service.
    # In that sense, a slug is a unique identifier for the resource.
    language_code = models.CharField(max_length=50)
    # A MIME type is a label used to identify a type of data
    mime_type = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']  # ordering is done alphabetically

        def __unicode__(self):
            return self.names

        def get_absolute_url(self):
            # return ('cab_laguage_details', (), {'slug': self.slug})
            return reverse('cab_laguage_details', (), {'slug': self.slug})
            #get_absolute_url = models.permalink(get_absolute_url)
            # permalink is now depricated

        def get_lexer(self):
            return lexers.get_lexer_by_name(self.language_code)
            '''pygments works by reading through a piece of text while using a specialized piece
            of code called a lexer, which knows the rules of the particular programming language the text
            is written in.'''


class snippet(models.Model):
    title = models.CharField(max_length=255)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    descriptipn_html = models.TextField(editable=False)
    code = models.TextField()
    highlighted_code = models.TextField(editable=False)
    #tags = TagField()
    tags = TaggableManager()
    pub_date = models.DateTimeField(editable=False)
    updated_date = models.DateTimeField(editable=False)

    class Meta:
        ordering = ['-pub_date']  # ordering based on published date

        def __unicode__(self):
            return self.title

        def save(self, force_insert=False, force_update=False):
            if not self.id:
                self.pub_date = datetime.datetime.now()
            self.updated_date = datetime.datetime.now()
            self.description_html = markdown(Self.description)
            self.highlighted_code = self.highlight()
            super(Snippet, self).save(force_insert, force_update)

        def get_absolute_url(self):
            # return ('codeshare_snippet_detail', (), {'objective_id': self.id})
            #get_absolute_url = models.permalink(get_absolute_url())
            return reverse('codeshare_snippet_detail', (), {'objective_id': self.id})

        def highlight(self):
            return highlight(self.code, self.language.get_lexer(), formatters.HtmlFormatter(linenos=True))

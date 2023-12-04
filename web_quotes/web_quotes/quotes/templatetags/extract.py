from bson.objectid import ObjectId

from django import template

from ..models import Author, Tag, Quote

register = template.Library()


def get_author(author_id):
    author = Author.objects.filter(id=author_id).first()
    
    return author.fullname

register.filter("author", get_author)
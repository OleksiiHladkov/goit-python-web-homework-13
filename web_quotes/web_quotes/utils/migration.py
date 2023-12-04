import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_quotes.settings")
django.setup()


from quotes.models import Quote, Tag, Author
from quotes.utils import get_mongodb


db = get_mongodb()

authors = db.author.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author["fullname"],
        born_date=author["born_date"],
        born_location=author["born_location"],
        description=author["description"],
    )


quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote["tags"]:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = bool(len(Quote.objects.filter(quote=quote["qoute"])))

    if not exist_quote:
        author = db.author.find_one({"_id": quote["author"]})
        a = Author.objects.get(fullname=author["fullname"])
        q = Quote.objects.create(quote=quote["qoute"], author=a)
        for tag in tags:
            q.tags.add(tag)

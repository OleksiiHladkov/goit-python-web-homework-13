import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_quotes.settings")
django.setup()


from quotes.models import Quote, Tag, Author

quotes = Quote.objects.all()

for i in quotes:
    print(type(i))
    break

# author = Author.objects.first()
# print(type(author.id))
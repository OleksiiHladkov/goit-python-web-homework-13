from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View

from .models import Author, Tag, Quote
from .forms import AddQuoteForm, AddAuthorForm, AddTagForm


# Create your views here.
def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


def author(request, id):
    author = Author.objects.filter(id=id).first()
    return render(request, "quotes/author.html", context={"author": author})


@login_required
def add_quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.author = Author.objects.filter(
                id=request.POST.get("author")
            ).first()
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to="quotes:main")
        else:
            return render(
                request,
                "quotes/add_quote.html",
                {"tags": tags, "authors": authors, "form": form},
            )

    return render(
        request,
        "quotes/add_quote.html",
        {"tags": tags, "authors": authors, "form": AddQuoteForm()},
    )


@login_required
def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/add_author.html", {"form": form})

    return render(request, "quotes/add_author.html", {"form": AddAuthorForm()})


@login_required
def add_tag(request):
    if request.method == "POST":
        form = AddTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/add_tag.html", {"form": form})

    return render(request, "quotes/add_tag.html", {"form": AddTagForm()})

from django import forms

from .models import Author, Tag, Quote


class AddQuoteForm(forms.ModelForm):
    quote = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = Quote
        fields = ["quote"]
        exclude = ["tags", "author"]


class AddAuthorForm(forms.ModelForm):
    fullname = forms.CharField(max_length=50, required=True)
    born_date = forms.CharField(max_length=50)
    born_location = forms.CharField(max_length=150)
    description = forms.TextInput()

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class AddTagForm(forms.ModelForm):
    name = forms.CharField(max_length=40, required=True)

    class Meta:
        model = Tag
        fields = ["name"]

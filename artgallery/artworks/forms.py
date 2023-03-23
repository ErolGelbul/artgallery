from django.forms import ModelForm
from django import forms
from .models import Artwork, Review


class ArtworkForm(ModelForm):
    class Meta:
        model = Artwork
        fields = [
            "title",
            "featured_image",
            "description",
            "demo_link",
            "source_link",
            "tags",
        ]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ArtworkForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["value", "body"]
        labels = {"value": "Place your vote", "body": "Add a comment with your vote"}

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})

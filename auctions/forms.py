from django import forms
from .models import Subasta

class ListingForm(forms.ModelForm):
    class Meta:
        model = Subasta
        text = forms.CharField(widget=forms.Textarea())
        fields = [
            'title',
            'text',
            'starting_bid',
            'image_url',
            'category',
        ]

class NewListing(forms.Form):
    class Meta:
        model = Subasta
        title = forms.CharField()
        description = forms.CharField(widget=forms.Textarea())
        bid = forms.IntegerField()
        image_url = forms.CharField(required=False)
        category = forms.CharField(required=False)

class NewBiding(forms.Form):
    new = forms.IntegerField()
from django import forms

class RatingForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        required=True,
        widget=forms.NumberInput(attrs={"class": "rating-input", "step": "1"}),
    )
    reservation_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is None:
            raise forms.ValidationError("Rating is required.")
        return rating
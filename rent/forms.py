from django import forms
from django.utils.translation import gettext as _
class RatingForm(forms.Form):
    number_of_milage = forms.DecimalField(required=True,)
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        required=True,
        widget=forms.HiddenInput(),  # Hide the default input, we'll use stars
    )
    reservation_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is None:
            raise forms.ValidationError(_("Rating is required."))
        return rating
    def clean_number_of_milage(self):
        number_of_milage = self.cleaned_data.get("number_of_milage")
        if number_of_milage is None:
            raise forms.ValidationError(_("number of mileage is required."))
        return number_of_milage
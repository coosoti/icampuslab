from datetime import datetime
from django import forms


from .models import Career

class CareerForm(forms.ModelForm):
	class Meta:
		publish = forms.DateField(widget=forms.SelectDateWidget,)
		model = Career
		fields = [
			"title",
			"category",
			"image",
			"description",
			"entry",
			"experience",
			"education",
			"draft",
			"publish",
		]
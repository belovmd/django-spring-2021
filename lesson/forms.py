from django import forms

from . import models


class EmailMaterialForm(forms.Form):
    my_name = forms.CharField(max_length=20)
    to_email = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea)


class MaterialForm(forms.ModelForm):
    class Meta:
        model = models.Material
        fields = ('title', 'body', 'material_type')

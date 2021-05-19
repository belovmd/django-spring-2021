from django import forms


class EmailMaterialForm(forms.Form):
    my_name = forms.CharField(max_length=20)
    to_email = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea)

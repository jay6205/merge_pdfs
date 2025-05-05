from django import forms

class PDFMergeForm(forms.Form):
    pdfs = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)

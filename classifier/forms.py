from django import forms

from classifier.models import Column, Classification, Source


class ColumnClassifierForm(forms.ModelForm):
    index = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Column
        fields = ["index", "main_class", "sub_class"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sub_class"].queryset = Classification.objects.none()


class SourceUploadForm(forms.Form):
    document = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True})
    )

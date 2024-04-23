from django import forms
from .models import Music

class MusicUploadForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'id': 'music-file', 'accept': 'audio/*'}),
        }

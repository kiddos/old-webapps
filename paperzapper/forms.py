from django import forms

from .models import Paper, User


class PaperForm(forms.ModelForm):
  class Meta:
    model = Paper
    fields = ('title', 'document', 'notes')

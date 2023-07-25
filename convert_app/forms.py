from django import forms

FORMAT_CHOICES = [
    ('JPEG', 'JPEG'),
    ('PNG', 'PNG'),
    ('WEBP', 'WEBP'),
    # добавьте другие форматы, если нужно
]

class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    current_format = forms.ChoiceField(choices=FORMAT_CHOICES)
    new_format = forms.ChoiceField(choices=FORMAT_CHOICES)

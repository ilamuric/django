from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.files.base import ContentFile
from .forms import ImageUploadForm
from PIL import Image as PilImage
import os
import io

from django.core.files.storage import default_storage

def convert_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data['image']
            current_format = form.cleaned_data['current_format']
            new_format = form.cleaned_data['new_format']
            
            if not img.name.endswith(current_format.lower()):
                return render(request, 'error.html', {'message': 'Image format doesn\'t match selected.'})  # замените на ваш шаблон
            
            pil_image = PilImage.open(img)
            output = io.BytesIO()
            pil_image.save(output, format=new_format)
            output.seek(0)
            img.name = f"converted_image.{new_format.lower()}"
            img.file = ContentFile(output.read())

            # Save the file
            file_name = default_storage.save(img.name, img.file)
            file_url = default_storage.url(file_name)
            
            # затем передайте file_url в контекст вашего шаблона
            return render(request, 'success.html', {'file_url': file_url})
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})  # замените на ваш шаблон


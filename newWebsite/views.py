from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.core.urlresolvers import reverse

#for etag decorator
from django.views.decorators.http import etag
import hashlib

#to validate placeholder data
from .forms import ImageForm


def index(request):
    example = reverse('placeholder', kwargs={'width':50, 'height':50})
    context = {'example': request.build_absolute_uri(example)}
    return render(request, 'index.html', context)

def generate_etag(request, height, width):
    content = 'Placeholder: {0}x{1}'.format(height, width)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()

@etag(generate_etag)
def placeholder(request, width, height):
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest('Invalid Image Parameters')
    return HttpResponse('OK')


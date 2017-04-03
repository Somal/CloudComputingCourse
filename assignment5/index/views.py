import json

from django.shortcuts import render

from .models import Voice


def main(request):
    # return render(request, 'static/index.html')
    if request.method == 'POST':
        data = request.POST['data']
        data = json.loads(data)
        voice_id = Voice.get_max_id() + 1
        for k, v in data.items():
            Voice.objects.create(voice_id=voice_id, key=k, value=v)
    return render(request, 'index.html')


def results(request):
    return render(request, 'results.html', content={'entries': {'data': []}})

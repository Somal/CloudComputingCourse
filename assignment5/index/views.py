from django.shortcuts import render


def main(request):
    # return render(request, 'static/index.html')
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'index.html')


def results(request):
    return render(request, 'results.html', content={'entries': {'data': []}})

from django.shortcuts import render


def main(request):
    # return render(request, 'static/index.html')
    return render(request, 'index.html')

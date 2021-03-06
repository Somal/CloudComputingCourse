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
            if isinstance(v, list):
                for vv in v:
                    Voice.objects.create(voice_id=voice_id, key=k, value=vv)
            else:
                Voice.objects.create(voice_id=voice_id, key=k, value=v)
    return render(request, 'index.html')


def results(request):
    max_id = Voice.get_max_id()
    data = []
    for id in range(max_id + 1):
        rows = Voice.objects.filter(voice_id=id)
        if len(rows)>0:
            data.append({r.key: r.value for r in rows})

    context = {"data": [], "statistics": {}}
    print(data)
    if data.__len__() > 0:
        question1 = [int(v.value) for v in Voice.objects.filter(key='question1')]
        mean = sum(question1) / len(question1) * 1.0

        # Statistics
        # Question 4
        question4_distribution = {"1": 0, "2": 0, "3": 0}
        for voice in Voice.objects.filter(key='question4'):
            question4_distribution[voice.value] += 1

        question4_count = len(Voice.objects.filter(key='question4'))
        for k in question4_distribution.keys():
            question4_distribution[k] = question4_distribution[k] / question4_count

        # Question 5
        question5_distribution = {"1": 0, "2": 0}
        for voice in Voice.objects.filter(key='question5'):
            question5_distribution[voice.value] += 1

        question5_count = len(Voice.objects.filter(key='question5'))
        for k in question5_distribution.keys():
            question5_distribution[k] = question5_distribution[k] / question5_count

        statistics = {'Distribution_of_answers_on___would_you_like': question4_distribution,
                      'Distribution_of_answers_on___recommend': question5_distribution}

        # Renaming
        names = {"question1": "Rate this project form 0 to 10",
                 "question2": "Can you briefly describe your experience in this project?",
                 "question3": "Tell us about the issues you faced while using the application",
                 "question4": "How often would you like to use this service?",
                 "question5": "Would you recommend this project to your friends ?"}
        renamed_data = []
        for d in data:
            tmp = {}
            for k, v in d.items():
                tmp[names[k]] = v
            renamed_data.append(tmp)
        context = {'data': renamed_data, 'mean': mean, 'statistics': statistics}
    return render(request, 'results.html', context=context)

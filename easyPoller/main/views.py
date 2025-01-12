from django.shortcuts import render, redirect
from .models import Poll, AnswerOptions
import json
from django.http import HttpResponse, JsonResponse

# Create your views here.

def index(request):
    if request.method == "POST":
        data = json.loads(request.body)

        new_poll = Poll(
            title = data.get("question")[0]
        )

        new_poll.save()

        for answer in data.get("answer_option"):
            a = AnswerOptions(poll=new_poll, option=answer, votes=0)
            a.save()

        return JsonResponse(new_poll.id, safe=False)


    polls = Poll.objects.all()
    return render(request, 'index.html', {'polls':polls})


def poll_view(request, id):
    poll = Poll.objects.filter(id=id).first()
    answers = AnswerOptions.objects.filter(poll=poll)
    return render(request, 'poll.html', {'poll': poll, 'answers':answers})

def vote(request):
    if request.method == "POST":
        ao = AnswerOptions.objects.filter(id=int(request.POST.get("answer_option_id"))).first()
        ao.votes += 1
        ao.save()

        return HttpResponse(200)




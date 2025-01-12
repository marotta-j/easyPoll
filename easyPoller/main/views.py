from django.shortcuts import render
from .models import Poll, AnswerOptions
import json

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


    polls = Poll.objects.all()
    return render(request, 'index.html', {'polls':polls})


def poll_view(request, id):
    poll = Poll.objects.filter(id=id).first()
    answers = AnswerOptions.objects.filter(poll=poll)
    print(poll)
    print(answers)
    return render(request, 'poll.html', {'poll': poll, 'answers':answers})




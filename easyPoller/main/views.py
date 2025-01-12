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

def results_view(request, id):
    poll = Poll.objects.filter(id=id).first()
    answers = AnswerOptions.objects.filter(poll=poll)
    return render(request, 'results.html', {'poll': poll, 'answers':answers})

def vote(request):
    if request.method == "POST":
        # get the vote_id so we can find that item and increment the votes on it
        vote_id = int(request.POST.get("answer_option_id"))
        ao = AnswerOptions.objects.filter(id=vote_id).first()
        poll_id = ao.poll.id

        # Check if we have voted on this poll already
        if request.session.get(f'voted_in_{poll_id}', False):
            return HttpResponse(403)
        else:
            ao.votes += 1
            ao.save()

            # Mark down that we voted
            request.session[f'voted_in_{str(poll_id)}'] = True

            return HttpResponse(200)




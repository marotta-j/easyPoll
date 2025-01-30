from django.shortcuts import render, redirect
from .models import Poll, AnswerOptions
import json
from django.http import HttpResponse, JsonResponse, Http404

# Create your views here.

def index(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("question")[0]

        # Server-side check for 200 max characters
        if len(title) > 200:
            return JsonResponse({'error':'The poll title is too long! (Max 200 characters)'}, status=400)

        new_poll = Poll(
            title = title
        )

        new_poll.save()

        for answer in data.get("answer_option"):
            # Check if all answer options are under 100 characters
            if len(answer) > 100:
                return JsonResponse({'error': 'One of your answer options is too long! (Max 100 characters)'}, status=400)
            a = AnswerOptions(poll=new_poll, option=answer, votes=0)
            a.save()

        return JsonResponse(new_poll.slug, safe=False)


    polls = Poll.objects.all()
    return render(request, 'index.html', {'polls':polls})


def poll_view(request, slug):
    poll = Poll.objects.filter(slug=slug).first()
    answers = AnswerOptions.objects.filter(poll=poll)

    # If either doesn't exist return 404
    if not poll or not answers:
        raise Http404("Poll not found")

    return render(request, 'poll.html', {'poll': poll, 'answers':answers})

def results_view(request, slug):
    poll = Poll.objects.filter(slug=slug).first()
    answers = AnswerOptions.objects.filter(poll=poll)

    # If either doesn't exist return 404
    if not poll or not answers:
        raise Http404("Poll not found")

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




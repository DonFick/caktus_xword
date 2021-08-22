import random
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Max
from xword_data.models import Clue
from xword_data.forms import AnswerForm

def get_random_clue():
    # we want a reasonably efficient way to select a random record
    # without pulling them all from the database in a large queryset
    # and we don't want to clobber the server with .order_by('?').first()
    # the dataset is non-volatile so we can us the primary key
    # but just in case we have some gaps, we can loop until we hit a good record
    max_id = Clue.objects.all().aggregate(max_id=Max('id'))['max_id']
    while True:
        pk = random.randint(1, max_id)
        clue = Clue.objects.filter(pk=pk).first()
        if clue:
            return clue

def Drill(request):
    # We use session middleware to track performance statistics
    clue_count = request.session.get('clue_count', 0)
    guess_count = request.session.get('guess_count', 0)
    context={}
    if request.method == 'POST':
        # We are evaluating a answer
        form = AnswerForm(request.POST)
        if form.is_valid():
            context['form'] = form
            guess_count += 1
            request.session['guess_count'] = guess_count
            guess = form.cleaned_data['answer'].upper().strip()
            clue_id = int(form.cleaned_data['clue_id'])
            clue = Clue.objects.filter(pk=clue_id).first()
            if not clue:
                errorcode = 1 #'Sorry, we lost the clue. Let's start again.'
                return render(request, 'unexpected_error.html', {'errorcode':errorcode})
            else:
                context['clue'] = clue
                if guess == clue.entry.entry_text:
                   message = 'Success. That is the correct entry.'
                   return HttpResponseRedirect('/answer')
                else:
                    context['message'] = 'Sorry, answer again.'
                    return render(request, 'drill.html', context)

        else:
            errorcode = 2  # 'Sorry, invalid form.'
            return render(request, 'unexpected_error.html', {'errorcode': errorcode})

    else:
        # we are presenting a new clue
        # Let's find a random clue
        clue = get_random_clue()
        clue_count += 1
        request.session['clue_count'] = clue_count
        form = AnswerForm(initial={'answer': '', 'clue_id':clue.id})

        context = {
            'form':form,
            'clue_count':clue_count,
            'guess_count': guess_count,
            'clue': clue,
        }

        return render(request, 'drill.html', context)

def Answer(request):
    context={}
    return render(request, 'answer.html', context)

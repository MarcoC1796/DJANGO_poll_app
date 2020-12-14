from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.views import generic

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html' # change the default: <app name>/<model name>_list.html
    context_object_name = 'latest_question_list' # changes default context variable (context_object_name): question_list

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

# expects pk to retrieve the particular item
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html' #change the default: <app name>/<model name>_detail.html

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# solve race problem
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
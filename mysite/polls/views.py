from datetime import date

from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from polls.models import Question, Choice

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        context = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def field_lookup_complex():
    # Roughly: SELECT * FROM polls_question
    # WHERE (
    #   question_text LIKE 'Who%'
    #   AND (pub_date = '2005-05-02 00:00:00'
    #       OR pub_date = '2005-05-06 00:00:00'))
    Question.objects.filter(
        Q(question_text__startswith='Who'),
        Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
    )

    # Roughly: equivalent to above query
    Question.objects.get(
        Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
        question_text__startswith='Who',
    )

    # Roughly: SELECT * FROM polls_question
    # WHERE (
    #   question_text LIKE 'Who%'
    #   OR NOT (pub_date BETWEEN '2005-01-01 00:00:00' AND '2005-12-31 23:59:59.999999')
    Question.objects.filter(
        Q(question_text__startswith='Who') | ~Q(pub_date__year=2005)
    )

    # Roughly: SELECT * FROM polls_question
    # WHERE (
    #   question_text LIKE 'Who%'
    #   AND NOT (pub_date BETWEEN '2005-01-01 00:00:00' AND '2005-12-31 23:59:59.999999')
    Question.objects.filter(
        Q(question_text__startswith='Who') & ~Q(pub_date__year=2005)
    )


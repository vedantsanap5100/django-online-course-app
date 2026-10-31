from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Course, Question, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        submission = Submission.objects.create(enrollment=course)
        selected_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_ids.append(int(value))
        submission.choices.set(selected_ids)
        return redirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    score = 0
    total_score = 0
    for question in course.question_set.all():
        total_score += question.grade
        selected_choices = submission.choices.filter(question=question)
        selected_ids = [choice.id for choice in selected_choices]
        if question.is_get_score(selected_ids):
            score += question.grade
    context = {
        'course': course,
        'submission': submission,
        'score': score,
        'total_score': total_score
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

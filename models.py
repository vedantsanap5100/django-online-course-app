from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Course(models.Model):
    name = models.CharField(max_length=30, default='online course')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = models.BooleanField(default=False)

    def __str__(self):
        return "Name: " + self.name + ", Description: " + self.description


class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    content = models.TextField()


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).values_list('id', flat=True)
        selected_ids = set(selected_ids)
        if set(all_answers) == selected_ids:
            return True
        return False


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Course, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

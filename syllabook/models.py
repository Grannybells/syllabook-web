from email.policy import default
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.

class Post(models.Model):
    course_code = models.CharField("Course code",max_length=100)
    course_name = models.CharField("Course name",max_length=100)
    credits = models.CharField("Credits",max_length=100)
    contact_hours = models.CharField("Hours",max_length=100)
    instructor = models.CharField("Professor",max_length=100)
    position = models.CharField("Position",max_length=100)
    textbook = RichTextField("Text books",blank=True, null=True)
    other_supplementary_material = RichTextField("Other materials",blank=True, null=True)
    course_description = RichTextField("Course Description",blank=True, null=True)
    prerequisites = models.CharField("Prerequisite",max_length=100)
    corequisites = models.CharField("Corequisite",max_length=100)
    course_classification = models.CharField("Course classification",max_length=100)
    course_objective = RichTextField("Course objective",blank=True, null=True)
    course_outcomes = RichTextField("Course outcome",blank=True, null=True)
    student_outcome_addressed_by_the_course = RichTextField("Student outcome",blank=True, null=True)
    course_topics = RichTextField("Topics",blank=True, null=True)
    prepared = models.CharField("Created by",max_length=100)
    noted = models.CharField("Noted by",max_length=100)
    marked = models.CharField("Signed by",max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.course_code

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})

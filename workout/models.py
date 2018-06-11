# coding=utf-8
# Python imports
# Django imports
from django.db import models
from django.core.urlresolvers import reverse
# Third party app imports
# Local app imports


# Funciones cross del modelo
def upload_routine_image(filename):
	return 'workout/routines/' + filename


def upload_exercise_image(filename):
	return 'workout/exercises/' + filename


# Create your models here.
class BodyPart(models.Model):
	id = models.SlugField(primary_key=True, max_length=60)
	name = models.CharField(null=False, blank=False, max_length=100, default='none')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	image = models.ImageField(upload_to=upload_exercise_image, null=False, blank=False)
	
	def __unicode__(self):
		return self.name
	
	def __str__(self):
		return self.name
	

class Exercise(models.Model):
	id = models.SlugField(primary_key=True, max_length=60)
	name = models.CharField(null=False, blank=False, max_length=100, default='none')
	description = models.TextField(null=False, blank=False, max_length=600, default='none')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	image = models.ImageField(upload_to=upload_exercise_image, null=False, blank=False)
	main_muscles = models.ManyToManyField('workout.BodyPart', related_name='main_muscles')
	other_muscles = models.ManyToManyField('workout.BodyPart', related_name='other_muscles')
	
	def __unicode__(self):
		return self.name
		
	def __str__(self):
		return self.name

		
class ExerciseSet(models.Model):
	exercise = models.ForeignKey('workout.Exercise', null=True, on_delete=models.CASCADE)
	reps = models.PositiveIntegerField()
	kgs = models.PositiveIntegerField()
	rest = models.PositiveIntegerField()


class Routine(models.Model):
	TYPE_ROUTINE = (('BU', 'Bulking'), ('CU', 'Cutting'), ('MA', 'Maintaining'),)

	id = models.SlugField(primary_key=True, max_length=60)
	name = models.CharField(null=False, blank=False, max_length=100, default='none')
	description = models.TextField(null=False, blank=False, max_length=600, default='none')
	type = models.CharField(max_length=2, choices=TYPE_ROUTINE, default='MA')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	image = models.ImageField(upload_to=upload_routine_image, null=False, blank=False)
	exercises = models.ManyToManyField('workout.ExerciseSet')
		
	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title


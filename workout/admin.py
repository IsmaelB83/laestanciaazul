# coding=utf-8
# Python imports
# Django imports
from django.contrib import admin
# Third party app imports
# Local app imports
from .models import BodyPart, Exercise, ExerciseSet, Routine


# Register your models here.
class BodyPartModelAdmin(admin.ModelAdmin):
	list_display = ["id", "name", "timestamp", "updated", "image"]
	list_display_links = ["id"]
	list_editable = ["name", "image"]
	list_filter = ["name"]
	search_fields = ["name"]
	
	class Meta:
		model = BodyPart


class ExerciseModelAdmin(admin.ModelAdmin):
	list_display = ["id", "name", "description", "timestamp", "updated", "image"]
	list_display_links = ["id"]
	list_editable = ["name", "description"]
	list_filter = ["name", "description"]
	search_fields = ["name", "description"]
	
	class Meta:
		model = Exercise


class ExerciseSetModelAdmin(admin.ModelAdmin):
	list_display = ["id", "exercise", "reps", "kgs", "rest"]
	list_display_links = ["id"]
	list_editable = ["exercise", "reps", "kgs", "rest"]
	list_filter = ["exercise"]
	search_fields = ["exercise"]
	
	class Meta:
		model = ExerciseSet


class RoutineModelAdmin(admin.ModelAdmin):
	list_display = ["id", "name", "description", "type", "timestamp", "updated", "image"]
	list_display_links = ["id"]
	list_editable = ["name", "description", "type", "image"]
	list_filter = ["name"]
	search_fields = ["name"]
	
	class Meta:
		model = Routine


admin.site.register(BodyPart, BodyPartModelAdmin)
admin.site.register(Exercise, ExerciseModelAdmin)
admin.site.register(ExerciseSet, ExerciseSetModelAdmin)
admin.site.register(Routine, RoutineModelAdmin)
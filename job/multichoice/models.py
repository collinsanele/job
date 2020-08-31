from django.db import models

# Create your models here.

class Story(models.Model):
	story_text = models.TextField()
	story_title = models.CharField(max_length=600, default="Title Here")
	
	def __str__(self):
		return self.story_title
	
	
	
class Question(models.Model):
	story = models.ForeignKey(Story, on_delete=models.CASCADE)
	question_text = models.CharField(max_length=600, default="default question")
	correct_ans = models.CharField(max_length=600, default="default correct answer")
	option_a = models.CharField(max_length=600, default="default")
	option_b = models.CharField(max_length=600, default="default")
	option_c = models.CharField(max_length=600, default="default")
	option_d = models.CharField(max_length=600, default="default")
	
	def __str__(self):
		return self.question_text

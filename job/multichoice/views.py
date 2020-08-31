from django.shortcuts import render, redirect
from multichoice.models import Question, Story
from django.contrib import messages

# Create your views here.

SCORE = 0
SCORE_PERCENTAGE = 0
REMARK = ""


def landing(request):
	return render(request, "multichoice/home.html")
	
	
def dashboard(request):
	return render(request, "multichoice/dashboard.html")
	

def before_create(request):
	return render(request, "multichoice/before-create.html")
	
	
def create_story(request):
	if request.method == "GET":
		return render(request, "multichoice/create-story.html")
		
	elif request.method == "POST":
		story_title = request.POST.get("title")
		story_body = request.POST.get("story-body")
		story = Story(story_text=story_body.strip(), story_title=story_title.strip())
		story.save()
		messages.success(request, "Story added successfully")
		return redirect("before_create")
		
	
	
	
def create_question(request):
	stories = Story.objects.all()
	
	if request.method == "GET":
		context = {"stories": stories}
		return render(request, "multichoice/create-question.html", context)
		
	elif request.method == "POST":
		if not stories:
			messages.error(request, "Please create a story first")
			print("flash msg")
			return redirect("create_story")
			
		story_id = request.POST.get("title")
	
		story = Story.objects.get(pk=story_id)
		
		question = request.POST.get("question")
		option_q_1 = request.POST.get("q1")
		option_q_2 = request.POST.get("q2")
		option_q_3 = request.POST.get("q3")
		option_q_4 = request.POST.get("q4")
		option_correct = request.POST.get("correct")
		
		question = Question(story=story, question_text=question, correct_ans= option_correct.strip(), option_a=option_q_1.strip(), option_b=option_q_2.strip(), option_c=option_q_3.strip(), option_d=option_q_4.strip())
		question.save()
		messages.success(request, "Question added successfully")
		return redirect("before_create")
	


def edit_delete(request):
	stories = Story.objects.all()
	context = {"stories": stories}
	return render(request, "multichoice/edit-delete.html", context)


def edit(request, pk):
	if request.method == "GET":
		question = Question.objects.get(pk=pk)
		context = {"question": question}
		return render(request, "multichoice/edit.html", context)
		
	elif request.method == "POST":
		question = Question.objects.get(pk=pk)
		
		story_id = question.story.id
		story = Story.objects.get(pk=story_id)
		title = request.POST.get("title")
		story_body = request.POST.get("story-body")
		question_text = request.POST.get("question")
		option_a = request.POST.get("q1")
		option_b = request.POST.get("q2")
		option_c = request.POST.get("q3")
		option_d = request.POST.get("q4")
		correct_option = request.POST.get("correct")
		
		story.story_title = title
		story.story_text = story_body
		question.story = story
		question.question_text = question_text
		question.correct_ans = correct_option
		question.option_a = option_a
		question.option_b = option_b
		question.option_c = option_c
		question.option_d = option_d
		
		question.save()
		story.save()
		
		messages.success(request, "Edited Successfully!")
		return redirect("edit_delete")
		
		
def delete(request, pk):
	question = Question.objects.get(pk=pk)
	question.delete()
	
	messages.success(request, "Deleted Successfully!")
	return redirect("edit_delete")
	


def start(request):
	global SCORE
	global SCORE_PERCENTAGE
	global REMARK
	
	try:
		story = Story.objects.last()
		
	except:
		story = []
		
	if request.method == "GET":	
		questions = story.question_set.all()
		context = {"story": story, "questions": questions}
		return render(request, "multichoice/index.html", context)
		
	elif request.method == "POST":
		SCORE = 0
		SCORE_PERCENTAGE = 0
		REMARK = ""
		
		correct_answers = [item.correct_ans for item in story.question_set.all()]
		
		answers = request.POST.getlist("answer")
		
		if len(answers) > len(correct_answers):
			return render(request, "multichoice/error.html")
		
		if not answers:
			answers = ["no answer" for item in correct_answers]
		
		try:
			total_questions = len(Story.objects.last().question_set.all())
		
		except Exception as e:
			pass
		
		if int(total_questions) == 0:
			messages.error(request, "There are no questions yet")
			return redirect("start")
		
		if int(total_questions) == 10:
			total_questions = 50
			
		
		for index, answer in enumerate(answers):
			if correct_answers[index].strip().lower() == answer.strip().lower():
				if total_questions == 50:
					SCORE+= 5
				else:
					SCORE+= 1
					
			
		SCORE_PERCENTAGE = round(SCORE/ int(total_questions) * 100)
		
		if SCORE_PERCENTAGE >= 75:
			REMARK = "YOU PASSED \nCONGRATS!"
			
		else:
			REMARK = "YOU FAILED! BETTER LUCK NEXT TIME"
			
		return redirect("outcome")
		
		
		
		
def outcome(request):
	global SCORE
	global SCORE_PERCENTAGE
	global REMARK
	
	score = SCORE
	context = {"score": score, "score_percentage": SCORE_PERCENTAGE, "remark": REMARK}
	return render(request, "multichoice/outcome.html", context)






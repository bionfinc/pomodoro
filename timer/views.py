from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from datetime import datetime
from accounts.models import UserProfile
from django.contrib.auth.models import User
from usersessions.models import UserSession, Task, TaskCategory
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

class EditTaskName(forms.Form):
    taskName = forms.CharField(label="New Task Name")

class EditUserSessionName(forms.Form):
    userSessionName = forms.CharField(label="New Session Name")

class EditSessionDescription(forms.Form):
    sessionDescription = forms.CharField(label="Edit Session Description")


# Create your views here.
def index_view(request):

    # If not a active user then render with blank values
    if not request.user.is_authenticated:
        return render(request, 'index.html', {
            'score': 0,
            'user': False,
            'description': ''
        })

    # Get all of a user's task categories to display in the dropdown
    user = request.user
    task_categories = []
    task_category_objects = TaskCategory.objects.filter(user_id=user.id)
    for category in task_category_objects:
        task_categories.append(category.task_category_name)

    # If logged in, check if the user has an active session. 
    user_session_description = ''
    if 'userSessionId' in request.session:  # If active session, get the current description
        userSessionId = request.session['userSessionId']
        user_session_description = UserSession.objects.get(id=userSessionId).description

    if 'taskName' not in request.session:  # Takes advantage of user sessions, checks to see if the taskName is in their session
        now = timezone.now()
        request.session['defaultTaskName'] = True
        request.session['taskNumber'] = 1
        request.session['taskName'] = 'Task: ' + now.strftime(
            "%Y-%m-%d: #1")  # creates a default taskName if they dont have one

    if 'userSessionName' not in request.session:  # Takes advantage of user sessions, checks to see if the userSessionName is in their session
        now = timezone.now()
        request.session['userSessionName'] = 'Session: ' + now.strftime(
            "%Y-%m-%d_%H:%M:%S")  # creates a default userSessionName if they dont have one
        userSessionObject = UserSession.objects.create(user= request.user, session_time_start = now, session_name=request.session['userSessionName'])
        request.session['userSessionId'] = userSessionObject.id

    return render(request, 'index.html', {
        'taskName': request.session['taskName'],
        'userSessionName': request.session['userSessionName'],
        'score': request.user.userprofile.score,
        'user': user,
        'description': user_session_description,
        'task_categories': task_categories
    })
    

# get taskName first then edit it via post
def editTask_view(request):
    #if its a post, it checks the validity of the form content
    if request.method == "POST":
        form = EditTaskName(request.POST)        # contains user's submitted form taskName
        if form.is_valid():                      # checks if the new name is valid
            taskName = form.cleaned_data['taskName']   # if its valid, get the task and add it to the list of tasks
            request.session['taskName'] = taskName             # changing the taskName for the user session
            request.session['defaultTaskName'] = False
            return HttpResponseRedirect(
                reverse('index'))  # returns the user to the timer, is not hard coded, uses the index name and reverses
        else:                                       # if not, it sends them back to the for with their invalid input
            return render(request, 'editTask.html', {
                'form': form
            })
    # if it wasnt a post (was a get) render them an empty form
    return render(request, "editTask.html", {
        'form': EditTaskName
    })
# get taskName first then edit it via post

def editUserSession_view(request):
    #if its a post, it checks the validity of the form content
    if request.method == "POST":
        form = EditUserSessionName(request.POST)        # contains user's submitted form userSession
        if form.is_valid():                      # checks if the new name is valid
            userSessionName = form.cleaned_data['userSessionName']   # if its valid, get the task and add it to the list of tasks
            userSessionId = request.session['userSessionId']  # gets the id of the current session
            userSessionObject = UserSession.objects.get(id = userSessionId) # gets the user session object with matching id
            userSessionObject.session_name = userSessionName # sets the user session objects name to the user inputed name
            userSessionObject.save() # updates the database with the new name
            request.session['userSessionName'] = userSessionName             # changing the userSession for the user session
            return HttpResponseRedirect(
                reverse('index'))  # returns the user to the timer, is not hard coded, uses the index name and reverses
        else:                                       # if not, it sends them back to the for with their invalid input
            return render(request, 'editUserSession.html', {
                'form': form
            })
    # if it wasnt a post (was a get) render them an empty form
    return render(request, "editUserSession.html", {
        'form': EditUserSessionName
    })

def editSessionDescription_view(request):
    if request.method == "POST":
        # Form instance populated from the request
        form = EditSessionDescription(request.POST)                             
        if form.is_valid():
            # Get the cleaned data from the form (Django's cleaned_data contains only the fields that have passed validation tests)                                                            
            sessionDescription = form.cleaned_data['sessionDescription']
            # Get the current UserSession Id that is saved in the sessions cookie
            userSessionId = request.session['userSessionId']
            # Get the object for current the UserSession (contains the column names and entry values)
            userSessionObject = UserSession.objects.get(id=userSessionId)
            # Update the session description
            userSessionObject.description = sessionDescription
            # Save the update to the database
            userSessionObject.save()
            return HttpResponseRedirect(reverse('index'))  # Successfully updated the database, return to the timer page
        else:                                      
            return render(request, 'editSessionDescription.html', {'form': form }) # Unsuccessful, go back to try again
    # Show the form for the user to Edit
    context = {'form': EditSessionDescription}
    # If there is a current session, pre-populate with the saved session description
    if request.user.is_authenticated:
        if 'userSessionId' in request.session:
            userSessionId = request.session['userSessionId']
            obj = UserSession.objects.get(id=userSessionId).description
            form = EditSessionDescription(initial={'sessionDescription': obj})
            context = {'form': form}
    return render(request, "editSessionDescription.html", context)
    
# AJAX for adding points to the score

def add_points(request):
    if request.user.is_authenticated:
        request.user.userprofile.score = request.user.userprofile.score + 10
        request.user.userprofile.save()
        return HttpResponse(request.user.userprofile.score)
    else:
        return HttpResponse('0')


# AJAX for deducting points from the score
def deduct_points(request):
    if request.user.is_authenticated:
        request.user.userprofile.score = request.user.userprofile.score - 10
        request.user.userprofile.save()
        return HttpResponse(request.user.userprofile.score)
    else:
        return HttpResponse('0')

# check logged in status
def is_logged_in(request):
    if request.user.is_authenticated:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

# save task info to db when "Start" button clicked
@csrf_exempt
def save_task_info(request):
    if request.user.is_authenticated:
        # pull data from ajax call
        task_name = json.loads(request.body)['task_name']
        task_time = json.loads(request.body)['task_time']
        category = json.loads(request.body)['category']
        # create instance of current session to use as FK for Task db
        session_id = UserSession.objects.get(id = request.session['userSessionId'])

        # create new entry in Task db
        newTask = Task.objects.create(usersession=session_id, task_name=task_name, task_time=task_time, time_start=timezone.now(), category=category)
        request.session['taskId'] = newTask.id  # save the id for the task in the database to the session as taskId
        return HttpResponse(status=200)
    else:
        errMessage = 'Error: user not logged in.'
        print(errMessage)
        return HttpResponse(errMessage)
        
# Update task category in the db when task category is changed
@csrf_exempt
def update_task_category(request):
    if request.user.is_authenticated:
        # create instance of current task by using its id stored in the the django session
        currentTask = Task.objects.get(id = request.session['taskId'])
        # pull current category from ajax call
        category = json.loads(request.body)['category']
        # update the current task category
        currentTask.category = category
        # update/save the changed category to the database
        currentTask.save()
        return HttpResponse(status=200)
    else:
        errMessage = 'Error: user not logged in.'
        print(errMessage)
        return HttpResponse(errMessage)

# AJAX for updating task time_end in db
def update_task_time_end(request):
    if request.user.is_authenticated:
        # create instance of current task by using its id stored in the the django session
        currentTask = Task.objects.get(id = request.session['taskId'])
        currentTask.time_end = timezone.now()
        currentTask.save()
        return HttpResponse(status=200)
    else:
        errMessage = 'Error: user not logged in.'
        print(errMessage)
        return HttpResponse(errMessage)

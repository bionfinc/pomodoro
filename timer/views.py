from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from datetime import datetime

class EditTaskName(forms.Form):
    taskName = forms.CharField(label="New Task Name")

# Create your views here.
def index_view(request):
    if 'taskName' not in request.session:          # Takes advantage of user sessions, checks to see if the taskName is in their session
        now = datetime.now()
        request.session['taskName'] = 'Task:' + now.strftime("%Y-%m-%d_%H:%M:%S")               # creates a default taskName if they dont have one
    return render(request,'index.html', {
        'taskName': request.session['taskName']
    })

# get taskName first then edit it via post
def editTask_view(request):
    #if its a post, it checks the validity of the form content
    if request.method == "POST":
        form = EditTaskName(request.POST)        # contains user's submitted form taskName
        if form.is_valid():                      # checks if the new name is valid
            taskName = form.cleaned_data['taskName']   # if its valid, get the task and add it to the list of tasks
            request.session['taskName'] = taskName             # changing the taskName for the user session
            return HttpResponseRedirect(reverse('index'))     # returns the user to the timer, is not hard coded, uses the index name and reverses 
        else:                                       # if not, it sends them back to the for with their invalid input
            return render(request, 'editTask.html', {
                'form': form
            })
    # if it wasnt a post (was a get) render them an empty form
    return render(request, "editTask.html", {
        'form': EditTaskName
    })

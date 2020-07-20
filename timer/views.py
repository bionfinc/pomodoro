from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms
from datetime import datetime
from accounts.models import UserProfile
from django.contrib.auth.models import User
from usersessions.models import UserSession

class EditTaskName(forms.Form):
    taskName = forms.CharField(label="New Task Name")

class EditUserSessionName(forms.Form):
    userSessionName = forms.CharField(label="New Session Name")


# Create your views here.
def index_view(request):
    if 'taskName' not in request.session:  # Takes advantage of user sessions, checks to see if the taskName is in their session
        now = datetime.now()
        request.session['taskName'] = 'Task: ' + now.strftime(
            "%Y-%m-%d_%H:%M:%S")  # creates a default taskName if they dont have one
        
    if 'userSessionName' not in request.session:  # Takes advantage of user sessions, checks to see if the userSessionName is in their session
        now = datetime.now()
        request.session['userSessionName'] = 'Session: ' + now.strftime(
            "%Y-%m-%d_%H:%M:%S")  # creates a default userSessionName if they dont have one
        userSessionObject = UserSession.objects.create(user= request.user, session_time_start = now, session_name=request.session['userSessionName'])
        request.session['userSessionId'] = userSessionObject.id
    # add in user's current score if logged in
    score = 0
    if request.user.is_authenticated:
        score = request.user.userprofile.score

    if request.user.is_authenticated:
        user = request.user
    else:
        user = False

    return render(request, 'index.html', {
        'taskName': request.session['taskName'],
        'userSessionName': request.session['userSessionName'],
        'score': score,
        'user': user
    })

# get taskName first then edit it via post
def editTask_view(request):
    #if its a post, it checks the validity of the form content
    if request.method == "POST":
        form = EditTaskName(request.POST)        # contains user's submitted form taskName
        if form.is_valid():                      # checks if the new name is valid
            taskName = form.cleaned_data['taskName']   # if its valid, get the task and add it to the list of tasks
            request.session['taskName'] = taskName             # changing the taskName for the user session
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
            userSessionId = request.session['userSessionId']
            userSessionObject = UserSession.objects.get(id = userSessionId)
            userSessionObject.session_name = userSessionName
            userSessionObject.save()
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

def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)
    return render(request, "flights/flight.html", {
        'flight': flight,
        'passengers': flight.passengers.all(),
        'non_passengers': Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST['passenger']))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse('flight', args=(flight.id,)))


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


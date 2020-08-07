from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User, Note
# Create your views here.

def index(request):
	notes = None
	totalnotes = None
	if request.user.is_authenticated:
		notes = Note.objects.filter(creator = request.user)
		totalnotes = notes.count()
	return render(request, "index.html", {
		"notes": notes,
		"totalnotes": totalnotes
		})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
    	if request.user.is_authenticated:
    		return HttpResponseRedirect(reverse('index'))
    	return render(request, "login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
    	if request.user.is_authenticated:
    		return HttpResponseRedirect(reverse('index'))
    	return render(request, "register.html")

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def create(request):
	if request.method == "POST":
		title = request.POST["title"]
		note = request.POST['note']
		this_note = Note(title = title, creator = request.user, note = note)
		this_note.save()
		return HttpResponseRedirect(reverse('note', args = [this_note.id]))
	else:
		return render(request, "create.html")

def note(request, id):
	note = Note.objects.filter(pk = id)
	if note.count() == 0 or not request.user.is_authenticated:
		return render(request, "error.html")
	note = note[0]
	if note.creator != request.user:
		return render(request, "error.html")
	if request.method == "POST":
		this_note = Note.objects.get(pk = id)
		this_note.title = request.POST["title"]
		this_note.note = request.POST["note"]
		this_note.save()
		return HttpResponseRedirect(reverse('index'))
	return render(request, "note.html", {
		"note": note
		})
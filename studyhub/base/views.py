from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Room, Topic, Message, User
from .forms import UserForm, MyUserCreationForm, RoomForm

def loginView(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exits")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Email OR Password is incorrect")

    return render(request, 'base/pages/login.html')


def logoutView(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user  = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    context = {"form": MyUserCreationForm}
    return render(request, "base/pages/signup.html", context)


def home(request):
    # return HttpResponse("Home Page")
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    rooms_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'rooms': rooms,
        "topics": topics,
        "rooms_count": rooms_count,
        "room_messages": room_messages,
    }
    return render(request, 'base/pages/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by("-created")
    participants = room.participants.all()
    if request.method == 'POST' and request.POST.get('body'):
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)
    context = {
        'room': room, 
        "room_messages": room_messages, 
        "participants": participants
    }
    return render(request, 'base/pages/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()[0:5]
    context = {
        "user": user,
        "rooms": rooms, 
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, 'base/pages/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    if request.method == 'POST':
        # form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room = Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),   
        )
        room.participants.add(request.user)
        return redirect('home')
        # if form.is_valid():
            
            # room = form.save(commit=False)
            # room.host = request.user
            # room.save()
            # participants = room.participants.all()
            # room.participants.add(request.user)
            
    topics = Topic.objects.all()
    form = RoomForm()
    context = {"form": form, "topics": topics}
    return render(request, 'base/pages/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get("name")
        room.description = request.POST.get("description")
        room.save()
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')

    
    form  = RoomForm(instance=room)
    topics = Topic.objects.all()
    context = { "form": form, "topics": topics, "room": room }
    return render(request, 'base/pages/room_form.html', context)  


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        room.delete()
        return redirect("home")

    return render(request, 'base/pages/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed here!")
    if request.method == 'POST':
        message.delete()
        return redirect(request)

    return render(request, 'base/pages/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {
        "form": form,
    }

    return render(request, 'base/pages/update_user.html', context)


def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter( Q(name__icontains=q) )
    
    context = {
        "topics": topics,
    }
    return render(request, 'base/pages/topics.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    context = {
        "room_messages": room_messages,
    }
    return render(request, 'base/pages/activity.html', context) 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from .message import MessageForm
from .topic import TopicForm

# rooms = [
#     {'id':1, 'name':'Manoj'},
#     {'id':2, 'name':'Madhavi'},
#     {'id':3, 'name':'Yatish'},
#     {'id':4, 'name':'Tirth'},
#     {'id':5, 'name':'Salman'}, 

# ]

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        print(username)
        password = request.POST.get('password')
        print(password)

        try:
            user = User.objects.get(username=username)
            print(user)
        except:
            messages.error(request, 'User does not exist') 
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'Username or Password does not exist')

        
    context = {'page': page}
    return render (request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    print('room', rooms)
    topics = Topic.objects.all()[0:5]

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages }
    
    return render(request, 'base/home.html', context)
    
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        print('message : ', message)
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}    
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get( id=pk )
    print('user :', user)

    rooms = user.room_set.all()
    print('rooms:', rooms)
    room_messages = user.message_set.all()
    print('room_messages:', room_messages)
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    print('context:', context)
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createroom(request):
    topics = Topic.objects.all()
    form = RoomForm()
    # print(form)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic=topic,
            name=request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

def createmessage(request):
    message = MessageForm()
    if request.method == 'POST':
        message = MessageForm(request.POST)
        if message.is_valid():
            message.save()

    context = {'message': message}
    return render(request, 'base/message.html', context)

def createtopic(request):
    topic = TopicForm()
    if request.method == 'POST':
        topic = TopicForm(request.POST)
        if topic.is_valid():
            topic.save()

    context = {'topic': topic}
    return render(request, 'base/topic.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    topics = Topic.objects.all()
    room = Room.objects.get( id=pk )
    form = RoomForm(instance=room)
    print('user',request.user)
    print('host',room.host)
    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get( id=pk )

    if request.user != room.host:
        return HttpResponse('You are not allowed here')  

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get( id=pk )
    

    if request.user != message.user:
        return HttpResponse('You are not allowed here')  

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})
    
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user) 

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
        return redirect('profile', pk = user.id)
    
    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)
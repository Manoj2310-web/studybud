from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm
from .message import MessageForm
from .topic import TopicForm

# Create your views here.
from django.http import HttpResponse

# rooms = [
#     {'id':1, 'name':'Manoj'},
#     {'id':2, 'name':'Madhavi'},
#     {'id':3, 'name':'Yatish'},
#     {'id':4, 'name':'Tirth'},
#     {'id':5, 'name':'Salman'},

# ]

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)
    
def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}    
    return render(request, 'base/room.html', context)

def createroom(request):
    form = RoomForm()
    # print(form)
    if request.method == 'POST':
        # print("POST data",request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
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

def updateRoom(request, pk):
    room = Room.objects.get( id=pk )
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get( id=pk )
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

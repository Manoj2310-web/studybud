from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

rooms = [
    {'id':1, 'name':'Manoj'},
    {'id':2, 'name':'Madhavi'},
    {'id':3, 'name':'Yatish'},
    {'id':4, 'name':'Tirth'},
    {'id':5, 'name':'Salman'},

]

def home(request):
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)
    
def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}    
    return render(request, 'base/room.html', context)
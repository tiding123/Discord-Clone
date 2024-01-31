from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# rooms=[
#     {'id':1, 'name':"sans"},
#     {'id':2, 'name':"yash"},
#     {'id':3, 'name':"pgla"},
# ]


def hello(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                               Q(host__username__icontains=q) |
                               Q(description__icontains=q))
    topics = Topic.objects.all()
    messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    temp = {'rooms':rooms, 'topics':topics,'messages':messages}
    return render(request,'Home.html',temp)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_message = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method =='POST':
        message=Message.objects.create(user=request.user,
                                      room=room,
                                      body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('room',pk)
    context = {'room':room,'messages':room_message,'participants':participants}
    return render(request,'room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form=RoomForm(request.POST)
        room = form.save(commit=False)
        room.host=request.user
        room.save( )
        return redirect('home')
    context={'form':form}
    return render(request,'room_form.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form=RoomForm(request.POST, instance=room)
        form.save()
        return redirect('home')
    context={'form':form}
    return render(request,'room_form.html',context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    rooms = Room.objects.all();
    context = {'rooms':rooms}
    return render(request,'delete_room.html',context)

def loginpage(request):
    page = "login"
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "invalid user")
    context = {'page':page}
    return render(request,'loginpage.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def register(request):
    form = UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"error")
    context = {'form':form}
    return render(request,"loginpage.html",context)

def DeleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    roomid = message.room.id
    if request.method == 'POST':
        message.delete()
        return redirect('room',roomid)
    context= {'message':message}
    return render(request,'deletemessage.html',context)

def profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    topics=Topic.objects.all()
    messages=user.message_set.all()
    context={'rooms':rooms,'topics':topics,'messages':messages}
    return render(request,'profile.html',context)

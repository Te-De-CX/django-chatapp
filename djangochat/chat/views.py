from django.shortcuts import render,redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
# Create your views here.

def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })
    
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    if Room.objects.filter(name=room).exists():
        return redirect("/"+room+"/?username"+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect("/"+room+"/?username="+username)
    
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST["room_id"]
    
    new_message = Message.objects.create(value=message, user=username, room=room_id)
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    try:
        # Get the room details
        room_details = Room.objects.get(name=room)
        
        # Filter messages by room ID
        messages = Message.objects.filter(room=room_details.id).values('user', 'value', 'date')
        
        # Convert the QuerySet to a list and format the date
        messages_list = list(messages)
        for message in messages_list:
            message['date'] = message['date'].strftime("%Y-%m-%d %H:%M:%S")  # Format the date
        
        return JsonResponse({"messages": messages_list})
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
from django.shortcuts import render
from reservation.models import *
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.shortcuts import *
from datetime import datetime, date

FORM = """
        <form method="POST">
        <p>Podaj nazwę sali:</p>
        <input type="text" name="name" value="{}">
        <p>Podaj pojemność sali:</p>
        <input type="number" step="1" min="0" name="capacity" value="{}">
        <p>Czy na sali jest projektor?</p>
        <input type="radio" name="is_projector" value="True" {}>Tak
        <input type="radio" name="is_projector" value="False" {}>Nie
        <p><input type="submit" value="{}"></p>
        </form>
    """
FORM2 = """
    <a href="/room/"><input type="button" value="Lista sal"></a>
    <a href="/room/new/"><input type="button" value="Dodaj nową salę"></a>
    {}
    """
@method_decorator(csrf_exempt, name="dispatch")
class NewRoom(View):
    def get(self, request):
        return HttpResponse(FORM2.format(FORM.format("", "", "", "",  "Dodaj salę")))
    
    def post(self, request):
        Rooms.objects.create(name = request.POST.get("name"), capacity = request.POST.get("capacity"), projector = request.POST.get("is_projector") )
        return HttpResponse(FORM2.format("<p>Sala została dodana!</p>"))
    
class ShowAll(View):
    def get(self, request):
        room = "<h1>Dostępne sale:</h1><ol>"
        for i in Rooms.objects.all():
            room += "<li>{} <a href='/room/{}' title='Szczegóły'>&#10067;</a> <a href='/room/modify/{}' title='Edytuj'>&#9998;</a> <a href='/room/delete/{}' title='Usuń'>&#128465;</a></li>".format(i.name, i.pk, i.pk, i.pk)
        room +="</ol>"
        return HttpResponse(FORM2.format(room))

class ShowRoom(View):
    def get(self, request, id):
        room = Rooms.objects.get(pk = int(id))
        reservations = Reservations.objects.filter(room_id = int(id))
        res_list = ""
        if room.projector == True:
            is_projector = "jest"
        else:
            is_projector = "nie ma"
        
        for res in reservations:
            res_list += "<li>Od: {} Do: {}</li>".format(res.date_from, res.date_to)
            
           
        details = """
            <p><b>{}</b></p>
            <ul>
                <li>Pojemność: {}</li>
                <li>Projektor: {}</li>
            </ul>
            <p>Obecne rezerwacje:</p>
                <ul>
                    {}
                </ul>
            <p><a href="/reservation/{}"><input type="button" value="Rezerwuj salę"></a></p>
        """.format(room.name, room.capacity, is_projector, res_list, room.pk)
        return HttpResponse(FORM2.format(details))

@method_decorator(csrf_exempt, name="dispatch")
class ModifyRoom(View):
    def get(self, request, id):
        room = Rooms.objects.get(pk = int(id))
        checked_yes = ""
        checked_no = ""
        if room.projector == True:
            checked_yes = "checked"
        elif room.projector == False:
            checked_no = "checked"
        return HttpResponse(FORM2.format(FORM.format(room.name, room.capacity, checked_yes, checked_no, "Ztawierdź zmiany")))
    
    def post(self, request, id):
        room = Rooms.objects.get(pk = int(id))
        room.name = request.POST.get("name")
        room.capacity = int(request.POST.get("capacity"))
        if request.POST.get("is_projector") == "True":
            room.projector = True
        else:
            room.projector = False
        room.save()
        return HttpResponse(FORM2.format("<p>Zmiany zostały wprowadzone!</p>"))
    
@method_decorator(csrf_exempt, name="dispatch")
class DeleteRoom(View):
    def get(self, request, id):
        delete = """
        <form method="POST">
            <p>Czy na pewno usunąć salę: {}</p>
            <input type="submit" value="Tak" name="choose"><input type="submit" value="Nie" name="choose">
        </form>    
        """
        room = Rooms.objects.get(pk = int(id))
        return HttpResponse(FORM2.format(delete.format(room.name)))
    
    def post(self, request, id):
        if request.POST.get("choose") == "Tak":
            room = Rooms.objects.get(pk = int(id))
            room.delete()
            return redirect("/room/")
        else:
            return redirect("/room/")
        
@method_decorator(csrf_exempt, name="dispatch")
class BookRoom(View):
    def get(self, request, id):
        room = Rooms.objects.get(pk = int(id))
        present_day = datetime.now().date()
        booking = """
        <form method="POST">
            <p>Rezerwujesz salę: {}</p>
            <p>Podaj od kiedy:</p>
            <input type="date" name="from" min="{}">
            <p>Podaj do kiedy:</p>
            <input type="date" name="to" min="{}">
            <p>Dodatkowe uwagi</p>
            <input type="text" name="desc">
            <p><input type="submit" value="Rezerwuj"></p>
        </form>
        """.format(room.name, present_day, present_day)
        
        return HttpResponse(FORM2.format(booking))
        
    def post(self, request, id):
        reservations = Reservations.objects.filter(room_id = int(id))
        present = datetime.now().date()
        date_from = request.POST.get("from").split("-")
        date_to = request.POST.get("to").split("-")
        try:
            date_1 = date(int(date_from[0]), int(date_from[1]), int(date_from[2]))
            date_2 = date(int(date_to[0]), int(date_to[1]), int(date_to[2]))
        except(ValueError, IndexError):
            return HttpResponse(FORM2.format("""<p>Podana wartość nie jest datą lub podałeś datę w złym formacie. Prawidłowy format: YYYY-MM-DD</p>
                                                <p><a href="/reservation/{}"><input type="button" value="Powrót do rezerwacji"></a></p>""".format(id)))
        is_booked = False
        
        for reservation in reservations:
            date_from_db = date(int(reservation.date_from.year), int(reservation.date_from.month), int(reservation.date_from.day))
            date_to_db = date(int(reservation.date_to.year), int(reservation.date_to.month), int(reservation.date_to.day))
            if date_from_db <= date_1 <= date_to_db or date_from_db <= date_2 <= date_to_db or date_1 <= date_from_db <= date_2 or date_1 <= date_to_db <= date_2:
                is_booked = True 
            
        if date_1 > present and is_booked == False:
            days = abs(date_1 - date_2)
            res1 = Reservations.objects.create(date_from = request.POST.get("from"), date_to = request.POST.get("to"), days = days.days, description = request.POST.get("desc"), room = Rooms.objects.get(pk = int(id)))
            return HttpResponse(FORM2.format("<p>Dodano rezerwację!</p>"))
        else:
            return HttpResponse(FORM2.format("<p>Podałeś datę z przeszłości lub w podanym okresie sala jest już zarezerwowana</p>"))
        
        


        
        
        
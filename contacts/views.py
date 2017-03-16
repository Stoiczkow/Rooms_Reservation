from django.shortcuts import render
from django.http.response import HttpResponse
from contacts.models import *
from django.views import View
from django.shortcuts import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
# Create your views here.
FORM = """
    <a href="/all/"><input type="button" value="Lista kontaktów"></a>
    <a href="/new/"><input type="button" value="Dodaj nową osobę"></a>
    {}
    """
def show_all_contacts(request):
    person = "<h1>Twoje kontakty:</h1><ol>"
    for i in Person.objects.all():
        person += "<li>{} {} <a href='/show/{}' title='Szczegóły'>&#10067;</a>   <a href='/modify/{}' title='Edytuj'>&#9998;</a>   <a href='/delete/{}' title='Usuń'>&#128465;</a></li>".format(i.name, i.surname, i.pk, i.pk, i.pk)
    person +="</ol>"
    return HttpResponse(FORM.format(person))

FORM2 = """
        <form method="POST">
        <p>Podaj imię i nazwisko</p>
        <input type="text" name="name" value="{}"><input type="text" name="surname" value="{}">
        <p>Podaj opis:</p>
        <input type="text" name="desc" value="{}">
        <p>Podaj miejscowość:</p>
        <input type="text" name="city" value="{}">
        <p>Podaj ulicę:</p>
        <input type="text" name="street" value="{}">
        <p>Podaj nr domu i mieszkania:</p>
        <input type="text" name="house" value="{}"><input type="text" name="apartment" value="{}">
        <p>Podaj nr telefonu:</p>
        <input type="text" name="phone" value="{}">
        <p>Podaj rodzaj telefonu:</p>
        <input type="text" name="phone_desc" value="{}">
        <p>Podaj e-mail:</p>
        <input type="text" name="email" value="{}">
        <p>Podaj rodzja e-maila:</p>
        <input type="text" name="email_desc" value="{}">
        <p><input type="submit" value="{}"></p>
        </form>
    """
@method_decorator(csrf_exempt, name="dispatch")
class NewContact(View):
    
    def get(self, request):
        return HttpResponse(FORM.format(FORM2.format("", "", "", "", "", "", "", "", "", "", "", "Dodaj osobę")))
    
    def post(self, request):
        addresses = Address.objects.all()
        flag =  True
        for i in addresses:
            if (i.city == request.POST.get("city") and i.street == request.POST.get("street") and i.house == request.POST.get("house") and i.apartment == request.POST.get("apartment")):  
                address_a = Address.objects.get(city=i.city, street=i.street, house=i.house, apartment=i.apartment)
                flag = False
                
        if flag == True:
            address_a = Address.objects.create(city=request.POST.get("city"), street=request.POST.get("street"), house=request.POST.get("house"), apartment=request.POST.get("apartment"))
        
        person_n = Person.objects.create(name=request.POST.get("name"), surname=request.POST.get("surname"), description=request.POST.get("desc"), address = address_a )
        try:
            Phone.objects.create(number=int(request.POST.get("phone")), description = request.POST.get("phone_desc"), person = person_n)
        except (ValueError, IntegrityError):
            return HttpResponse("Podałeś numer telefonu, który nie jest liczbą lub podany numer już istnieje w skrzynce kontaktowej. Możesz dodać prawidłowy numerr edytując kontakt. <p><a href='/all/'><input type='button' value='Wróć do listy kontaktów'></a></p>")
        try:
            Email.objects.create(email=request.POST.get("email"), description = request.POST.get("email_desc"), person = person_n)
        except (ValueError, IntegrityError):
            return HttpResponse("Podałeś błędny email lub podany email już istnieje w skrzynce kontaktowej. Możesz dodać prawidłowy email edytując kontakt. <p><a href='/all/'><input type='button' value='Wróć do listy kontaktów'></a></p>")

        return redirect("/all/")

@method_decorator(csrf_exempt, name="dispatch")
class ModifyContact(View):
    def get(self, request, id):
        person_m = Person.objects.get(pk = int(id))
        try:
            phone = Phone.objects.get(person = person_m)
        except ObjectDoesNotExist:
            phone = None
        try:
            email = Email.objects.get(person = person_m)
        except ObjectDoesNotExist:
            email = None
        
        if phone == None and email == None:
            return HttpResponse(FORM.format(FORM2.format(person_m.name, person_m.surname, person_m.description, person_m.address.city, person_m.address.street, person_m.address.house, person_m.address.apartment, "", "", "", "",  "Zatwierdź zmiany"))) 
        elif phone != None and email == None:
            return HttpResponse(FORM.format(FORM2.format(person_m.name, person_m.surname, person_m.description, person_m.address.city, person_m.address.street, person_m.address.house, person_m.address.apartment, phone.number, phone.description, "", "",  "Zatwierdź zmiany"))) 
        elif phone == None and email != None:
            return HttpResponse(FORM.format(FORM2.format(person_m.name, person_m.surname, person_m.description, person_m.address.city, person_m.address.street, person_m.address.house, person_m.address.apartment, "", "", email.email, email.description,  "Zatwierdź zmiany"))) 
        elif phone != None and email != None:
            return HttpResponse(FORM.format(FORM2.format(person_m.name, person_m.surname, person_m.description, person_m.address.city, person_m.address.street, person_m.address.house, person_m.address.apartment, phone.number, phone.description, email.email, email.description,  "Zatwierdź zmiany"))) 

    def post(self, request, id):
        person = Person.objects.get(pk = int(id))
        person.name = request.POST.get("name")
        person.surname = request.POST.get("surname")
        person.description = request.POST.get("desc")
        person.address.city = request.POST.get("city")
        person.address.street = request.POST.get("street")
        person.address.house = request.POST.get("house")
        person.address.apartment = request.POST.get("apartment")
        person.save()
        person.address.save()
        return redirect("/all/")

@method_decorator(csrf_exempt, name="dispatch")
class DeleteContact(View):
    def get(self, request, id):
        delete = """
        <form method="POST">
            <p>Czy na pewno usunąć kontakt: {} {}</p>
            <input type="submit" value="Tak" name="choose"><input type="submit" value="Nie" name="choose">
        </form>    
        """
        person = Person.objects.get(pk = int(id))
        
        return HttpResponse(delete.format(person.name, person.surname))
    
    def post(self, request, id):
        if request.POST.get("choose") == "Tak":
            person = Person.objects.get(pk = int(id))
            person.delete()
            return redirect("/all/")
        else:
            return redirect("/all/")

@method_decorator(csrf_exempt, name="dispatch")
class ShowOne(View):
    def get(self, request, id):
        details = """
        <p><b>{} {}</b></p>
        <p>{}</p>
        <p>Adres:{} {}/{} {}</p>
        <p>Telefon:{} </p>
        <p>Email:{}</p>
        """
        person = Person.objects.get(pk = int(id))
        
       
        try:
            phone = Phone.objects.get(person = person)
            try:
                email = Email.objects.get(person = person)
            except UnboundLocalError:
                pass
        except ObjectDoesNotExist:
            try:
                if email == None and phone != None:
                    return HttpResponse(FORM.format(details.format(person.name, person.surname, person.description, person.address.street, person.address.house, person.address.apartment, person.address.city, phone.number, ""))) 
                elif email != None and phone == None:
                    return HttpResponse(FORM.format(details.format(person.name, person.surname, person.description, person.address.street, person.address.house, person.address.apartment, person.address.city, "", email.email)))
            except UnboundLocalError:
                return HttpResponse(FORM.format(details.format(person.name, person.surname, person.description, person.address.street, person.address.house, person.address.apartment, person.address.city, "", "")))
         

        return HttpResponse(FORM.format(details.format(person.name, person.surname, person.description, person.address.street, person.address.house, person.address.apartment, person.address.city, phone.number, email.email))) 

    
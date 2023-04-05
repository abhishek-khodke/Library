from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import Book

# Create your views here.

@csrf_exempt
def home(request): 
    # print(request.method)
    if request.method == "POST":
        data = request.POST
        # print(request.POST)
        bid = data.POST.get("book_id")
        name = data.POST.get("book_name")
        qty = data.POST.get("book_qty")
        price = data.POST.get("book_price")
        author = data.POST.get("book_author")
        is_pub= data.POST.get("book_is_pub")
        # print(request.POST)
        # print(name, qty, price, author, is_pub)
        if is_pub == "Yes":
            is_pub = True
        else:
            is_pub = False
        if not bid:
            Book.objects.create(name=name, qty=qty, price=price, author=author, is_published=is_pub)
        else:
            book_obj = Book.objects.get(id=bid)
            book_obj.name = name
            book_obj.qty = qty
            book_obj.price = price
            book_obj.author = author
            book_obj.is_published = is_pub
            book_obj.save()
        
        # return redirect("home_page")
        return HttpResponse("Success")


    elif request.method == "GET":
        # pront(request.GET)
        return render(request, "home.html", context={"person_name": "Abhishek"})
    
def show_books(request):
    return render(request, "show_books.html", {"books" : Book.objects.filter(is_active=True), "active": True})

def update_book(request, id): 
    book_obj = Book.objects.get(id=id)
    return render(request, "home.html", context={"single_book": book_obj})

def delete_book(request, pk): # hard delete
    Book.objects.get(id=pk).delete()
    return redirect("all_active_books")

def soft_delete_book(request, pk):
    book_obj = Book.objects.get(id=pk)
    book_obj.is_active = False
    book_obj.save()
    return redirect("all_inactive_books")

def show_inactive_books(request):
    return render(request, "show_books.html", {"books" : Book.objects.filter(is_active=False), "inactive": True})

def restore_book(request, pk):
    book_obj = Book.objects.get(id=pk)
    book_obj.is_active = True
    book_obj.save()
    return redirect("all_active_books")
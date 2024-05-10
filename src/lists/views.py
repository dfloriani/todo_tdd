from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from lists.forms import ItemForm

def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST["text"], list=our_list)
            return redirect(our_list)
    else:
        form = ItemForm()
    return render(request, "list.html", {"list": our_list, "form": form})

def new_list(request):
    form = ItemForm(data=request.POST)  
    if form.is_valid():  
        nulist = List.objects.create()
        Item.objects.create(text=request.POST["text"], list=nulist)
        return redirect(nulist)
    else:
        return render(request, "home.html", {"form": form})


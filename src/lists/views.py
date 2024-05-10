from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from lists.forms import ItemForm

def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    error = None

    if request.method == "POST":
        try:
            item = Item(text=request.POST["item_text"], list=our_list)
            item.full_clean()
            item.save()
            return redirect(our_list)
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, "list.html", {"list": our_list, "error": error})

def new_list(request):
    nulist = List.objects.create()
    item = Item.objects.create(text=request.POST["item_text"], list=nulist)
    try:
        item.full_clean()
    except ValidationError:
        nulist.delete()
        expected_error = mark_safe("You can't have an empty list item")
        response = render(request, "home.html", {"error": expected_error})
        return response
    return redirect(nulist)


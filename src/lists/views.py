from django.shortcuts import redirect, render
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

def home_page(request):
    return render(request, "home.html")

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"], list=our_list)
        return redirect(f"/lists/{our_list.id}/")
    return render(request, "list.html", {"list": our_list})

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
    return redirect(f"/lists/{nulist.id}/")


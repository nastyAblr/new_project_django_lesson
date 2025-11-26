from django.shortcuts import render, get_object_or_404

from .models import Pizza
from .forms import OrderForm


def index(request):
    return render(request, 'pizzeria/index.html')

def menu_view(request):
    pizzas = Pizza.objects.all()
    return render(request, 'pizzeria/menu.html', {'pizzas': pizzas})

def pizza_detail(request, slug):
    pizza = get_object_or_404(Pizza, slug=slug)
    return render(request, 'pizzeria/pizza_detail.html', {'pizza': pizza})



def order_view(request, slug):
    pizza = get_object_or_404(Pizza, slug=slug)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.pizza = pizza
            order.save()
            return render(request, 'pizzeria/order_success.html', {'pizza': pizza})
    else:
        form = OrderForm()

    return render(request, 'pizzeria/order_form.html', {
        'pizza': pizza,
        'form': form
    })

def contacts(request):
    return render(request, "pizzeria/contacts.html")


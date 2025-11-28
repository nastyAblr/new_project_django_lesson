from django.shortcuts import render, get_object_or_404, redirect
from .models import Pizza, Order, OrderItem, UserProfile
from .forms import OrderForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from decimal import Decimal


def index(request):
    return render(request, "pizzeria/index.html")


# меню
def menu_view(request):
    pizzas = Pizza.objects.all()
    return render(request, 'pizzeria/menu.html', {'pizzas': pizzas})


# детальная страница
def pizza_detail(request, slug):
    pizza = get_object_or_404(Pizza, slug=slug)
    return render(request, 'pizzeria/pizza_detail.html', {'pizza': pizza})


# --- КОРЗИНА (в session) ---
def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def add_to_cart(request, slug):
    pizza = get_object_or_404(Pizza, slug=slug)
    cart = _get_cart(request)
    pid = str(pizza.id)
    if pid in cart:
        cart[pid]['quantity'] += 1
    else:
        cart[pid] = {'name': pizza.name, 'price': str(pizza.price), 'quantity': 1}
    _save_cart(request, cart)
    messages.success(request, f"Пицца {pizza.name} добавлена в корзину")
    return redirect('menu')


def cart_view(request):
    cart = _get_cart(request)
    items = []
    total = Decimal('0.00')
    for pid, data in cart.items():
        try:
            pizza = Pizza.objects.get(id=int(pid))
        except Pizza.DoesNotExist:
            continue
        qty = data['quantity']
        price = Decimal(data['price'])
        cost = price * qty
        items.append({'pizza': pizza, 'quantity': qty, 'price': price, 'cost': cost})
        total += cost
    return render(request, 'pizzeria/cart.html', {'items': items, 'total': total})


def cart_update(request):
    if request.method == 'POST':
        cart = _get_cart(request)
        for pid, qty in request.POST.items():
            if pid.startswith('qty_'):
                id = pid.split('qty_')[1]
                if id in cart:
                    q = int(qty) if qty.isdigit() else 0
                    if q > 0:
                        cart[id]['quantity'] = q
                    else:
                        del cart[id]
        _save_cart(request, cart)
    return redirect('cart')


def cart_clear(request):
    request.session['cart'] = {}
    return redirect('cart')


# --- ОФОРМЛЕНИЕ ЗАКАЗА (требует логина) ---
@login_required(login_url='login')
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        messages.error(request, "Корзина пуста")
        return redirect('menu')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            # вычислить total
            total = Decimal('0.00')
            order.save()  # сохраняем, чтобы получить id
            for pid, data in cart.items():
                pizza = Pizza.objects.get(id=int(pid))
                qty = data['quantity']
                item = OrderItem.objects.create(order=order, pizza=pizza, price=pizza.price, quantity=qty)
                total += pizza.price * qty
            order.total = total
            order.save()
            # очистить корзину
            request.session['cart'] = {}
            messages.success(request, f"Заказ #{order.id} создан")
            return redirect('order_detail', pk=order.id)
    else:
        # предзаполнить поля из профиля если есть
        profile = getattr(request.user, 'profile', None)
        initial = {}
        if profile:
            initial['phone'] = profile.phone
            initial['address'] = profile.address
            initial['name'] = request.user.get_full_name() or request.user.username
        form = OrderForm(initial=initial)
    return render(request, 'pizzeria/checkout.html', {'form': form})


# просмотр конкретного заказа (доступно владельцу или админу)
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.user != order.user and not request.user.is_staff:
        messages.error(request, "Доступ запрещён")
        return redirect('menu')
    return render(request, 'pizzeria/order_detail.html', {'order': order})


# личный кабинет
@login_required(login_url='login')
def account(request):
    orders = Order.objects.filter(user=request.user)
    profile = getattr(request.user, 'profile', None)
    return render(request, 'pizzeria/account.html', {'orders': orders, 'profile': profile})

@login_required(login_url='login')
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "pizzeria/user_orders.html", {"orders": orders})

# def user_orders(request):
#     # показываем только заказы текущего пользователя
#     orders = Order.objects.filter(user=request.user).order_by("-created_at")
#     return render(request, "pizzeria/user_orders.html", {"orders": orders})


# регистрация
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # <-- правильный способ
            messages.success(request, "Регистрация прошла успешно")
            return redirect('account')
    else:
        form = UserRegisterForm()
    return render(request, 'pizzeria/signup.html', {'form': form})

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from order.models import Category, Item, Order, Product
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from  django.views import generic


@login_required(login_url="/accounts/login/")
def order(request, order_id=-1):
    item_form_set = modelformset_factory(Item, fields=('quantity',))
    categories = Category.objects.all()
    if request.method == 'POST':
        order_num = request.POST['order_id']
        if request.POST.__contains__('cancel'):
            return cancel_order(request, order_num)
        inst = Order.objects.get(pk=order_num)
        for product in Product.objects.all():
            if request.POST.__contains__(product.prod_name):
                inst.item_set.update(product=product, quantity=request.POST[product.prod_name])
        return confirmation(request, order_num)
    elif order_id != -1:
        inst = Order.objects.get(pk=order_id)
        formset = item_form_set(queryset=inst.items.through)
        context = {
            "formset": formset,
            "order_num": order_id,
            "categories": categories
        }
        return render(request, "orders/order.html", context)
    elif order_id == -1:
        inst = Order.objects.filter(recipient=request.user).latest('id');
        for product in Product.objects.all():
            if product.prod_name not in inst.item_set.values_list('product__prod_name', flat=True):
                item = Item(quantity=0, product=product, order=inst)
                item.save()
                inst.item_set.add(item)
        context = {
            "order": inst,
            "categories": categories
        }
        return render(request, "orders/order.html", context)


@login_required(login_url="/accounts/login/")
def details(request):
    orders_list = Order.objects.filter(recipient=request.user)
    context = {
        "orders_list": orders_list
    }
    return render(request, "orders/index.html", context)


@login_required(login_url="/accounts/login/")
def confirmation(request, order_id=1):
    inst = Order.objects.get(id=order_id)
    items = Item.objects.filter(order=inst)
    context = {
        "items": items,
        "order": inst
    }
    return render(request, "orders/confirmation.html", context)


def cancel_order(request, order_id):
    inst = Order.objects.get(id=order_id)
    inst.delete()
    return HttpResponseRedirect(reverse('orders:index'))


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/index.html'
    context_object_name = 'latest_order_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return Order.objects.filter(recipient=self.request.user).order_by('-date_created')


def login(request):
    user = ""
    if user is not None and user.is_authenticated:
        login(request, user)
        request.session.setdefault('recipient_id', user.id)
        context = {'user': user}
        return render(request, "details", context)
    else:
        return render(request, "orders/index.html")


def logout_view(request):
    return logout_then_login(request)


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'orders/order-details.html'
    queryset = Order.objects.all()

    def get_object(self):
        order = super(OrderDetailView, self).get_object()
        return order

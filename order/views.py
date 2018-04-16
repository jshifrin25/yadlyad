from django.urls import reverse
from django.http.response import HttpResponseRedirect,  JsonResponse
from django.shortcuts import render
from order.models import Category, Item, Order
from django.forms.models import modelformset_factory
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from  django.views import generic


@login_required(login_url="/accounts/login/")
def order(request, order_id=-1):
    item_form_set = modelformset_factory(Item,  form=ItemForm)
    categories = Category.objects.all()
    if request.method == 'POST':
        order_num = request.POST['order_id']
        if request.POST.__contains__('cancel'):
            return cancel_order(request, order_num)
        inst = Order.objects.get(pk=order_num)
        print(request.POST['submit'])
        formset = item_form_set(request.POST)
        print(formset.as_p)
        if formset.is_valid():
            print("Formset is valid")
            print(formset.as_p)
            formset.save()
        return confirmation(request, inst)
    else:
        order = Order.objects.filter(recipient=request.user).latest('id')
        if order_id != -1:
            print('duplicating order',  order_id)
            items = duplicate(order,  order_id)
        else:
            items = Item.objects.filter(order__id = order.id)
        formset = item_form_set(queryset = items)
        context = {
            "formset": formset,
            "order_num": order.id,
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
def confirmation(request, inst):
    context = {
        "order": inst
    }
    return render(request, "orders/confirmation.html", context)


def cancel_order(request, order_id):
    inst = Order.objects.get(id=order_id)
    inst.delete()
    return HttpResponseRedirect(reverse('orders:index'))
    
def reset_order(request):
    item_set = Item.objects.filter(order__id = request.POST['order'])
    dict = {}
    for item in item_set:
        dict[item.product.prod_name] = item.quantity
    return JsonResponse(dict,  safe=False)
    
def duplicate(order,  id):
    queryset = order.item_set.all()
    dup_order = Order.objects.get(pk = id)
    for entry in dup_order.item_set.all():
        queryset.filter(product__prod_name = entry.product.prod_name).update(quantity = entry.quantity)
    return queryset

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
        

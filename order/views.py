from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from order.models import Category, Item, Order, Product
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
        formset = item_form_set(queryset=Item.objects.filter(order__id=order.id))
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

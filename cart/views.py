from django.views.generic import ListView, CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from products.models import Product
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render




class CartListView(ListView, LoginRequiredMixin):
    template_name = 'cart_detail.html'

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        cart_items = {}

        # Fetch actual Product objects based on their IDs
        for product_id, quantity in cart.items():
            product = Product.objects.get(pk=product_id)
            cart_items[product] = quantity

        return render(request, 'cart_detail.html', {'cart': cart_items})

    def get_queryset(self):
        return self.request.session.get('cart', [])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_queryset()
        context['cart_items'] = Product.objects.filter(id__in=cart.keys())
        context['cart'] = cart  # {product_id: quantity}
        return context
    
    
class ClearCartView(View):
    def post(self, request, *args, **kwargs):
        request.session['cart'] = {}
        return HttpResponseRedirect(reverse('cart_detail'))
    


class AddToCartView(LoginRequiredMixin, CreateView):
    model = Product
    fields = []
    success_url = reverse_lazy('cart_detail')
    
    def post(self, request, *args, **kwargs):
        product_id = str(self.kwargs.get('pk'))
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        # If product is already in the cart, update quantity
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

        request.session['cart'] = cart
        return HttpResponseRedirect(reverse('cart_detail'))

    def form_valid(self, form):
        print('form_valid()')
        product_id = self.kwargs['pk']
        cart = self.request.session.get('cart', [])
        if product_id not in cart:
            cart.append(product_id)
        self.request.session['cart'] = cart
        return HttpResponseRedirect(self.get_success_url())


class RemoveFromCartView(View):
    def post(self, request, product_id, *args, **kwargs):
        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
        request.session['cart'] = cart
        return redirect(reverse('product_list'))

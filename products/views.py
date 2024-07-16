from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

def set_liked_by_user(products, user):
    if not isinstance(products, list):
            products = [products]

    for product in products:
        if user.is_authenticated:
            product.liked = user in product.liked_by.all()
        else:
            product.liked = False
    return products

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_name = self.kwargs.get('category', None)
        if category_name:
            category = get_object_or_404(Category, name=category_name)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = list(context['object_list'])  # Convert QuerySet to list
        set_liked_by_user(products, self.request.user)
        context['object_list'] = products  # Update the context
        context['categories'] = Category.objects.all()  # To show categories as filters
        return context
    


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_liked_by_user([context['object']], self.request.user)

        return context

    


class LikeProductView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product = Product.objects.get(id=product_id)

        if request.user in product.liked_by.all():
            product.liked_by.remove(request.user)
        else:
            product.liked_by.add(request.user)

        referer_url = request.META.get('HTTP_REFERER', reverse('product_list'))
        return_url = reverse('product_detail', args=[product_id])
        if return_url not in referer_url:
            return_url = reverse('product_list')

        return HttpResponseRedirect(return_url) 
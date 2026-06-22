from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.db.models import Q
from django.http import HttpResponseRedirect
from .models import Product, CartItem, Order, OrderItem
from .forms import ProductForm, OrderForm


class ProductListView(ListView):
    template_name = 'webapp/products.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        qs = Product.objects.filter(stock__gte=1).order_by('category__title', 'title')
        query = self.request.GET.get('q', '')
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class ProductDetailView(DetailView):
    template_name = 'webapp/product_detail.html'
    model = Product
    context_object_name = 'product'


class ProductCreateView(CreateView):
    template_name = 'webapp/product_form.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products')


class ProductUpdateView(UpdateView):
    template_name = 'webapp/product_form.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products')


class ProductDeleteView(DeleteView):
    template_name = 'webapp/product_delete.html'
    model = Product
    success_url = reverse_lazy('products')


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.stock < 1:
            return redirect('products')
        cart_item, created = CartItem.objects.get_or_create(product=product)
        if not created:
            if cart_item.quantity < product.stock:
                cart_item.quantity += 1
                cart_item.save()
        return redirect('products')


class CartRemoveView(View):
    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')


class CartDeleteView(View):
    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        cart_item.delete()
        return redirect('cart')


class CartView(ListView):
    template_name = 'webapp/cart.html'
    model = CartItem
    context_object_name = 'cart_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = sum(item.total() for item in self.object_list)
        context['order_form'] = OrderForm()
        return context


class OrderCreateView(View):
    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            cart_items = CartItem.objects.all()
            if cart_items:
                order = form.save()
                for item in cart_items:
                    OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                    # Списание остатка
                    item.product.stock -= item.quantity
                    if item.product.stock < 0:
                        item.product.stock = 0
                    item.product.save()
                cart_items.delete()
        return redirect('products')
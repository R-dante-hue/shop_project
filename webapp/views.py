from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm, SearchForm


def products_view(request):
    products = Product.objects.filter(stock__gte=1).order_by('category__title', 'title')
    search_form = SearchForm(request.GET or None)
    if search_form.is_valid() and search_form.cleaned_data.get('title'):
        products = products.filter(title__icontains=search_form.cleaned_data['title'])
    return render(request, 'webapp/products.html', {'products': products, 'search_form': search_form})


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'webapp/product_detail.html', {'product': product})


def product_add_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, categories=categories)
        if form.is_valid():
            Product.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data.get('description', ''),
                category_id=form.cleaned_data['category'],
                price=form.cleaned_data['price'],
                image_url=form.cleaned_data['image_url'],
                stock=form.cleaned_data['stock'],
            )
            return redirect('products')
    else:
        form = ProductForm(categories=categories)
    return render(request, 'webapp/product_form.html', {'form': form, 'button_text': 'Добавить', 'title_text': 'Добавить товар'})


def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, categories=categories)
        if form.is_valid():
            product.title = form.cleaned_data['title']
            product.description = form.cleaned_data.get('description', '')
            product.category_id = form.cleaned_data['category']
            product.price = form.cleaned_data['price']
            product.image_url = form.cleaned_data['image_url']
            product.stock = form.cleaned_data['stock']
            product.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(categories=categories, initial={
            'title': product.title,
            'description': product.description,
            'category': product.category_id,
            'price': product.price,
            'image_url': product.image_url,
            'stock': product.stock,
        })
    return render(request, 'webapp/product_form.html', {'form': form, 'button_text': 'Сохранить', 'title_text': 'Редактировать товар'})


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'webapp/product_delete.html', {'product': product})
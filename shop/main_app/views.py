from django.shortcuts import render
from django.views.generic import DetailView, View

from .models import NoteBook, Smartphone, Category, LatestProducts
from .mixins import CategoryDetailMixin


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_header_drop_list()
        products = LatestProducts.objects.get_products_for_main_page('notebook', 'smartphone')
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, 'base.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        'notebook': NoteBook,
        'smartphone': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

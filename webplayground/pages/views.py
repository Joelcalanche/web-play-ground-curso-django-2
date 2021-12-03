from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import Page
from django.urls import reverse , reverse_lazy
from .forms import PageForm

# # Create your views here.
# def pages(request):
#     pages = get_list_or_404(Page)
#     return render(request, 'pages/pages.html', {'pages':pages})

# def page(request, page_id, page_slug):
#     page = get_object_or_404(Page, id=page_id)
#     return render(request, 'pages/page.html', {'page':page})

class StaffRequiredMixin(object):
    """
    Este mixin requerira que el usuario sea miembro del staff

    """
    
    # def dispatch(self, request, *args, **kwargs ):
    #     if not request.user.is_staff:
    #         return redirect(reverse_lazy('admin:login')) 
    # #print(request.user)   
    #     return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

    """usando el metodo decorador de django, su y usamos decoradores nos ahorramos hacer el mixin"""
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs ):
 
  
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)



class PageListView(ListView):

    model = Page

class PageDetailView(DetailView):
    model = Page

# class PageCreate(StaffRequiredMixin, UpdateView):
""" arriba se muestra la clase usando mixin, abajo usando decoradorares"""

@method_decorator(staff_member_required, name="dispatch")
class PageCreate(CreateView):
    model = Page
    form_class = PageForm
    # fields = ['title','content', 'order']
    # def get_success_url(self):
    #     return reverse('pages:pages')
    # el codigo de arriba tambien funciona
    success_url = reverse_lazy('pages:pages')

    # este metodo nos permite contralar peticion como tal, cada vez que modifiquemos un metodo hacer el return de abajo
    # con esto podemos verificar si el usuario esta registrado o no, y si no esta lo redireccionamos al login del administrador
    # def dispatch(self, request, *args, **kwargs ):
    #     if not request.user.is_staff:
    #         return redirect(reverse_lazy('admin:login')) 
    #     #print(request.user)   
    #     return super(PageCreate, self).dispatch(request, *args, **kwargs)

@method_decorator(staff_member_required, name="dispatch")
class PageUpdate( UpdateView):
    model = Page
    form_class = PageForm
    # fields = ['title', 'content', 'order']
    template_name_suffix = '_update_form'
    # success_url = reverse_lazy('pages:pages')

    def get_success_url(self):
        return reverse_lazy('pages:update', args=[self.object.id]) + '?ok'
@method_decorator(staff_member_required, name="dispatch")
class PageDelete( DeleteView):
    model = Page
    
    success_url = reverse_lazy('pages:pages')
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Thread, Message


from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import  reverse_lazy
# Create your views here.
@method_decorator(login_required, name="dispatch")
class ThreadList(TemplateView):

   template_name = "messenger/thread_list.html"
   
    # model = Thread

    # filtraremos un queryset
    # def get_queryset(self):

    #     # con esto obtenemos todas las instancias de thread
    #     queryset = super(ThreadList,self).get_queryset()
    #     # filtramos por el usuario que este identificado en este momento
    #     return queryset.filter(users=self.request.user)

        # nos aprovechamos de la relacion inversa  pata ahorrarnos el codigo de arriba
@method_decorator(login_required, name="dispatch")
class ThreadDetail(DetailView):

    model = Thread

    def get_object(self):

        obj = super(ThreadDetail, self).get_object()

        if self.request.user not in obj.users.all():
            
            raise Http404()
        return obj


def add_message(request, pk):
    # print(request.GET)
    """comprobamos si el usuario esta identificado"""
    json_response ={'created':False}
    if request.user.is_authenticated:
        content = request.GET.get('content', None)
        if content:
            # obtenemos el  el hilo
            thread = get_object_or_404(Thread, pk=pk)
            # creamos el mensaje
            message = Message.objects.create(user=request.user, content=content)
            thread.messages.add(message)
            json_response ={'created':True}
            if len(thread.messages.all()) is  1:
                 json_response["first"] = True 
    else:
        raise Http404("User is not authenticated")

    

    # se transforma de un dicconario de python a un objeto java script
    return JsonResponse(json_response)

@login_required
def start_thread(request, username):
    # obtenemos el usuario con quien queremos empezar a conversar
    user = get_object_or_404(User, username=username)

    # creamos un hilo entre el usuario y nosotros
    thread = Thread.objects.find_or_create(user, request.user)

    # finalmente redireccionaos al hilo
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))
from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
# from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

from django.urls import reverse_lazy

from django import forms

from django.views.generic.edit import UpdateView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Profile
# Create your views here.

class SignUpView(CreateView):
    #  usamos el formulario generico
    form_class = UserCreationFormWithEmail
    # success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get_success_url(self):
        # con el signo de interrogacion recuperamos parametros get
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
      form = super(SignUpView, self).get_form()
      # Modificacion  en tiempo real
      
      form.fields["username"].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Nombre de usuario'})
      
      # recordar que estamos  extendiendo el usercreationform, debemos tener mucho cuidado con el re-escribir el campo widgects por que pudieramos borrar las configuraciones pre-establecidas      
      form.fields["email"].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Direccion de email'})
      
      form.fields["password1"].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Contraseña'})
      form.fields["password2"].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Repite la contraseña'})
    # el codigo de abajo esconde las label pero hay una forma mejor
    #   form.fields["username"].label = ""
    #   form.fields["password1"].label = ""
    #   form.fields["password2"].label = ""
      return form


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    # model = Profile
    # fields = ["avatar", "bio", "link"]
    success_url = reverse_lazy("profile")
    template_name = 'registration/profile_form.html'

    def get_object(self):

    #  Recuperar el objeto que se va a editar

    # con esto obtenmos el user a partir del user que tenemos en la request
    # en lugar de usar solo get, usaremos un get_or_create asi nos aseguramos de que si no existe se cree la instancia
    # definimos 2 variables debido a que se devuelve una tupla
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile




@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy("profile")
    template_name = 'registration/profile_email_form.html'

    def get_object(self):

        # recuperamos la instancia del usuario que queremos editar
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
      # Modificacion  en tiempo real
      
        form.fields["email"].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Email'})

        return form
      
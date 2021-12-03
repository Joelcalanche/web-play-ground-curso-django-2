from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
# Create your models here.
from django.db.models.signals import post_save

def custom_upload_to(instance, filename):

    # recuperas la instancia(imagen) justo a como estaba antes de guardarla
    old_instance = Profile.objects.get(pk=instance.pk)

    old_instance.avatar.delete()

    return 'profiles/' + filename


class Profile(models.Model):
    # crearemos una relaciion
    # con esto indicamos que solo puede haber un perfil por cada usuario
    # no se pueden tener varios usuarios para un perfil ni varios perfiles para un usuario
    
    """
    tipos de relaciones en django
    - OneToOneField(1:1) 1 usuario- perfil(unica para ambos sentidos)
    - ForeignKeyField(1:N) 1 autor <- N entradas(unica en un solo sentido)
    - ManyToManyField(N:M) Nentradas<->Mcategorias(bilateral)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    link = models.URLField(max_length=200, null=True, blank=True)
    class Meta:
        ordering = ['user__username']

    # para servir imagenes necesitamos usar pillow y en setting crear una seccion para servir media y cada vez que creemos un modelo debemos ir a  setting y luego realizar las migraciones

"""
existen estos tipos de señales
antes de guardar las instancias(pre_save)
justo despues de guardarlas(post_save)
justo antes de borrarla(pre_delete)
justo despues de borrarla(post_delete)

"""
# estamos configurando una señal para que se ejecute una funcion en un momento determinado de la vida de una instancia
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):

    # si existe esta clave sera la primera vez que se cree, devolvemos por defecto false en caso de que no exista esta clave
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        # print("Se acaba de crear un usuario y su perfil enlazado")
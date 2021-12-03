from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]

"""

CREANDO OBJECT MANAGER


"""
# con el podemos definir nuestros propios metodos
class ThreadManager(models.Manager):
    def find(self, user_1, user_2):
        #  dentro de un object manager self hace referencia a el query-set que contiene todas las instancias de un modelo
        #self ees equivalente a Thread.objects.all()
        queryset = self.filter(users=user_1).filter(users=user_2)

        # si hay almenos un elemento
        if len(queryset) > 0:
            return queryset[0]
        return None

    def find_or_create(self, user_1, user_2):

        thread = self.find(user_1, user_2)

        if thread is None:

            thread = Thread.objects.create()
            thread.users.add(user_1, user_2)
        
        return thread








# el thread es algo asi como un lugar o punto de encuentro que almacena los usuarios y los mensajes de esos usuarios
class Thread(models.Model):

    users = models.ManyToManyField(User, related_name="threads")

    messages = models.ManyToManyField(Message)

    # los campos many2many se gestionan a parte del updated, por lo que nosotros mismos debemos forzar el guardado 
    updated = models.DateTimeField(auto_now=True)
    
    objects = ThreadManager()
    
    class Meta:

        ordering = ["-updated"] 
    
    
    """ queremos poder hacer algo como esto Thread.objects.find(user1, user2), osea dado un hilo encontrar los usuarios"""

def messages_changed(sender, **kwargs):
    instance = kwargs.pop("instance", None)

    action = kwargs.pop("action", None)

    # almacena los identificadores de los mensajes
    pk_set = kwargs.pop("pk_set", None)

    print(instance, action, pk_set)

    # interceptaremos y borraremoss los mensajes de primary key set


    # creamos un conjunto para capturarlo
    false_pk_set = set()
    # antes de agregar a la instancia
    if action is "pre_add":
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user not in instance.users.all():
                print("Ups, ({}) no forma parte del hilo".format(msg.user))
                false_pk_set.add(msg_pk)


    """
    buscaremos los mensajes que estaran en el false pk que estan en pk_set y los borramos
    usando diferencia de conjuntos
    """ 
    pk_set.difference_update(false_pk_set)         

# estamos conectando la se;al con cualquier cambio en  el campo manytomany messages
# m2m_changed.connect(messages_changed, sender=Thread.messages.through)
# esta es otra forma de modificar  una funcion

    # forzaremos la actualizacion haciendo un save
    instance.save()
# estoy registrando tomando como referencia el campo messages del modelo Thread
m2m_changed.connect(messages_changed, sender=Thread.messages.through)
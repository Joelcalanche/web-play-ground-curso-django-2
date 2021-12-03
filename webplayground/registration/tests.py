from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
# Create your tests here.

class ProfileTestCase(TestCase):
    # aqui preparamos la prueba
    def setUp(self):
        # creamos un usuario de prueba
        User.objects.create_user('test','test@test.com', 'test1234')
   # aqui ejecutamos las pruebas, debemos cuidar que empiece con test_
    def test_profile_exists(self):
        # esto me devolvera true o false
        exists = Profile.objects.filter(user__username='test').exists()

        self.assertEqual(exists, True)


    
from django.test import TestCase, Client
from lesson import models
# Create your tests here.


class MaterialTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = models.User()
        self.user.save()

    def test_material_create_return_200(self):
        response = self.client.post('/create/',
                                    {'title': 'testtitle',
                                     'body': 'mybody',
                                     'material_type': 'typetype'},
                                    )

        print(models.Material.objects.first())
        self.assertEqual(response.status_code, 200)


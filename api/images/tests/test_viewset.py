from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from images.factories import ImageFactory
from helpers import ALLOWED_IMAGE_FORMAT


class ImageViewSetTest(APITestCase):
    @staticmethod
    def _create_example_image(name, new_gif=None):
        gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00"
            b"\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
            if not new_gif
            else new_gif
        )
        obj = SimpleUploadedFile(name, gif, content_type="image/gif")
        data = {"title": "random_title", "height": 400, "width": 500, "attachment": obj}
        return data

    def setUp(self):
        self.image = ImageFactory()
        self.images_url = reverse("images-list")
        self.image_url = reverse("images-detail", kwargs={"pk": self.image.pk})

    def test_list(self):
        response = self.client.get(self.images_url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue((data["results"]))

        obj = data["results"][0]
        self.assertTrue(obj["id"])
        self.assertTrue(obj["title"])
        self.assertTrue(obj["height"])
        self.assertTrue(obj["width"])
        self.assertTrue(obj["url"])

    def test_retrieve(self):
        response = self.client.get(self.image_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = response.json()
        self.assertEqual(obj["id"], self.image.pk)

    def test_create(self):
        gif = self._create_example_image("random.gif")
        response = self.client.post(self.images_url, data=gif, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create__when_wrong_extension_provided__then_return_bad_request(self):
        gif = self._create_example_image("another_random.jp2")
        response = self.client.post(self.images_url, data=gif, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["attachment"],
            [f"Extension not recognized. Please use one of {ALLOWED_IMAGE_FORMAT}"],
        )

    def test_create__when_size_too_large__then_return_bad_request(self):
        gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00"
            b"\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
            * 1000000
        )
        data = self._create_example_image("super_another_random.jpeg", gif)
        response = self.client.post(self.images_url, data=data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["attachment"],
            ["Files too large. Size should not exceed 10.0 MB."],
        )

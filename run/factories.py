from pdb import set_trace as debug

import factory

from django.contrib.auth.models import User

from .models import Author, Publisher


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = 'robert'


class AuthorFactory(factory.DjangoModelFactory):
    class Meta:
        model = Author

    name = 'Henry Miller'


class PublisherFactory(factory.DjangoModelFactory):
    class Meta:
        model = Publisher

    house = 'Random House'

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for author in authors:
                self.authors.add(author)

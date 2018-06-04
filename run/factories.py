import factory

from django.contrib.auth.models import User

#from .models import List, ListType, Item


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = 'robert'


#class ListTypeFactory(factory.DjangoModelFactory):
#    class Meta:
#        model = ListType
#
#    type = 'Member'
#
#
#class ListFactory(factory.DjangoModelFactory):
#    class Meta:
#        model = List
#
#    owner = factory.SubFactory(UserFactory)
#    type = factory.SubFactory(ListTypeFactory)
#
#
#class ItemFactory(factory.DjangoModelFactory):
#    class Meta:
#        model = Item
#
#    type = factory.SubFactory(ListTypeFactory)
#    #value = 1
#
#    @factory.post_generation
#    def lists(self, create, extracted, **kwargs):
#        if not create:
#            # Simple build, do nothing.
#            return
#
#        if extracted:
#            # A list of groups were passed in, use them
#            for list in extracted:
#                self.lists.add(list)

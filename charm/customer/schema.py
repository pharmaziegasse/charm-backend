import graphene

from django.contrib.auth import get_user_model

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import permission_required, login_required

from .models import Customer

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class CustomerQType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class Query(graphene.AbstractType):
    # Returns all Customeres
    customer_all = graphene.List(
        CustomerQType,
        token=graphene.String(required=False)
    )
    
    # Returns a single Customer object based on given id
    customer_by_id = graphene.Field(
        CustomerQType,
        token=graphene.String(required=False),
        id=graphene.Int(required=True)
    )
    
    # Returns a single Customer object with given phone number
    customer_by_phone = graphene.Field(
        CustomerQType,
        token=graphene.String(required=False),
        phone=graphene.String(required=True)
    )

    # Returns a single Customer object with given username
    customer_by_name = graphene.Field(
        CustomerQType,
        token=graphene.String(required=False),
        username=graphene.String(required=True)
    )

    @permission_required('user.coach')
    def resolve_customer_all(self, info, **_kwargs):
        return Customer.objects.all()

    @permission_required('user.coach')
    def resolve_customer_by_id(self, info, id, **_kwargs):
        return Customer.objects.get(id=id)

    @permission_required('user.coach')
    def resolve_customer_by_phone(self, info, phone, **_kwargs):
        return Customer.objects.get(telephone=phone)

    @permission_required('user.coach')
    def resolve_customer_by_name(self, info, username, **_kwargs):
        return Customer.objects.get(username=username)
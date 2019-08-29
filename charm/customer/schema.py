import graphene

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import staff_member_required, login_required

from .models import Customer

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class Query(graphene.AbstractType):
    # Returns all Customeres
    customer_all = graphene.List(
        CustomerType,
        token=graphene.String(required=False)
    )
    
    # Returns a single Customer object based on given id
    customer_by_id = graphene.Field(
        CustomerType,
        token=graphene.String(required=False),
        id=graphene.Int(required=True)
    )
    
    # Returns a single Customer object with given phone number
    customer_by_phone = graphene.Field(
        CustomerType,
        token=graphene.String(required=False),
        phone=graphene.String(required=True)
    )

    # Returns a single Customer object with given username
    customer_by_name = graphene.Field(
        CustomerType,
        token=graphene.String(required=False),
        username=graphene.String(required=True)
    )

    @staff_member_required
    def resolve_customer_all(self, info, **_kwargs):
        return Customer.objects.all()

    @staff_member_required
    def resolve_customer_by_id(self, info, id, **_kwargs):
        return Customer.objects.get(id=id)

    @staff_member_required
    def resolve_customer_by_phone(self, info, phone, **_kwargs):
        return Customer.objects.get(telephone=phone)

    @staff_member_required
    def resolve_customer_by_name(self, info, username, **_kwargs):
        return Customer.objects.get(username=username)
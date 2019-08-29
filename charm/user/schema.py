import graphene

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import staff_member_required, login_required

from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class Query(graphene.AbstractType):
    # Returns all users
    user_all = graphene.List(
        UserType,
        token=graphene.String(required=False)
    )
    
    # Returns a single user object based on given id
    user_by_id = graphene.Field(
        UserType,
        token=graphene.String(required=False),
        id=graphene.Int(required=True)
    )
    
    # Returns a single user object with given phone number
    user_by_phone = graphene.Field(
        UserType,
        token=graphene.String(required=False),
        phone=graphene.String(required=True)
    )

    # Returns a single user object with given username
    user_by_name = graphene.Field(
        UserType,
        token=graphene.String(required=False),
        username=graphene.String(required=True)
    )

    # Returns the username of a user object with a given phone number
    username_by_phone = graphene.Field(
        graphene.String,
        token=graphene.String(required=False),
        phone=graphene.String(required=True)
    )

    # Returns the username of a user object with a given email address
    username_by_email = graphene.Field(
        graphene.String,
        token=graphene.String(required=False),
        email=graphene.String(required=True)
    )

    # Returns currently logged in user object
    user_self = graphene.Field(
        UserType,
        token=graphene.String(required=False)
    )

    @staff_member_required
    def resolve_user_all(self, info, **_kwargs):
        return get_user_model().objects.all()

    @staff_member_required
    def resolve_user_by_id(self, info, id, **_kwargs):
        return get_user_model().objects.get(id=id)

    @staff_member_required
    def resolve_user_by_phone(self, info, phone, **_kwargs):
        return get_user_model().objects.get(telephone=phone)

    @staff_member_required
    def resolve_user_by_name(self, info, username, **_kwargs):
        return get_user_model().objects.get(username=username)

    @login_required
    def resolve_username_by_phone(self, info, phone, **_kwargs):
        user = get_user_model().objects.get(telephone=phone)
        return user.username

    @login_required
    def resolve_username_by_email(self, info, email, **_kwargs):
        user = get_user_model().objects.get(email=email)
        return user.username

    @login_required
    def resolve_user_self(self, info, **_kwargs):
        user = info.context.user
        return user
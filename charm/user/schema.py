import graphene

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import permission_required, login_required

from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class SetPasswordMutation(graphene.Mutation):
    # Result returns true if successfull and false if the action failed
    result = graphene.Field(graphene.Boolean)
    # A detailed, human-readable return message about what happend
    message = graphene.Field(graphene.String)
    # Short, single-string return message
    msg_code = graphene.Field(graphene.String)

    class Arguments:
        username = graphene.String(required=True)
        activation_token = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, activation_token, password):
        user = get_user_model().objects.get(username=username)

        if user.activation_url == None:
            return SetPasswordMutation(False, "No password reset process initiated.", "no_password_process")

        if not user.activation_url == activation_token:
            return SetPasswordMutation(False, "Failed due to invalid activation token.", "invalid_activation_token")

        get_user_model().set_password(user, password)
        user.activation_url = None
        user.save()

        return SetPasswordMutation(True, "Password set successfully.", "success")

class PasswordResetMutation(graphene.Mutation):
    pass

class Mutation(graphene.ObjectType):
    set_password = SetPasswordMutation.Field()
    password_reset_activation = PasswordResetMutation.Field()

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

    @permission_required('user.coach')
    def resolve_user_all(self, info, **_kwargs):
        return get_user_model().objects.all()

    @permission_required('user.coach')
    def resolve_user_by_id(self, info, id, **_kwargs):
        return get_user_model().objects.get(id=id)

    @permission_required('user.coach')
    def resolve_user_by_phone(self, info, phone, **_kwargs):
        return get_user_model().objects.get(telephone=phone)

    @permission_required('user.coach')
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
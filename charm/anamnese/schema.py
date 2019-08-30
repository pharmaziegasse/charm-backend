import graphene

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import permission_required, login_required

from django.contrib.auth import get_user_model

from .models import Anamnese

class AnamneseType(DjangoObjectType):
    class Meta:
        model = Anamnese

class Query(graphene.AbstractType):
    # Users should not be able to see their own anamneses.
    # myan = graphene.List(AnamneseType, token=graphene.String(required=False))
    
    # Returns all anamneses
    an_all = graphene.List(
        AnamneseType,
        token=graphene.String(required=False)
    )
    
    # Returns a single anamnese based on given id
    an_by_id = graphene.Field(
        AnamneseType,
        token=graphene.String(required=False),
        id=graphene.Int(required=True)
    )
    
    # Returns all anamneses of a user with given id
    an_by_uid = graphene.List(
        AnamneseType,
        token=graphene.String(required=False),
        uid=graphene.Int(required=True)
    )

    # Returns the latest anamnese of a user with given id
    an_latest_by_uid = graphene.Field(
        AnamneseType,
        token=graphene.String(required=False),
        uid=graphene.Int(required=True)
    )

    @permission_required('user.coach')
    def resolve_an_all(self, info, **_kwargs):
        return Anamnese.objects.all()

    @permission_required('user.coach')
    def resolve_an_by_id(self, info, id, **_kwargs):
        return Anamnese.objects.get(id=id)

    @permission_required('user.coach')
    def resolve_an_by_uid(self, info, uid, **_kwargs):
        return Anamnese.objects.filter(user=get_user_model().objects.get(id=uid))

    @permission_required('user.coach')
    def resolve_an_latest_by_uid(self, info, uid, **_kwargs):
        return Anamnese.objects.filter(user=get_user_model().objects.get(id=uid)).latest()

    # @login_required
    # def resolve_myan(self, info, **_kwargs):
    #     user = info.context.user
    #     return Anamnese.objects.filter(user=user)
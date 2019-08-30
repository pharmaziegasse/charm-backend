import graphene

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import permission_required, login_required

from .models import Coach

class CoachType(DjangoObjectType):
    class Meta:
        model = Coach

class Query(graphene.AbstractType):
    # Returns all coaches
    coach_all = graphene.List(
        CoachType,
        token=graphene.String(required=False)
    )
    
    # Returns a single coach object based on given id
    coach_by_id = graphene.Field(
        CoachType,
        token=graphene.String(required=False),
        id=graphene.Int(required=True)
    )
    
    # Returns a single coach object with given phone number
    coach_by_phone = graphene.Field(
        CoachType,
        token=graphene.String(required=False),
        phone=graphene.String(required=True)
    )

    # Returns a single coach object with given username
    coach_by_name = graphene.Field(
        CoachType,
        token=graphene.String(required=False),
        username=graphene.String(required=True)
    )

    @permission_required('user.coach')
    def resolve_coach_all(self, info, **_kwargs):
        return Coach.objects.all()

    @permission_required('user.coach')
    def resolve_coach_by_id(self, info, id, **_kwargs):
        return Coach.objects.get(id=id)

    @permission_required('user.coach')
    def resolve_coach_by_phone(self, info, phone, **_kwargs):
        return Coach.objects.get(telephone=phone)

    @permission_required('user.coach')
    def resolve_coach_by_name(self, info, username, **_kwargs):
        return Coach.objects.get(username=username)
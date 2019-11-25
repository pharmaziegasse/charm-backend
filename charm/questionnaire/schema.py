import graphene

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import permission_required, login_required

from django.contrib.auth import get_user_model

from .models import Questionnaire_1, Questionnaire_2, Questionnaire_3

class Questionnaire_1_Type(DjangoObjectType):
    class Meta:
        model = Questionnaire_1

class Questionnaire_2_Type(DjangoObjectType):
    class Meta:
        model = Questionnaire_2

class Questionnaire_3_Type(DjangoObjectType):
    class Meta:
        model = Questionnaire_3

class Query(graphene.AbstractType):
    # Questionnaire 1
    # Returns all questionnaires
    q1_all = graphene.List(
        Questionnaire_1_Type,
        token=graphene.String(required=False)
    )
    
    # Returns a single questionnaire based on given id
    q1_by_id = graphene.Field(
        Questionnaire_1_Type,
        token=graphene.String(required=False),
        id=graphene.Int(required=True)
    )
    
    # Returns all questionnaires of a user with given id
    q1_by_uid = graphene.List(
        Questionnaire_1_Type,
        token=graphene.String(required=False),
        uid=graphene.Int(required=True)
    )

    # Returns the latest questionnaire of a user with given id
    q1_latest_by_uid = graphene.Field(
        Questionnaire_1_Type,
        token=graphene.String(required=False),
        uid=graphene.Int(required=True)
    )

    # Questionnaire 2
    # Returns all questionnaires
    q2_all = graphene.List(
        Questionnaire_2_Type,
        token=graphene.String(required=False)
    )
    
    # Returns a single questionnaire based on given id
    q2_by_id = graphene.Field(
        Questionnaire_2_Type,
        token=graphene.String(required=False),
        id=graphene.Int(required=True)
    )
    
    # Returns all questionnaires of a user with given id
    q2_by_uid = graphene.List(
        Questionnaire_2_Type,
        token=graphene.String(required=False),
        uid=graphene.Int(required=True)
    )

    # Returns the latest questionnaire of a user with given id
    q2_latest_by_uid = graphene.Field(
        Questionnaire_2_Type,
        token=graphene.String(required=False),
        uid=graphene.Int(required=True)
    )

    # Questionnaire 3
    # Returns all questionnaires
    q3_all = graphene.List(
        Questionnaire_3_Type,
        token=graphene.String(required=False)
    )
    
    # Returns a single questionnaire based on given id
    q3_by_id = graphene.Field(
        Questionnaire_3_Type,
        token=graphene.String(required=False),
        id=graphene.Int(required=True)
    )
    
    # Returns all questionnaires of a user with given id
    q3_by_uid = graphene.List(
        Questionnaire_3_Type,
        token=graphene.String(required=False),
        uid=graphene.Int(required=True)
    )

    # Returns the latest questionnaire of a user with given id
    q3_latest_by_uid = graphene.Field(
        Questionnaire_3_Type,
        token=graphene.String(required=False),
        uid=graphene.Int(required=True)
    )

    # Questionnaire 1
    @permission_required('user.coach')
    def resolve_q1_all(self, info, **_kwargs):
        return Questionnaire_1.objects.all()

    @permission_required('user.coach')
    def resolve_q1_by_id(self, info, id, **_kwargs):
        return Questionnaire_1.objects.get(id=id)

    @permission_required('user.coach')
    def resolve_q1_by_uid(self, info, uid, **_kwargs):
        return Questionnaire_1.objects.filter(user=get_user_model().objects.get(id=uid))

    @permission_required('user.coach')
    def resolve_q1_latest_by_uid(self, info, uid, **_kwargs):
        return Questionnaire_1.objects.filter(user=get_user_model().objects.get(id=uid)).latest()

    # Questionnaire 2
    @permission_required('user.coach')
    def resolve_q2_all(self, info, **_kwargs):
        return Questionnaire_2.objects.all()

    @permission_required('user.coach')
    def resolve_q2_by_id(self, info, id, **_kwargs):
        return Questionnaire_2.objects.get(id=id)

    @permission_required('user.coach')
    def resolve_q2_by_uid(self, info, uid, **_kwargs):
        return Questionnaire_2.objects.filter(user=get_user_model().objects.get(id=uid))

    @permission_required('user.coach')
    def resolve_q2_latest_by_uid(self, info, uid, **_kwargs):
        return Questionnaire_2.objects.filter(user=get_user_model().objects.get(id=uid)).latest()

    # Questionnaire 3
    @permission_required('user.coach')
    def resolve_q3_all(self, info, **_kwargs):
        return Questionnaire_3.objects.all()

    @permission_required('user.coach')
    def resolve_q3_by_id(self, info, id, **_kwargs):
        return Questionnaire_3.objects.get(id=id)

    @permission_required('user.coach')
    def resolve_q3_by_uid(self, info, uid, **_kwargs):
        return Questionnaire_3.objects.filter(user=get_user_model().objects.get(id=uid))

    @permission_required('user.coach')
    def resolve_q3_latest_by_uid(self, info, uid, **_kwargs):
        return Questionnaire_3.objects.filter(user=get_user_model().objects.get(id=uid)).latest()

import graphene

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import staff_member_required, login_required

from django.contrib.auth import get_user_model

from .models import Beautyreport

class BeautyreportType(DjangoObjectType):
    class Meta:
        model = Beautyreport

class Query(graphene.AbstractType):
    # Returns all beautyreports
    br_all = graphene.List(
        BeautyreportType,
        token=graphene.String(required=False)
    )
    
    # Returns a single beautyreport based on given id
    br_by_id = graphene.Field(
        BeautyreportType,
        token=graphene.String(required=False),
        id=graphene.Int(required=True)
    )
    
    # Returns all beautyreports of a user with given id
    br_by_uid = graphene.List(
        BeautyreportType,
        token=graphene.String(required=False),
        uid=graphene.Int(required=True)
    )

    # Returns the latest beautyreport of a user with given id
    br_latest_by_uid = graphene.Field(
        BeautyreportType,
        token=graphene.String(required=False),
        uid=graphene.Int(required=True)
    )

    # Returns all beautyreports of the currently logged in user
    br_own = graphene.List(
        BeautyreportType,
        token=graphene.String(required=False)
    )

    # Returns the latest beautyreport of the currently logged in user
    br_latest_own = graphene.Field(
        BeautyreportType,
        token=graphene.String(required=False)
    )

    @staff_member_required
    def resolve_ab_all(self, info, **_kwargs):
        return Beautyreport.objects.all()

    @staff_member_required
    def resolve_ab_by_id(self, info, id, **_kwargs):
        return Beautyreport.objects.get(id=id)

    @staff_member_required
    def resolve_ab_by_uid(self, info, uid, **_kwargs):
        return Beautyreport.objects.filter(user=get_user_model().objects.get(id=uid))

    @staff_member_required
    def resolve_ab_latest_by_uid(self, info, uid, **_kwargs):
        return Beautyreport.objects.filter(user=get_user_model().objects.get(id=uid)).latest()

    @login_required
    def resolve_own(self, info, **_kwargs):
        user = info.context.user
        return Beautyreport.objects.filter(user=user)

    @login_required
    def resolve_latest_own(self, info, **_kwargs):
        user = info.context.user
        return Beautyreport.objects.filter(user=user).latest()
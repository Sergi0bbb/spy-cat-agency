from django.db import transaction
from django.db.models import QuerySet
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from spy_cat.models import SpyCat, Mission, Target
from spy_cat.serializers import (
    SpyCatSerializer,
    MissionSerializer,
    MissionListSerializer,
    MissionDetailSerializer,
    TargetUpdateSerializer,
)


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class MissionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def get_queryset(self) -> QuerySet[Mission]:
        queryset = super().get_queryset()

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("cat").prefetch_related("targets")

        return queryset

    def get_serializer_class(self) -> ModelSerializer:
        serializer_map = {
            "list": MissionListSerializer,
            "retrieve": MissionDetailSerializer,
            "assign_cat": MissionDetailSerializer,
            "update_targets": TargetUpdateSerializer,
        }
        return serializer_map.get(self.action, MissionSerializer)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        if instance.cat:
            return Response(
                {"detail": "Mission assigned to a cat cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if instance.is_complete:
            return Response(
                {"detail": "Completed missions cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["patch"])
    def update_targets(self, request: Request, pk: int = None) -> Response:
        mission = self.get_object()
        targets_data = request.data.get("targets", [])

        if not targets_data:
            raise ValidationError("No targets data provided.")

        updated_targets = []
        with transaction.atomic():
            for target_data in targets_data:
                target_id = target_data.get("id")
                if not target_id:
                    raise ValidationError("Target ID is required for each target.")

                target = get_object_or_404(Target, id=target_id)
                if target.mission_id != mission.id:
                    raise ValidationError(
                        f"Target ID {target_id} is not part of this mission."
                    )

                if mission.is_complete or target.is_complete:
                    raise ValidationError(
                        f"Cannot modify completed target (ID {target_id}) or mission."
                    )

                serializer = TargetUpdateSerializer(
                    target, data=target_data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                updated_targets.append(serializer.data)

        return Response(updated_targets, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def assign_cat(self, request: Request, pk: int = None) -> Response:
        mission = self.get_object()
        cat_id = request.data.get("cat_id")

        if mission.cat:
            return Response(
                {"detail": "This mission is already assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cat = get_object_or_404(SpyCat, pk=cat_id)
        if cat.mission_set.filter(is_complete=False).exists():
            return Response(
                {"detail": "This cat is already assigned to an incomplete mission."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        mission.cat = cat
        mission.save()

        return Response(
            MissionDetailSerializer(mission).data, status=status.HTTP_201_CREATED
        )

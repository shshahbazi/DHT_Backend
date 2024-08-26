from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from scoring.models import Feature, PurchasedFeature
from scoring.serializers import FeatureSerializer, PurchasedFeatureSerializer


class FeatureListApiView(APIView):
    @swagger_auto_schema(responses={200: FeatureSerializer(many=True)}, tags=['Features'])
    def get(self, request):
        features = Feature.objects.all()
        serializer = FeatureSerializer(features, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FeatureDetailApiView(APIView):
    @swagger_auto_schema(responses={200: FeatureSerializer()}, tags=['Features'])
    def get(self, request, pk):
        feature = Feature.objects.get(id=pk)
        serializer = FeatureSerializer(feature)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PurchaseFeatureApiView(APIView):
    @swagger_auto_schema(responses={201: None, 400: None}, tags=['Features'])
    def get(self, request, pk):
        feature = Feature.objects.get(id=pk)
        user = request.user

        if feature.get_feature(user=user):
            purchased_feature = PurchasedFeature.objects.create(user=user, feature=feature)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"You don't have enough score"})



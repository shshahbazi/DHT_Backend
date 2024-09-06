from django.db.models import Count
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mental.models import DailyMood
from mental.serializers import MoodTrackerSerializer


class SubmitMood(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=MoodTrackerSerializer(), responses={200: None}, tags=['MoodTracker'])
    def post(self, request):
        serializer = MoodTrackerSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        daily_mood = serializer.create(validated_data=serializer.validated_data)
        daily_mood.save()

        return Response(status=status.HTTP_201_CREATED)


class MoodDistributionApiView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: None}, tags=['MoodTracker'])
    def get(self, request):
        mood_names = {5: 'thrilled',
                      4: 'happy',
                      3: 'neutral',
                      2: 'sad',
                      1: 'verySad'}
        user = request.user
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=10)

        mood_counts = DailyMood.objects.filter(user=user, created_at__gte=start_date) \
            .values('mood').annotate(count=Count('mood'))

        mood_list = []

        mood_dict = {mood: 0 for mood in range(1, 6)}  # 1 تا 5

        for entry in mood_counts:
            mood_dict[entry['mood']] = entry['count']

        total_moods = sum(mood_dict.values())
        mood_percentages = {
            mood: (count / total_moods) * 100 if total_moods > 0 else 0
            for mood, count in mood_dict.items()
        }

        for key, value in mood_percentages.items():
            mood_data = {"name": f'{mood_names[key]}', "value": value}
            mood_list.append(mood_data)

        return Response(mood_list, status=status.HTTP_200_OK)

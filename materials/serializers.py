from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_not_youtube
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.CharField(validators=[validate_not_youtube])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)
    subscription_status = serializers.SerializerMethodField()

    @staticmethod
    def get_lessons_count(obj):
        return Lesson.objects.filter(course=obj).count()

    @staticmethod
    def get_lessons(obj):
        return [lesson.name for lesson in Lesson.objects.filter(course=obj)]

    def get_subscription_status(self, obj):
        user = self.context["request"].user
        if Subscription.objects.filter(user=user, course=obj).exists():
            return True
        return False

    class Meta:
        model = Course
        fields = ("id", "name", "description", "lessons_count", "lessons", "owner", "subscription_status")


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

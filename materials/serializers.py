from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_not_youtube


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.CharField(validators=[validate_not_youtube])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)

    @staticmethod
    def get_lessons_count(obj):
        return Lesson.objects.filter(course=obj).count()

    @staticmethod
    def get_lessons(obj):
        return [lesson.name for lesson in Lesson.objects.filter(course=obj)]

    class Meta:
        model = Course
        fields = ("id", "name", "description", "lessons_count", "lessons", "owner")

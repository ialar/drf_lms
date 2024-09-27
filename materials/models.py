from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    description = models.TextField(
        **NULLABLE, verbose_name="Описание курса", help_text="Опишите курс"
    )
    preview = models.ImageField(
        upload_to="materials/course_image",
        verbose_name="Изображение курса",
        help_text="Загрузите изображение для курса",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    description = models.TextField(
        **NULLABLE, verbose_name="Описание урока", help_text="Опишите урок"
    )
    preview = models.ImageField(
        upload_to="materials/lesson_image",
        verbose_name="Изображение урока",
        help_text="Загрузите изображение для урока",
        **NULLABLE
    )
    video = models.TextField(
        **NULLABLE, verbose_name="Ссылка на видео", help_text="Вставьте ссылку на видео"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="Выберите курс",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

# -*- coding: utf-8 -*-
"""
Команда: згенерувати або оновити конспекти всіх уроків до мінімум 1500 слів.
Уроки без контенту або з контентом < 1500 слів отримують новий конспект через ШІ.
"""
import re
from django.core.management.base import BaseCommand
from courses.models import Lesson
from courses.ai_service import generate_lesson_content


def word_count(html_text):
    if not html_text or not html_text.strip():
        return 0
    clean = re.sub(r"<[^>]+>", " ", html_text)
    return len(clean.split())


class Command(BaseCommand):
    help = 'Згенерувати/оновити конспекти всіх уроків до мінімум 1500 слів (ШІ).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Лише показати, які уроки були б оновлені, без виклику API.',
        )
        parser.add_argument(
            '--course',
            type=str,
            default=None,
            help='Slug курсу: обробити лише уроки цього курсу.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        course_slug = options.get('course')
        qs = Lesson.objects.select_related('course').all().order_by('course', 'order')
        if course_slug:
            qs = qs.filter(course__slug=course_slug)
        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.WARNING('Уроків не знайдено.'))
            return
        updated = 0
        skipped = 0
        errors = 0
        for lesson in qs:
            lang = (lesson.course.language or 'python').lower()
            wc = word_count(lesson.content or '')
            if wc >= 1500:
                skipped += 1
                self.stdout.write('Пропущено (вже 1500+ слів): {} - {}'.format(lesson.course.slug, lesson.title))
                continue
            if dry_run:
                self.stdout.write('[dry-run] Згенерував би: {} - {} (зараз слів: {})'.format(lesson.course.slug, lesson.title, wc))
                updated += 1
                continue
            self.stdout.write('Генерую конспект: {} - {} ...'.format(lesson.course.slug, lesson.title))
            content = generate_lesson_content(lesson.title, lang)
            if not content:
                self.stdout.write(self.style.ERROR('  Помилка генерації (перевір OPENAI_API_KEY).'))
                errors += 1
                continue
            lesson.content = content
            lesson.save(update_fields=['content'])
            new_wc = word_count(content)
            updated += 1
            self.stdout.write(self.style.SUCCESS('  Збережено, слів: {}'.format(new_wc)))
        self.stdout.write('')
        self.stdout.write('Готово. Оновлено: {}, пропущено: {}, помилок: {}.'.format(updated, skipped, errors))

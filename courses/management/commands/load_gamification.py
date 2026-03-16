# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from courses.models import League, Achievement, Competition, Quiz, Question, Course, Lesson


class Command(BaseCommand):
    help = 'Load leagues, achievements, competition and sample quizzes.'

    def handle(self, *args, **options):
        # ——— Ліги ———
        if not League.objects.exists():
            League.objects.create(name='Бронза', slug='bronze', min_points=0, icon='🥉', color='#cd7f32', order=0)
            League.objects.create(name='Срібло', slug='silver', min_points=100, icon='🥈', color='#c0c0c0', order=1)
            League.objects.create(name='Золото', slug='gold', min_points=500, icon='🥇', color='#ffd700', order=2)
            self.stdout.write('Leagues created.')

        # ——— Досягнення (мемчики) ———
        achievements = [
            ('first_lesson', 'Hello, World!', 'Заверши перший урок', '🐣', 10),
            ('lessons_5', 'Ще п\'ять хвилин, мамо', 'Заверши 5 уроків', '📚', 25),
            ('lessons_10', 'Я вже не той', 'Заверши 10 уроків', '🌟', 50),
            ('lessons_15', 'Синьйор девелопер', 'Заверши 15 уроків', '📖', 35),
            ('first_quiz', 'Перший раз не рахується', 'Пройди перший тест', '📝', 15),
            ('quiz_perfect', 'Чи то я, чи то ШІ', 'Пройди тест на 100%', '💯', 30),
            ('quizzes_5', 'Тести — моя любов', 'Пройди 5 тестів', '🎯', 20),
            ('quizzes_10', 'Готовий до продакшену', 'Пройди 10 тестів', '📋', 20),
            ('quizzes_50', 'Півсотні тестів не буває', 'Пройди 50 тестів', '📑', 40),
            ('quizzes_100', 'Легенда серед QA', 'Пройди 100 тестів', '🏆', 100),
            ('streak_3', 'Вогник запалився', '3 дні поспіль', '🔥', 20),
            ('streak_7', 'Тиждень без прокрастинації', '7 днів поспіль', '🔥', 50),
            ('streak_14', 'Два тижні — я змінився', '14 днів поспіль', '🔥', 80),
            ('points_100', 'Перша сотня, як у спорті', 'Набери 100 балів', '⭐', 0),
            ('points_500', 'Півтисячі — мама гордиться', 'Набери 500 балів', '🏆', 0),
            ('points_1000', 'Тисяча. Тепер я інфлюенсер', 'Набери 1000 балів', '👑', 0),
        ]
        for i, (ct, name, desc, icon, pts) in enumerate(achievements):
            obj, created = Achievement.objects.update_or_create(
                slug=ct,
                defaults={
                    'name': name,
                    'description': desc,
                    'icon': icon,
                    'points_reward': pts,
                    'condition_type': ct,
                    'order': i,
                }
            )
        self.stdout.write('Achievements synced.')

        # ——— Змагання ———
        if not Competition.objects.exists():
            start = timezone.now()
            end = start + timedelta(days=30)
            Competition.objects.create(
                name='Лютневий марафон',
                slug='feb-marathon',
                description='Збирай бали протягом місяця. Топ-20 потраплять у таблицю переможців.',
                start_at=start,
                end_at=end,
                is_active=True,
            )
            self.stdout.write('Competition created.')

        # ——— Зразкові тести ———
        py = Course.objects.filter(slug='python-basics').first()
        if py:
            lesson_first = py.lessons.order_by('order').first()
            if lesson_first and not Quiz.objects.filter(lesson=lesson_first).exists():
                q1 = Quiz.objects.create(
                    lesson=lesson_first,
                    course=py,
                    title='Перевірка: перша програма та змінні',
                    quiz_type='single_choice',
                    is_practice=False,
                    order=0,
                )
                Question.objects.create(
                    quiz=q1,
                    text='Яка функція в Python виводить текст на екран?',
                    order=0,
                    data={
                        'options': [
                            {'text': 'print()', 'correct': True},
                            {'text': 'echo()', 'correct': False},
                            {'text': 'console.log()', 'correct': False},
                            {'text': 'write()', 'correct': False},
                        ]
                    },
                )
                Question.objects.create(
                    quiz=q1,
                    text='Чи потрібно в Python оголошувати тип змінної?',
                    question_type='true_false',
                    order=1,
                    data={'correct': False},
                )
                Question.objects.create(
                    quiz=q1,
                    text='Що таке змінна в програмуванні?',
                    question_type='flashcard',
                    order=2,
                    data={'back': 'контейнер для зберігання даних'},
                )

                q2 = Quiz.objects.create(
                    lesson=lesson_first,
                    course=py,
                    title='Тренувальний: основи (без оцінки)',
                    quiz_type='ordering',
                    is_practice=True,
                    order=1,
                )
                Question.objects.create(
                    quiz=q2,
                    text='Розташуй рядки коду в правильному порядку для виводу привітання.',
                    question_type='ordering',
                    order=0,
                    data={'items': ['name = "User"', 'greeting = "Hello"', 'print(greeting, name)']},
                )

                q3 = Quiz.objects.create(
                    course=py,
                    title='Пари: термін — визначення (Python)',
                    quiz_type='match_pairs',
                    is_practice=False,
                    order=2,
                )
                Question.objects.create(
                    quiz=q3,
                    text='З\'єднай термін з визначенням.',
                    question_type='match_pairs',
                    order=0,
                    data={
                        'pairs': [
                            ['print', 'функція виводу'],
                            ['змінна', 'іменоване місце для значення'],
                            ['Python', 'мова програмування'],
                        ]
                    },
                )

                q4 = Quiz.objects.create(
                    course=py,
                    title='Пропущене слово (код)',
                    quiz_type='fill_blank',
                    is_practice=False,
                    order=3,
                )
                Question.objects.create(
                    quiz=q4,
                    text='Встав пропущене: для виводу в Python використовується ___("текст").',
                    question_type='fill_blank',
                    order=0,
                    data={'text': 'Для виводу в Python використовується ___("текст").', 'blanks': ['print']},
                )

                self.stdout.write('Sample quizzes created.')
        self.stdout.write(self.style.SUCCESS('Gamification data loaded.'))

# -*- coding: utf-8 -*-
"""
Створює вступні тести (визначення рівня) для кожного опублікованого курсу.
Питання залежать від мови курсу (Python / JavaScript).
Запуск: python manage.py create_placement_quizzes
"""
from django.core.management.base import BaseCommand
from courses.models import Course, Quiz, Question


# Питання для вступного тесту (універсальні / основи програмування)
PLACEMENT_QUESTIONS_COMMON = [
    {
        'text': 'Що таке змінна в програмуванні?',
        'question_type': 'single_choice',
        'data': {
            'options': [
                {'text': 'Команда для виводу тексту', 'correct': False},
                {'text': 'Іменоване місце в пам\'яті для зберігання значення', 'correct': True},
                {'text': 'Назва програми', 'correct': False},
                {'text': 'Тип помилки', 'correct': False},
            ]
        },
    },
    {
        'text': 'У більшості мов програмування нумерація індексів у списку (масиві) починається з нуля.',
        'question_type': 'true_false',
        'data': {'correct': True},
    },
    {
        'text': 'Що робить умовний оператор if?',
        'question_type': 'single_choice',
        'data': {
            'options': [
                {'text': 'Повторює код кілька разів', 'correct': False},
                {'text': 'Виконує код лише за певної умови', 'correct': True},
                {'text': 'Закриває програму', 'correct': False},
                {'text': 'Виводить повідомлення', 'correct': False},
            ]
        },
    },
    {
        'text': 'Цикл — це конструкція, що повторює блок коду кілька разів.',
        'question_type': 'true_false',
        'data': {'correct': True},
    },
    {
        'text': 'Що таке функція?',
        'question_type': 'single_choice',
        'data': {
            'options': [
                {'text': 'Змінна для зберігання тексту', 'correct': False},
                {'text': 'Блок коду, який можна викликати по імені', 'correct': True},
                {'text': 'Коментар у коді', 'correct': False},
                {'text': 'Назва файлу', 'correct': False},
            ]
        },
    },
    {
        'text': 'Оператор присвоєння зберігає значення справа в змінну зліва (наприклад: x = 5).',
        'question_type': 'true_false',
        'data': {'correct': True},
    },
    {
        'text': 'Який тип даних зазвичай використовують для цілих чисел?',
        'question_type': 'single_choice',
        'data': {
            'options': [
                {'text': 'string (рядок)', 'correct': False},
                {'text': 'integer (ціле число)', 'correct': True},
                {'text': 'boolean', 'correct': False},
                {'text': 'array', 'correct': False},
            ]
        },
    },
    {
        'text': 'Коментар у коді виконується комп\'ютером як звичайна команда.',
        'question_type': 'true_false',
        'data': {'correct': False},
    },
    {
        'text': 'Що таке масив (список)?',
        'question_type': 'single_choice',
        'data': {
            'options': [
                {'text': 'Одна змінна з одним значенням', 'correct': False},
                {'text': 'Впорядкований набір елементів', 'correct': True},
                {'text': 'Умова в програмі', 'correct': False},
                {'text': 'Назва циклу', 'correct': False},
            ]
        },
    },
    {
        'text': 'return у функції повертає значення і може завершувати її виконання.',
        'question_type': 'true_false',
        'data': {'correct': True},
    },
]

# Додаткові питання для Python
PLACEMENT_QUESTIONS_PYTHON = [
    {
        'text': 'Яка функція в Python виводить текст на екран?',
        'question_type': 'single_choice',
        'data': {
            'options': [
                {'text': 'echo()', 'correct': False},
                {'text': 'print()', 'correct': True},
                {'text': 'write()', 'correct': False},
                {'text': 'output()', 'correct': False},
            ]
        },
    },
    {
        'text': 'У Python блоки коду позначаються відступами (пробілами), а не фігурними дужками.',
        'question_type': 'true_false',
        'data': {'correct': True},
    },
    {
        'text': 'Як оголосити функцію в Python?',
        'question_type': 'single_choice',
        'data': {
            'options': [
                {'text': 'function my_func():', 'correct': False},
                {'text': 'def my_func():', 'correct': True},
                {'text': 'func my_func():', 'correct': False},
                {'text': 'define my_func():', 'correct': False},
            ]
        },
    },
]

# Додаткові питання для JavaScript
PLACEMENT_QUESTIONS_JAVASCRIPT = [
    {
        'text': 'Як вивести повідомлення в консоль браузера в JavaScript?',
        'question_type': 'single_choice',
        'data': {
            'options': [
                {'text': 'print()', 'correct': False},
                {'text': 'console.log()', 'correct': True},
                {'text': 'echo()', 'correct': False},
                {'text': 'write()', 'correct': False},
            ]
        },
    },
    {
        'text': 'Ключові слова let та const використовують для оголошення змінних у сучасному JavaScript.',
        'question_type': 'true_false',
        'data': {'correct': True},
    },
    {
        'text': 'Як оголосити функцію в JavaScript?',
        'question_type': 'single_choice',
        'data': {
            'options': [
                {'text': 'def myFunc() {}', 'correct': False},
                {'text': 'function myFunc() {}', 'correct': True},
                {'text': 'func myFunc() {}', 'correct': False},
                {'text': 'fn myFunc() {}', 'correct': False},
            ]
        },
    },
]


def get_questions_for_language(language):
    """Повертає список питань для вступного тесту залежно від мови курсу."""
    questions = list(PLACEMENT_QUESTIONS_COMMON)
    if language == 'python':
        questions.extend(PLACEMENT_QUESTIONS_PYTHON)
    else:
        questions.extend(PLACEMENT_QUESTIONS_JAVASCRIPT)
    return questions


class Command(BaseCommand):
    help = 'Створює вступний тест (визначення рівня) для кожного опублікованого курсу.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перестворити тест, якщо він вже існує (старі питання видаляються).',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        courses = Course.objects.filter(is_published=True).order_by('order')
        if not courses.exists():
            self.stdout.write(self.style.WARNING('Немає опублікованих курсів. Спочатку запустіть load_sample_data.'))
            return

        created = 0
        updated = 0
        for course in courses:
            placement = course.quizzes.filter(is_placement=True).first()
            if placement and not force:
                self.stdout.write(f'Курс "{course.title}" вже має вступний тест (пропуск).')
                continue

            if placement and force:
                placement.questions.all().delete()
                quiz = placement
                updated += 1
            else:
                quiz = Quiz.objects.create(
                    course=course,
                    lesson=None,
                    title='Вступний тест — визначення рівня',
                    quiz_type='single_choice',
                    is_practice=False,
                    is_placement=True,
                    order=0,
                    is_published=True,
                )
                created += 1

            questions_data = get_questions_for_language(course.language)
            for i, q_data in enumerate(questions_data):
                Question.objects.create(
                    quiz=quiz,
                    text=q_data['text'],
                    question_type=q_data.get('question_type', 'single_choice'),
                    order=i,
                    data=q_data.get('data', {}),
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Курс "{course.title}": вступний тест створено/оновлено, {len(questions_data)} питань.'
                )
            )

        if created or updated:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Готово. Створено тестів: {created}, оновлено: {updated}.'
                )
            )
        else:
            self.stdout.write('Нічого не змінено (усі курси вже мають тест). Використайте --force для перезапису.')

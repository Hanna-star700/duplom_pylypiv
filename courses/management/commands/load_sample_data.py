# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from courses.models import Course, Lesson, Exercise


def html(s):
    return s.strip()


class Command(BaseCommand):
    help = 'Load sample Python and JavaScript courses with lessons and exercises. Use --reset to replace existing data.'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Delete existing courses and reload')

    def handle(self, *args, **options):
        if options.get('reset'):
            Course.objects.all().delete()
        elif Course.objects.exists():
            self.stdout.write('Courses already exist. Use --reset to replace.')
            return

        # ——— Python ———
        py = Course.objects.create(
            title='Python 3 — основи',
            slug='python-basics',
            language='python',
            short_description='Від змінних до функцій та списків. Пиши код у браузері та бач результат миттєво.',
            description='Повноцінний курс для початківців: синтаксис, типи даних, умови, цикли, функції та списки. Кожен урок супроводжується завданнями з запуском коду прямо на сторінці.',
            duration_hours=24,
            level='Початковий',
            order=0,
            icon='🐍',
            color='#3776ab',
        )

        l1 = Lesson.objects.create(
            course=py,
            title='Перша програма та змінні',
            slug='first-program',
            content=html('''
<h2>Що таке Python?</h2>
<p>Python — одна з найпопулярніших мов програмування. Вона має простий синтаксис, тому її легко читати та писати. Python використовують у веб-розробці, аналізі даних, машинному навчанні та автоматизації.</p>

<h2>Перша програма</h2>
<p>Класична перша програма виводить привітання. У Python для цього використовується функція <code>print()</code>:</p>
<pre><code>print("Hello, World!")</code></pre>

<h2>Змінні</h2>
<p>Змінні зберігають дані. Тип даних оголошувати не потрібно — Python визначає його автоматично.</p>
<pre><code>name = "LearnCode"
year = 2026
print(name, year)</code></pre>
<p>У завданні справа спробуй вивести своє ім'я.</p>
            '''),
            order=0,
            duration_minutes=15,
        )
        Exercise.objects.create(
            lesson=l1,
            title='Виведи своє ім\'я',
            instruction='Напиши програму, яка виводить твоє ім\'я за допомогою print(). Наприклад: print("Анна").',
            starter_code='print("")',
            hint='Використай print("Твоє ім\'я") — замість лапок можна використати апостроф.',
            order=0,
        )

        l2 = Lesson.objects.create(
            course=py,
            title='Числа та операції',
            slug='numbers',
            content=html('''
<h2>Цілі та дробові числа</h2>
<p>У Python є типи <code>int</code> (цілі числа) та <code>float</code> (дробові):</p>
<pre><code>a = 10
b = 3.14
print(a + b)</code></pre>

<h2>Оператори</h2>
<ul>
<li><code>+</code> <code>-</code> <code>*</code> <code>/</code> — додавання, віднімання, множення, ділення</li>
<li><code>//</code> — цілочисельне ділення</li>
<li><code>%</code> — остача від ділення</li>
<li><code>**</code> — піднесення до степеня</li>
</ul>
<pre><code>print(2 ** 10)   # 1024</code></pre>
            '''),
            order=1,
            duration_minutes=18,
        )
        Exercise.objects.create(
            lesson=l2,
            title='Обчисли вираз',
            instruction='Обчисли 2 у степені 10 і виведи результат за допомогою print().',
            starter_code='# 2 ** 10 = ?\nprint()',
            hint='Використай print(2 ** 10)',
            order=0,
        )

        l3 = Lesson.objects.create(
            course=py,
            title='Умови: if та else',
            slug='conditions',
            content=html('''
<h2>Умовний оператор if</h2>
<p>Код всередині блоку <code>if</code> виконується лише коли умова істинна:</p>
<pre><code>age = 18
if age >= 18:
    print("Повнолітній")</code></pre>
<p>Зверни увагу на відступи — у Python вони визначають блок коду.</p>

<h2>else та elif</h2>
<pre><code>x = 5
if x > 10:
    print("більше 10")
elif x > 0:
    print("додатнє")
else:
    print("менше або 0")</code></pre>
            '''),
            order=2,
            duration_minutes=20,
        )
        Exercise.objects.create(
            lesson=l3,
            title='Перевірка числа',
            instruction='Змінна n вже задана. Якщо n парне (ділиться на 2 без остачі), виведи "парне", інакше — "непарне". Використай if та else.',
            starter_code='n = 7\n# if n % 2 == 0: ... else: ...\nprint()',
            hint='Перевір n % 2 == 0 для парності.',
            order=0,
        )

        l4 = Lesson.objects.create(
            course=py,
            title='Цикли: for та while',
            slug='loops',
            content=html('''
<h2>Цикл for</h2>
<p>Повторити дію для кожного елемента послідовності:</p>
<pre><code>for i in range(5):
    print(i)   # 0, 1, 2, 3, 4</code></pre>

<h2>range</h2>
<p><code>range(5)</code> — числа від 0 до 4. <code>range(1, 6)</code> — від 1 до 5.</p>

<h2>Цикл while</h2>
<pre><code>count = 0
while count < 3:
    print(count)
    count += 1</code></pre>
            '''),
            order=3,
            duration_minutes=22,
        )
        Exercise.objects.create(
            lesson=l4,
            title='Сума від 1 до 10',
            instruction='Обчисли суму чисел від 1 до 10 (1+2+3+...+10) і виведи результат. Використай цикл for і змінну-накопичувач.',
            starter_code='total = 0\n# for i in range(1, 11): ...\nprint(total)',
            hint='for i in range(1, 11): total += i',
            order=0,
        )

        l5 = Lesson.objects.create(
            course=py,
            title='Функції',
            slug='functions',
            content=html('''
<h2>Оголошення функції</h2>
<p>Функція — це блок коду, який можна викликати по імені:</p>
<pre><code>def greet(name):
    return "Hello, " + name

print(greet("World"))</code></pre>

<h2>return</h2>
<p><code>return</code> повертає значення і завершує виконання функції. Якщо нічого не повертати, функція поверне <code>None</code>.</p>
            '''),
            order=4,
            duration_minutes=25,
        )
        Exercise.objects.create(
            lesson=l5,
            title='Функція суми двох чисел',
            instruction='Напиши функцію sum_two(a, b), яка повертає суму двох чисел. Потім виведи результат виклику sum_two(3, 7).',
            starter_code='def sum_two(a, b):\n    # return ...\n    pass\n\nprint(sum_two(3, 7))',
            hint='return a + b',
            order=0,
        )

        # ——— JavaScript ———
        js = Course.objects.create(
            title='JavaScript — основи',
            slug='javascript-basics',
            language='javascript',
            short_description='Змінні, функції, масиви та умови. Готовність до веб-розробки та інтерактивних сторінок.',
            description='Курс для тих, хто хоче писати інтерактивні сайти та розуміти фронтенд. Усі приклади та завдання виконуються прямо в браузері — результат виводиться під редактором.',
            duration_hours=20,
            level='Початковий',
            order=1,
            icon='🟨',
            color='#f7df1e',
        )

        j1 = Lesson.objects.create(
            course=js,
            title='Змінні та console.log',
            slug='variables-console',
            content=html('''
<h2>JavaScript у браузері</h2>
<p>JavaScript виконується в браузері. Для виводу інформації використовуй <code>console.log()</code>. На цій платформі результат з\'явиться у блоці «Результат виконання» під редактором.</p>

<h2>let та const</h2>
<p><code>let</code> — змінна, яку можна змінювати. <code>const</code> — константа (значення не змінюється).</p>
<pre><code>let name = "LearnCode";
const year = 2026;
console.log(name, year);</code></pre>
            '''),
            order=0,
            duration_minutes=15,
        )
        Exercise.objects.create(
            lesson=j1,
            title='Виведи привітання',
            instruction='Виведи в консоль рядок "Hello, JavaScript!" за допомогою console.log().',
            starter_code='console.log("");',
            hint='console.log("Hello, JavaScript!");',
            order=0,
        )

        j2 = Lesson.objects.create(
            course=js,
            title='Числа та оператори',
            slug='numbers',
            content=html('''
<h2>Арифметика</h2>
<p>JavaScript підтримує звичайні оператори: +, -, *, /, % (остача), ** (степінь).</p>
<pre><code>console.log(10 + 5);
console.log(2 ** 10);</code></pre>

<h2>Змінні з числами</h2>
<pre><code>let a = 20;
let b = 4;
console.log(a / b);</code></pre>
            '''),
            order=1,
            duration_minutes=15,
        )
        Exercise.objects.create(
            lesson=j2,
            title='Обчисли та виведи',
            instruction='Обчисли 100 поділити на 4 і виведи результат через console.log().',
            starter_code='console.log();',
            hint='console.log(100 / 4);',
            order=0,
        )

        j3 = Lesson.objects.create(
            course=js,
            title='Умови: if та else',
            slug='conditions',
            content=html('''
<h2>if та else</h2>
<p>Блок коду всередині фігурних дужок виконується лише за умови:</p>
<pre><code>let age = 18;
if (age >= 18) {
  console.log("Повнолітній");
} else {
  console.log("Неповнолітній");
}</code></pre>

<h2>Оператори порівняння</h2>
<p>== (рівно), != (не рівно), &gt;=, &lt;=, &gt;, &lt;. Для суворого порівняння типів використовуй === та !==.</p>
            '''),
            order=2,
            duration_minutes=18,
        )
        Exercise.objects.create(
            lesson=j3,
            title='Максимум з двох',
            instruction='Є змінні a та b. Виведи через console.log більше з двох значень. Використай if/else.',
            starter_code='let a = 15;\nlet b = 22;\n// if (a > b) ... else ...\nconsole.log();',
            hint='if (a > b) console.log(a); else console.log(b);',
            order=0,
        )

        j4 = Lesson.objects.create(
            course=js,
            title='Масиви',
            slug='arrays',
            content=html('''
<h2>Створення масиву</h2>
<p>Масив — впорядкований набір елементів. Індекси з нуля.</p>
<pre><code>let fruits = ["apple", "banana", "orange"];
console.log(fruits[0]);   // "apple"
console.log(fruits.length);  // 3</code></pre>

<h2>Методи</h2>
<p><code>push()</code> — додати в кінець. <code>pop()</code> — прибрати останній. <code>join()</code> — зліпити в рядок.</p>
<pre><code>fruits.push("grape");
console.log(fruits.join(", "));</code></pre>
            '''),
            order=3,
            duration_minutes=20,
        )
        Exercise.objects.create(
            lesson=j4,
            title='Виведи перший і останній елемент',
            instruction='У масиву arr виведи перший елемент (індекс 0) та останній (індекс arr.length - 1).',
            starter_code='let arr = ["a", "b", "c", "d"];\nconsole.log();\nconsole.log();',
            hint='arr[0] та arr[arr.length - 1]',
            order=0,
        )

        j5 = Lesson.objects.create(
            course=js,
            title='Функції',
            slug='functions',
            content=html('''
<h2>Оголошення функції</h2>
<pre><code>function greet(name) {
  return "Hello, " + name;
}
console.log(greet("World"));</code></pre>

<h2>Стрілкова функція</h2>
<pre><code>const add = (a, b) => a + b;
console.log(add(2, 3));</code></pre>
<p>Функція повертає значення через <code>return</code>. Без return результат буде <code>undefined</code>.</p>
            '''),
            order=4,
            duration_minutes=22,
        )
        Exercise.objects.create(
            lesson=j5,
            title='Функція множення',
            instruction='Напиши функцію multiply(a, b), яка повертає добуток двох чисел. Виведи результат multiply(6, 7).',
            starter_code='function multiply(a, b) {\n  // return ...\n}\nconsole.log(multiply(6, 7));',
            hint='return a * b;',
            order=0,
        )

        self.stdout.write(self.style.SUCCESS(
            'Sample data loaded: Python (5 lessons) and JavaScript (5 lessons) with exercises.'
        ))

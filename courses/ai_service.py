# -*- coding: utf-8 -*-
"""
Сервіс AI для генерації завдань та перевірки коду (OpenAI API).
Для диплома: інтелектуальна система перевірки програмного коду.
"""
import os
import re
import json

def _get_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except ImportError:
        return None


# Модель: дешева, достатня для оцінки (кілька центів за перевірку)
AI_MODEL = "gpt-4o-mini"


def generate_task(topic, language="Python"):
    """
    Генерує завдання для студента по темі уроку.
    topic: назва теми (наприклад "Цикли в Python")
    """
    client = _get_client()
    if not client:
        return None

    prompt = f"""
Create a simple programming task for a student.
Topic: {topic}
Language: {language}

Requirements:
- Beginner level
- Short description (2-4 sentences)
- One task only
- Output in Ukrainian language.
"""
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


def check_student_code(topic, task, student_code, language="Python"):
    """
    Перевіряє код студента: оцінка 1–10, помилки, що добре, поради.
    Повертає текст з полями: Score, Errors, Good, Advice.
    """
    client = _get_client()
    if not client:
        return None

    prompt = f"""
You are a programming teacher.

Topic: {topic}
Task: {task}
Language: {language}

Student code:
```
{student_code}
```

Evaluate the solution and respond STRICTLY in this format (in Ukrainian):

Score: X/10
Errors: ...
Good: ...
Advice: ...
"""
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


def parse_score_from_feedback(feedback_text):
    """
    Витягує оцінку 1–10 з тексту відповіді AI (для збереження в БД).
    Підтримує формат "Оцінка: X/10" (укр.) та "Score: X/10" (англ.).
    Повертає int від 1 до 10 або None.
    """
    if not feedback_text:
        return None
    match = re.search(r"(?:Оцінка|Score):\s*(\d+)/10", feedback_text, re.IGNORECASE)
    if match:
        score = int(match.group(1))
        return max(1, min(10, score))
    return None


def generate_placement_task(language="Python"):
    """
    Генерує завдання на 3 рівні для вступного тесту.
    Повертає dict: level1, level2, level3, full_task (або None якщо API недоступний).
    """
    client = _get_client()
    if not client:
        return None
    lang_name = "Python" if language == "python" else "JavaScript"
    prompt = f"""Створи одне програмістське завдання для вступного тесту з 3 рівнями складності. Мова: {lang_name}.

Формат відповіді СТРОГО українською, без зайвого тексту:

Рівень 1:
(коротке просте завдання — 1-2 речення)

Рівень 2:
(та сама тема, але з додатковими умовами або обмеженнями — 2-3 речення)

Рівень 3:
(складніша версія або відкрите завдання — 2-3 речення)

Завдання має бути для початківців, зрозуміле. Один блок завдання на всі 3 рівні."""
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=350,
        )
        text = response.choices[0].message.content.strip()
        parts = {"full_task": text, "level1": "", "level2": "", "level3": ""}
        for i, marker in enumerate(["Рівень 1:", "Рівень 2:", "Рівень 3:"], 1):
            key = "level%d" % i
            idx = text.find(marker)
            if idx >= 0:
                start = idx + len(marker)
                next_m = text.find("Рівень", start + 2)
                end = next_m if next_m > 0 else len(text)
                parts[key] = text[start:end].strip()
        if not parts["level1"]:
            parts["level1"] = text[:400]
        return parts
    except Exception:
        return None


def evaluate_placement_answer(full_task, user_code, language="Python"):
    """
    Перевіряє відповідь користувача на завдання вступного тесту.
    Повертає dict: feedback (пояснення), solution (приклад правильного коду), score (1-10).
    """
    client = _get_client()
    if not client:
        return None
    lang_name = "Python" if language == "python" else "JavaScript"
    prompt = f"""Ти — вчитель програмування. Завдання для студента (3 рівні):

{full_task}

Мова: {lang_name}

Код студента:
```
{user_code or '(нічого не написано)'}
```

Зроби:
1. Оціни рішення від 1 до 10 (враховуй навіть часткове виконання або спробу).
2. Коротко поясни українською: що добре, що можна покращити.
3. Напиши приклад ПРАВИЛЬНОГО повного розв'язку (код) для рівня 1 або 2.

Відповідь СТРОГО у форматі (українською):

Оцінка: X/10
Пояснення: ...
Правильний розв'язок:
```код
...
```"""
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        text = response.choices[0].message.content.strip()
        score = parse_score_from_feedback(text) or 5
        feedback = text
        solution = ""
        if "```" in text:
            code_match = re.search(r"```(?:код)?\s*([\s\S]*?)```", text)
            if code_match:
                solution = code_match.group(1).strip()
        return {"feedback": feedback, "solution": solution or "(див. пояснення вище)", "score": score}
    except Exception:
        return None


def generate_lesson_content(lesson_title, language="python"):
    """
    Генерує конспект уроку двома викликами API: спочатку перша половина,
    потім продовження. Так отримуємо справді довгий конспект (багато тексту та прикладів).
    Повертає HTML-рядок (безпечні теги: p, h2, h3, ul, ol, li, pre, code, strong).
    """
    client = _get_client()
    if not client:
        return None
    lang_name = "Python" if language == "python" else "JavaScript"
    system_msg = "Ти автор навчальних конспектів. Пиши ТІЛЬКИ українською. Використовуй тільки безпечні HTML-теги: <h2>, <h3>, <p>, <ul>, <ol>, <li>, <pre>, <code>, <strong>. Конспект має бути ДУЖЕ ДОВГИМ — мінімум 1500 слів загалом, багато абзаців і прикладів коду. Не скорочуй."

    # Частина 1: вступ + перші 4–5 розділів з прикладами (~500+ слів)
    prompt1 = f"""Напиши ПЕРШУ ЧАСТИНУ навчального конспекту уроку (українською).

Тема: {lesson_title}
Мова: {lang_name}

Вимоги до цієї частини:
- ОБОВ'ЯЗКОВО: обсяг цієї частини не менше 500 слів. Короткі 2–3 абзаци — неприйнятно; конспект усього уроку має бути не менше 1500 слів.
- Вступ (2–3 абзаци): про що урок, навіщо це потрібно.
- Мінімум 4 розділи з підзаголовками <h2> або <h3>. У кожному розділі — 2–4 абзаци пояснень і мінімум 1 приклад коду в <pre><code>...</code></pre> з коментарями.
- Загалом у цій частині мінімум 4 приклади коду та багато тексту. Пиши розгорнуто, не в стислому вигляді. Не скорочуй.
- Тільки теги: <h2>, <h3>, <p>, <ul>, <ol>, <li>, <pre>, <code>, <strong>.

Почни одразу з контенту (без зайвих фраз типу "Ось конспект")."""

    try:
        r1 = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt1},
            ],
            max_tokens=6144,
        )
        part1 = (r1.choices[0].message.content or "").strip()
        if not part1:
            return None
    except Exception:
        return None

    # Частина 2: продовження — ще 4+ розділів і приклади
    prompt2 = f"""Ось перша частина конспекту уроку (тема: {lesson_title}, мова: {lang_name}):

---
{part1[-6000:]}
---

Допиши ДРУГУ ЧАСТИНУ того самого конспекту українською. Вимоги:
- Обсяг цієї частини: мінімум 500 слів (разом з першою частиною конспект має бути не менше 1500 слів).
- Мінімум 4 нові розділи з підзаголовками <h2> або <h3> (наприклад: ще приклади, типові помилки, поради, підсумок, вправи).
- У кожному розділі кілька абзаців і мінімум 1 приклад коду в <pre><code>...</code></pre>. Загалом додай ще мінімум 4 приклади коду.
- Стиль і мову продовжуй так само. Тільки безпечні теги: <h2>, <h3>, <p>, <ul>, <ol>, <li>, <pre>, <code>, <strong>.
- Пиши багато тексту, не скорочуй. Починай одразу з наступного розділу (без фраз на кшталт "Ось друга частина")."""

    try:
        r2 = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt2},
            ],
            max_tokens=6144,
        )
        part2 = (r2.choices[0].message.content or "").strip()
    except Exception:
        part2 = ""

    combined = part1 + "\n\n" + part2 if part2 else part1

    # Частина 3: ще 2–3 розділи для максимального обсягу
    prompt3 = f"""Ось дві частини конспекту уроку (тема: {lesson_title}, мова: {lang_name}):

---
{combined[-5000:]}
---

Допиши ТРЕТЮ частину того самого конспекту українською: ще 2–3 розділи (наприклад додаткові приклади коду, підсумкова таблиця, типові питання та відповіді, поради для практики). Обсяг цієї частини: мінімум 500 слів, щоб загальний конспект був не менше 1500 слів. Кожен розділ — підзаголовок <h2> або <h3>, кілька абзаців, приклади в <pre><code>...</code></pre>. Тільки безпечні теги. Пиши багато. Починай одразу з наступного розділу."""

    try:
        r3 = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt3},
            ],
            max_tokens=4096,
        )
        part3 = (r3.choices[0].message.content or "").strip()
    except Exception:
        part3 = ""

    if part3:
        combined = combined + "\n\n" + part3

    # Перевірка обсягу: якщо менше 1500 слів — доповнити ще одним викликом
    def _word_count(html_text):
        if not html_text:
            return 0
        clean = re.sub(r"<[^>]+>", " ", html_text)
        return len(clean.split())

    if _word_count(combined) < 1500:
        prompt4 = f"""Ось поточний конспект уроку (тема: {lesson_title}, мова: {lang_name}). Він занадто короткий.

---
{combined[-5000:]}
---

Допиши ще одну частину того самого конспекту українською: 2–3 нові розділи з підзаголовками <h2>/<h3>, багато абзаців і прикладів коду в <pre><code>...</code></pre>. Загальний обсяг конспекту має становити мінімум 1500 слів — тому ця частина має бути розгорнутою (не менше 400–500 слів). Тільки теги: <h2>, <h3>, <p>, <ul>, <ol>, <li>, <pre>, <code>, <strong>. Починай одразу з наступного розділу."""
        try:
            r4 = client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt4},
                ],
                max_tokens=3072,
            )
            part4 = (r4.choices[0].message.content or "").strip()
            if part4:
                combined = combined + "\n\n" + part4
        except Exception:
            pass

    return combined


def podcast_reply(lesson_title, lesson_content, history, user_message, language="python"):
    """
    Відповідь ШІ в режимі подкасту: ставить питання по темі уроку, перевіряє відповідь користувача,
    каже що правильно/неправильно, ставить наступне питання.
    history: list of {role: 'user'|'assistant', content: str}
    Повертає текст відповіді асистента.
    """
    client = _get_client()
    if not client:
        return None
    lang_name = "Python" if language == "python" else "JavaScript"
    context = f"Урок: {lesson_title}\nМова: {lang_name}\n\nКороткий зміст уроку (для контексту):\n{(lesson_content or '')[:2000]}"
    first_turn = not history and user_message.lower().strip() in (
        'почнемо', 'так', 'готовий', 'привіт', 'start', 'hi', 'да'
    )
    system = """Ти — репетитор з програмування. Твоя роль у режимі «подкаст»:
1. Став короткі питання по темі уроку (що таке змінна, як працює цикл тощо).
2. Коли учень відповідає — оціни: що правильно, що ні; коротко поясни якщо потрібно.
3. Потім постав наступне питання по темі уроку.
Відповідай завжди українською, коротко (2–5 речень), дружньо. Не пиши код у відповіді, якщо не просять."""
    if first_turn:
        system += "\n\nЗараз учень тільки почав. Постав йому ПЕРШЕ питання по темі уроку (без оцінки відповіді)."
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": context},
    ]
    for h in (history or [])[-10:]:
        messages.append({"role": h.get("role", "user"), "content": (h.get("content") or "")[:2000]})
    messages.append({"role": "user", "content": user_message[:1500]})
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=messages,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


def generate_quiz_questions(lesson_title, lesson_content, question_type, num_questions=5, language="python"):
    """
    Генерує питання для тесту по темі уроку.
    question_type: 'true_false' | 'single_choice' | 'match_pairs'
    Повертає list питань у структурованому вигляді для фронту.
    """
    client = _get_client()
    if not client:
        return None
    lang_name = "Python" if language == "python" else "JavaScript"
    context = (lesson_content or "")[:2500]
    type_instructions = {
        "true_false": """Для кожного питання поверни об'єкт з полями "text" (текст питання) та "correct" (true або false).
Приклад: [{"text": "Змінна в Python оголошується через =", "correct": true}, ...]""",
        "single_choice": """Для кожного питання поверни об'єкт з полями "text" (текст питання), "options" (масив з 3-4 варіантів відповіді), "correct_index" (індекс правильної відповіді, з 0).
Приклад: [{"text": "Що виведе print(2+2)?", "options": ["3", "4", "5", "22"], "correct_index": 1}, ...]""",
        "match_pairs": """Поверни один об'єкт з полем "pairs" — масив пар [термін, визначення] для з'єднання (5-7 пар). Терміни та визначення українською.
Приклад: [{"pairs": [["змінна", "іменована комірка для значення"], ["цикл", "повторення блоку коду"], ...]}]""",
    }
    instr = type_instructions.get(question_type, type_instructions["true_false"])
    prompt = f"""Тема уроку: {lesson_title}
Мова програмування: {lang_name}
Короткий зміст уроку (контекст):
{context}

Згенеруй тест українською. Тип: {question_type}.
Кількість: {num_questions} питань для true_false/single_choice, або один блок з 5-7 парами для match_pairs.

{instr}

Поверни ТІЛЬКИ валідний JSON (масив об'єктів), без пояснь до або після."""
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
        )
        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```\s*$", "", raw)
        data = json.loads(raw)
        if question_type == "match_pairs" and isinstance(data, list) and data and "pairs" in data[0]:
            return data
        if question_type in ("true_false", "single_choice") and isinstance(data, list):
            return data[:num_questions]
        return None
    except (json.JSONDecodeError, TypeError, KeyError, IndexError):
        return None


def _count_correct_answers(questions, answers, question_type):
    """Підраховує правильні відповіді по questions та answers. Повертає (correct_count, total)."""
    if not questions or not isinstance(answers, (list, tuple)):
        return 0, len(questions) or 0
    correct = 0
    if question_type == "true_false":
        for i, q in enumerate(questions[: len(answers)]):
            if i >= len(answers):
                break
            want = q.get("correct")
            got = answers[i]
            if got is True or (isinstance(got, str) and got.lower() in ("true", "так", "1", "yes")):
                got = True
            elif got is False or (isinstance(got, str) and got.lower() in ("false", "ні", "0", "no")):
                got = False
            if want == got:
                correct += 1
        return correct, len(questions)
    if question_type == "single_choice":
        for i, q in enumerate(questions[: len(answers)]):
            if i >= len(answers):
                break
            want = q.get("correct_index", 0)
            try:
                got = int(answers[i]) if answers[i] is not None else -1
            except (TypeError, ValueError):
                got = -1
            if want == got:
                correct += 1
        return correct, len(questions)
    if question_type == "match_pairs":
        # questions = [{"pairs": [[l,r],[l,r],...]}]; answers = list of [left, right] for each pair
        total_pairs = 0
        for q in questions:
            pairs = q.get("pairs") or []
            total_pairs += len(pairs)
        if not questions:
            return 0, 0
        pairs = questions[0].get("pairs") or []
        correct_set = set()
        for p in pairs:
            if isinstance(p, (list, tuple)) and len(p) >= 2:
                correct_set.add((str(p[0]).strip(), str(p[1]).strip()))
            elif isinstance(p, dict):
                correct_set.add((str(p.get("left", "")).strip(), str(p.get("right", "")).strip()))
        user_pairs = []
        for a in answers:
            if isinstance(a, (list, tuple)) and len(a) >= 2:
                user_pairs.append((str(a[0]).strip(), str(a[1]).strip()))
            elif isinstance(a, dict):
                user_pairs.append((str(a.get("left", "")).strip(), str(a.get("right", "")).strip()))
        correct = sum(1 for p in user_pairs if p in correct_set)
        return correct, len(pairs)
    return 0, len(questions)


def evaluate_quiz_answers(lesson_title, questions, answers, question_type, language="python"):
    """
    Оцінює відповіді так само, як завдання від ШІ: оцінка 1–10 + пояснення.
    Повертає dict: correct_count, total, feedback, score (1–10).
    """
    correct_count, total = _count_correct_answers(questions, answers, question_type)
    client = _get_client()
    lang_name = "Python" if language == "python" else "JavaScript"
    percent = round(100 * correct_count / total, 0) if total else 0
    score_from_percent = max(1, min(10, (percent * 10) // 100)) if total else 5
    feedback = (
        f"Оцінка: {score_from_percent}/10\n"
        f"Пояснення: Учень відповів правильно на {correct_count} з {total} питань."
        + (" Чудово!" if correct_count >= total else " Варто повторити матеріал уроку.")
    )
    if client and total > 0:
        prompt = f"""Ти — вчитель програмування. Учень пройшов тест по темі уроку.

Тема уроку: {lesson_title}
Мова: {lang_name}

Результат: учень відповів правильно на {correct_count} з {total} питань ({percent}%).

Зроби:
1. Оціни результат від 1 до 10 (враховуй відсоток та зусилля; 10 — все правильно, 1 — майже нічого).
2. Коротко поясни українською: що добре, що варто повторити (1–3 речення). Без коду.

Відповідь СТРОГО у форматі (українською):

Оцінка: X/10
Пояснення: ..."""
        try:
            response = client.chat.completions.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )
            text = (response.choices[0].message.content or "").strip()
            if text:
                feedback = text
        except Exception:
            pass
    score = parse_score_from_feedback(feedback) or score_from_percent
    return {
        "correct_count": correct_count,
        "total": total,
        "feedback": feedback,
        "score": max(1, min(10, score)),
    }

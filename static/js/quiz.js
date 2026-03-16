(function () {
  'use strict';

  var form = document.getElementById('quiz-form');
  var submitBtn = document.getElementById('quiz-submit-btn');
  if (!form) return;

  function handleQuizSubmit(e) {
    if (e) e.preventDefault();
    var questions = form.querySelectorAll('.quiz-question');
    var answers = [];
    questions.forEach(function (block) {
      var qId = parseInt(block.getAttribute('data-question-id'), 10);
      var type = block.getAttribute('data-type');
      var answer = null;

      if (type === 'single_choice') {
        var r = block.querySelector('input[type="radio"]:checked');
        answer = r ? r.value : null;
      } else if (type === 'multiple_choice') {
        var checked = block.querySelectorAll('input[type="checkbox"]:checked');
        answer = Array.prototype.map.call(checked, function (c) { return c.value; });
      } else if (type === 'true_false') {
        var rf = block.querySelector('input[type="radio"]:checked');
        answer = rf ? rf.value : null;
      } else if (type === 'flashcard') {
        var inp = block.querySelector('input[type="text"]');
        answer = inp ? inp.value.trim() : '';
      } else if (type === 'match_pairs') {
        var rows = block.querySelectorAll('.quiz-match-row');
        answer = Array.prototype.map.call(rows, function (row) {
          var left = row.getAttribute('data-left') || row.querySelector('.quiz-match-left').textContent;
          var sel = row.querySelector('select');
          var right = sel ? sel.value : '';
          return [left, right];
        });
      } else if (type === 'ordering') {
        var orderList = block.querySelector('.quiz-order-list');
        var items = orderList ? orderList.querySelectorAll('.quiz-order-item');
        answer = Array.prototype.map.call(items, function (item) {
          var v = item.getAttribute('data-value');
          if (v) return v;
          var inp = item.querySelector('input');
          return inp ? inp.value : '';
        });
      } else if (type === 'fill_blank') {
        var inputs = block.querySelectorAll('.quiz-fill-inputs input');
        answer = Array.prototype.map.call(inputs, function (i) { return i.value.trim(); });
      }

      answers.push({ question_id: qId, answer: answer });
    });

    var btn = submitBtn || form.querySelector('button[type="button"]#quiz-submit-btn') || form.querySelector('button[type="submit"]');
    if (btn) { btn.disabled = true; btn.textContent = 'Перевірка...'; }

    var xhr = new XMLHttpRequest();
    var quizId = typeof window.QUIZ_ID !== 'undefined' ? window.QUIZ_ID : null;
    if (!quizId) {
      if (btn) { btn.disabled = false; btn.textContent = 'Перевірити відповіді'; }
      alert('Помилка: не визначено тест. Оновіть сторінку.');
      return;
    }
    var csrfToken = window.CSRF_TOKEN || (document.getElementById('csrf-token') && document.getElementById('csrf-token').value) || (form.querySelector('input[name=csrfmiddlewaretoken]') && form.querySelector('input[name=csrfmiddlewaretoken]').value);
    xhr.open('POST', '/quiz/' + quizId + '/submit/');
    xhr.setRequestHeader('Content-Type', 'application/json');
    if (csrfToken) xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.onload = function () {
      if (btn) { btn.disabled = false; btn.textContent = 'Перевірити відповіді'; }
      if (xhr.status !== 200) {
        alert('Помилка сервера (' + xhr.status + '). Перевірте, що ви увійшли в обліковий запис, та спробуйте знову.');
        return;
      }
      var res;
      try {
        res = JSON.parse(xhr.responseText || '{}');
      } catch (err) {
        alert('Помилка відповіді. Спробуйте оновити сторінку та пройти тест знову.');
        return;
      }
      if (res.already_passed && res.redirect_url) {
        if (res.message) alert(res.message);
        window.location.href = res.redirect_url;
        return;
      }
      if (res.ok) {
        if (res.redirect_url) {
          form.style.display = 'none';
          var resultEl = document.getElementById('quiz-result');
          var textEl = document.getElementById('quiz-result-text');
          var placementResult = res.placement_result || {};
          var correct = res.correct != null ? res.correct : res.score;
          var total = res.total != null ? res.total : res.max_score;
          var percent = res.percent != null ? res.percent : (total ? Math.round(100 * correct / total) : 0);
          var msg = 'Результат вступного тесту: ' + correct + ' з ' + total + ' правильних (' + percent + '%).\n\n';
          msg += 'Визначено ваш рівень: ' + (placementResult.level || '') + '.\n\n';
          msg += (placementResult.start_lesson_text || ('Рекомендований старт: урок ' + (placementResult.lesson_num || '') + ' — «' + (placementResult.lesson_title || '') + '».')) + '\n\n';
          if (res.points_added != null && res.points_added > 0) {
            msg += 'Нараховано балів: +' + res.points_added + ' (за відповіді та проходження вступного тесту).';
          }
          msg += '\n\nЗа кілька секунд перейдемо до уроку, або натисніть кнопку нижче.';
          if (resultEl && textEl) {
            textEl.innerHTML = msg.replace(/\n/g, '<br>');
            resultEl.style.display = 'block';
            resultEl.classList.add('quiz-result-visible');
            if (resultEl.scrollIntoView) resultEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
          var gotoBtn = document.getElementById('quiz-result-goto-lesson');
          if (gotoBtn && res.redirect_url) {
            gotoBtn.href = res.redirect_url;
            gotoBtn.style.display = 'inline-flex';
          }
          setTimeout(function () { window.location.href = res.redirect_url; }, 4000);
          return;
        }
        form.style.display = 'none';
        var resultEl = document.getElementById('quiz-result');
        var textEl = document.getElementById('quiz-result-text');
        if (resultEl && textEl) {
          var correct = res.correct != null ? res.correct : res.score;
          var total = res.total != null ? res.total : res.max_score;
          var percent = res.percent != null ? res.percent : (total ? Math.round(100 * correct / total) : 0);
          var msg = 'Правильних відповідей: ' + correct + ' з ' + total + ' (' + percent + '%)';
          if (!window.QUIZ_IS_PRACTICE && res.points_added != null && res.points_added > 0) {
            msg += '. Нараховано балів: +' + res.points_added;
          } else if (window.QUIZ_IS_PRACTICE) {
            msg = 'Тренувальний режим. ' + msg + '. Бали не нараховуються.';
          }
          textEl.textContent = msg;
          resultEl.style.display = 'block';
          resultEl.classList.remove('quiz-result-high');
          if (percent >= 80) resultEl.classList.add('quiz-result-high');
          var achievementEl = document.getElementById('quiz-result-achievement');
          if (achievementEl) {
            var iconEl = document.getElementById('quiz-result-achievement-icon');
            var titleEl = document.getElementById('quiz-result-achievement-title');
            var descEl = document.getElementById('quiz-result-achievement-desc');
            var icon = '😅';
            var title = 'Наступного разу буде краще!';
            var desc = 'Практика робить майстра.';
            if (percent >= 80) {
              icon = '🏆';
              title = '«Легенда тестів»';
              desc = 'Ідеальний або майже ідеальний результат — як у Ворлд оф Тенкс!';
            } else if (percent >= 60) {
              icon = '🔥';
              title = '«Майже топ»';
              desc = 'Добре пройдено. Ще трохи — і буде максимум.';
            } else if (percent >= 40) {
              icon = '💪';
              title = '«Середнячок»';
              desc = 'Є куди рости, але основа вже є.';
            } else if (percent >= 20) {
              icon = '🐢';
              title = '«Помалу вперед»';
              desc = 'Практика робить майстра.';
            }
            if (iconEl) iconEl.textContent = icon;
            if (titleEl) titleEl.textContent = title;
            if (descEl) descEl.textContent = desc;
            achievementEl.style.display = 'flex';
          }
          requestAnimationFrame(function () {
            resultEl.classList.add('quiz-result-visible');
          });
        }
      } else {
        alert(res.message || 'Щось пішло не так. Спробуйте ще раз.');
      }
    };
    xhr.onerror = function () {
      if (btn) { btn.disabled = false; btn.textContent = 'Перевірити відповіді'; }
      alert('Помилка мережі.');
    };
    xhr.send(JSON.stringify({ answers: answers }));
  }

  if (submitBtn) {
    submitBtn.addEventListener('click', handleQuizSubmit);
  } else {
    form.addEventListener('submit', function (e) { e.preventDefault(); handleQuizSubmit(e); });
  }
})();

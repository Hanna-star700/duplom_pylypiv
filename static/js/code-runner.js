/**
 * LearnCode — запуск коду в браузері: JavaScript та Python (Pyodide)
 */

(function () {
  'use strict';

  var pyodidePromise = null;

  function getPyodide() {
    if (typeof loadPyodide === 'undefined') return Promise.resolve(null);
    if (!pyodidePromise) {
      pyodidePromise = loadPyodide({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'
      });
    }
    return pyodidePromise;
  }

  function runJavaScript(code, outputEl) {
    var logs = [];
    var originalLog = console.log;
    console.log = function () {
      var args = Array.prototype.slice.call(arguments);
      logs.push(args.map(function (x) {
        if (typeof x === 'object' && x !== null) return JSON.stringify(x, null, 2);
        return String(x);
      }).join(' '));
    };
    try {
      var fn = new Function(code);
      fn();
      outputEl.textContent = logs.length ? logs.join('\n') : '(немає виводу — використай console.log(...))';
      outputEl.classList.remove('error');
    } catch (e) {
      outputEl.textContent = 'Помилка: ' + e.message;
      outputEl.classList.add('error');
    } finally {
      console.log = originalLog;
    }
  }

  function runPython(code, outputEl, doneCallback) {
    outputEl.textContent = 'Завантаження Python (Pyodide)...';
    outputEl.classList.remove('error');
    getPyodide().then(function (pyodide) {
      if (!pyodide) {
        outputEl.textContent = 'Python не завантажився. Переконайся: 1) відкриваєш сайт через http://127.0.0.1:8000 (не file://); 2) сервер запущений (python manage.py runserver); 3) є інтернет.';
        outputEl.classList.add('error');
        if (doneCallback) doneCallback();
        return;
      }
      outputEl.textContent = 'Виконання...';
      pyodide.runPython('import io, sys; sys.stdout = io.StringIO()');
      pyodide.runPythonAsync(code).then(function () {
        try {
          var out = pyodide.runPython('sys.stdout.getvalue()');
          outputEl.textContent = out != null && String(out).trim() ? String(out).trim() : '(немає виводу — використай print())';
          outputEl.classList.remove('error');
        } catch (err) {
          outputEl.textContent = 'Помилка: ' + (err.message || String(err));
          outputEl.classList.add('error');
        }
        if (doneCallback) doneCallback();
      }).catch(function (e) {
        outputEl.textContent = 'Помилка: ' + (e.message || String(e));
        outputEl.classList.add('error');
        if (doneCallback) doneCallback();
      });
    }).catch(function (e) {
      outputEl.textContent = 'Не вдалося завантажити Python. Відкривай сайт через http://127.0.0.1:8000 і перевір інтернет.';
      outputEl.classList.add('error');
      if (doneCallback) doneCallback();
    });
  }

  document.querySelectorAll('[data-run]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.getAttribute('data-exercise-id');
      var textarea = document.getElementById('code-' + id);
      var outputEl = document.getElementById('output-' + id);
      if (!textarea || !outputEl) return;
      var code = textarea.value.trim();
      var lang = textarea.getAttribute('data-lang');
      outputEl.removeAttribute('data-placeholder');
      outputEl.textContent = '';
      outputEl.classList.remove('error');
      var label = btn.textContent;
      btn.textContent = 'Виконання...';
      btn.disabled = true;
      function done() {
        btn.textContent = label;
        btn.disabled = false;
      }
      if (lang === 'javascript') {
        runJavaScript(code, outputEl);
        done();
      } else {
        runPython(code, outputEl, done);
      }
    });
  });
})();

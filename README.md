# qa-automation-template
Шаблон для автотестов на Python, готовый к CI/CD
## Запуск
1. **Клонируйте репозиторий** на ваш локальный компьютер:
    Используйте команду в терминале:
```sh
git@github.com:mish-design/aqa-template.git
```
2. **Далее на локальном компьютере нужно создать виртуальное окружение**
```sh
python3 -m venv .venv
```
**Активация виртуального окружения**:

- **macOS/Linux**:
    
```jsx
source .venv/bin/activate
```
    
- **Windows**:
```jsx
.venv\Scripts\activate
```
3. **Установить зависимости в файле с**

```jsx
pip install -r requirements.txt
```

Для данного проекта будем использовать эти requirements (возможно будет изменены версии)

4.  **Базовый запуск:**

```sh
pytest tests/
 ```   


**Использованеи файла Conftest:**

Выбрать фаил для тестов на  playwright или Selenium, переименовать в conftest.py

## Описание файлов и папок прокта
- README.md — описание нашего проекта, как работать как запускать тесты
- conftest.py — позволяет управлять фикстурами, браузерами
- .gitignore — в нем указываются файлы и каталоги, которые Git будет игнорировать при пуше в master. Это поможет не засорять наш проект временными и ненужными файлами.
- pytest.ini — конфигурационный файл для определения пользовательских маркеров и интеграции с плагинами и расширениями. (При помощи маркеров удобно разделять автотесты, например, на smoke и регрессионные — в зависимости от ситуации прогоняться будут нужные нам тесты).
- requirements.txt — это специальный текстовый файл, принятый в Python-сообществе как стандарт для хранения списка всех необходимых библиотек (зависимостей) и их версий.
т.е. все модули, которые должны быть установлены (например, pytest, playwright, requests и т.д.).
- tests/: здесь лежат файлы с тестами (например, test_login.py, test_registration.py и т.д.).
- pages/: если используете Page Object Model, здесь можно хранить классы-обёртки для ваших страниц (LoginPage, HomePage).

## Инструкция по настройке CI

Подробное описание процесса настройки CI доступно по ссылке:
[Настройка CI (базовая)](https://www.notion.so/mishdesign/CI-39242d3e2cac41b3b45ec13624362958)

Чтобы тесты запускались в GitHub Action используй один из фалов .yml в папке .github/workflows/

Если тесты на будут на GitLab, то .yml брать в корне проекта (там два под playwright и под Selenium)

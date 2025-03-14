
import pytest
import allure
from pages.base_page import BasePage

@allure.epic("Проект: Автотестирование сайта")
@allure.feature("UI Testing")
@allure.story("Взаимодействие с главной страницей")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
    Тест проверяет базовые функциональности:
    - Открытие главной страницы
    - Проверка заголовка страницы
    - Заполнение поля поиска и нажатие кнопки поиска
    - Ожидание появления результатов
    - Валидация текста результатов поиска
""")
@allure.link("https://example.com/testcase/123", name="Test Case Link")
@allure.issue("ISSUE-456", name="Связанный баг")
def test_home_page_interaction(page, base_url):
    """
    Пример теста с использованием расширенных Allure-тегов и принтами для каждого шага, убрать по необходимости.
    """
    base_page = BasePage(page, base_url)

    with allure.step("Открываем главную страницу"):
        base_page.open("/")  # Открываем базовый URL
        print("Базовая страница открыта по адресу:", base_url)

    with allure.step("Получаем заголовок страницы"):
        title = base_page.get_title()
        print("Заголовок страницы:", title)
        allure.attach(title, name="Page Title", attachment_type=allure.attachment_type.TEXT)
        assert "Example" in title, f"Заголовок '{title}' не содержит 'Example'"

    with allure.step("Заполняем поле поиска"):
        base_page.fill("#search", "Test Query")
        print("Поле поиска заполнено значением 'Test Query'")

    with allure.step("Нажимаем кнопку поиска"):
        base_page.click("#searchButton")
        print("Кнопка поиска нажата")

    with allure.step("Ожидаем появления результатов поиска"):
        base_page.wait_for_element_visible(".results", timeout=5000)
        print("Результаты поиска появились")

    with allure.step("Получаем текст результатов поиска"):
        results_text = base_page.get_text(".results")
        print("Текст результатов поиска:", results_text)
        allure.attach(results_text, name="Search Results", attachment_type=allure.attachment_type.TEXT)
        assert "Test Query" in results_text, "Результаты поиска не содержат 'Test Query'"

from playwright.sync_api import Page, TimeoutError

class BasePage:
    """
    Универсальная базовая страница для тестирования на Playwright.
    Предоставляет расширенный набор методов для работы со страницей.
    """
    def __init__(self, page: Page, base_url: str = None):
        self.page = page
        self.base_url = base_url

    def open(self, path: str = ""):
        """
        Открывает страницу по базовому URL с указанным путем.
        """
        url = f"{self.base_url}{path}" if self.base_url else path
        self.page.goto(url)

    def click(self, locator: str):
        """
        Кликает по элементу, найденному по CSS-селектору.
        """
        self.page.click(locator)

    def fill(self, locator: str, text: str):
        """
        Очищает и заполняет поле ввода указанным текстом.
        """
        self.page.fill(locator, text)

    def get_text(self, locator: str) -> str:
        """
        Возвращает внутренний текст элемента.
        """
        return self.page.inner_text(locator)

    def is_visible(self, locator: str) -> bool:
        """
        Проверяет, виден ли элемент.
        """
        return self.page.is_visible(locator)

    def get_title(self) -> str:
        """
        Возвращает заголовок страницы.
        """
        return self.page.title()

    def get_current_url(self) -> str:
        """
        Возвращает текущий URL страницы.
        """
        return self.page.url

    def wait_for_element_visible(self, locator: str, timeout: int = 5000):
        """
        Ожидает, что элемент станет видимым в течение указанного времени (в миллисекундах).
        """
        try:
            self.page.wait_for_selector(locator, state="visible", timeout=timeout)
        except TimeoutError:
            raise Exception(f"Элемент {locator} не стал видимым за {timeout} мс.")

    def get_attribute(self, locator: str, attribute: str) -> str:
        """
        Возвращает значение атрибута элемента.
        """
        element = self.page.query_selector(locator)
        if element:
            return element.get_attribute(attribute)
        raise Exception(f"Элемент {locator} не найден для получения атрибута {attribute}.")

    def double_click(self, locator: str):
        """
        Выполняет двойной клик по элементу.
        """
        self.page.dblclick(locator)

    def right_click(self, locator: str):
        """
        Выполняет клик правой кнопкой мыши по элементу.
        """
        self.page.click(locator, button="right")

    def hover(self, locator: str):
        """
        Наводит курсор на элемент.
        """
        self.page.hover(locator)

    def scroll_into_view(self, locator: str):
        """
        Прокручивает страницу до элемента.
        """
        element = self.page.query_selector(locator)
        if element:
            element.scroll_into_view_if_needed()
        else:
            raise Exception(f"Элемент {locator} не найден для прокрутки.")

    def select_option(self, locator: str, value: str):
        """
        Выбирает опцию в выпадающем списке по значению.
        """
        self.page.select_option(locator, value=value)

    def refresh(self):
        """
        Обновляет текущую страницу.
        """
        self.page.reload()

    def go_back(self):
        """
        Возвращается на предыдущую страницу.
        """
        self.page.go_back()

    def get_inner_html(self, locator: str) -> str:
        """
        Возвращает внутренний HTML элемента.
        """
        return self.page.inner_html(locator)

    def get_outer_html(self, locator: str) -> str:
        """
        Возвращает HTML элемента целиком.
        """
        element = self.page.query_selector(locator)
        if element:
            return element.evaluate("el => el.outerHTML")
        raise Exception(f"Элемент {locator} не найден для получения outerHTML.")

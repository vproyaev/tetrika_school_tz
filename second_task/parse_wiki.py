import json
import sys

import requests
from bs4 import BeautifulSoup, element

FIRST_PAGE_WITH_ANIMALS = (
    'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%'
    'D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE'
    '_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
)
PARSER = 'lxml'


class Wikipedia:

    def __init__(self) -> None:
        self._url: str = 'https://ru.wikipedia.org'
        self._next_page_str: str = 'Следующая страница'
        self._page_tag: str = 'div'
        self._tag_a: str = 'a'
        self._href: str = 'href'
        self._tag_li: str = 'li'
        self._title: str = 'title'

    def get_url(self) -> str:
        return self._url

    url = property(fget=get_url, fset=None, fdel=None)

    def get_next_page_str(self) -> str:
        return self._next_page_str

    next_page_str = property(fget=get_next_page_str, fset=None, fdel=None)

    def get_page_tag(self) -> str:
        return self._page_tag

    page_tag = property(fget=get_page_tag, fset=None, fdel=None)

    def get_tag_a(self) -> str:
        return self._tag_a

    tag_a = property(fget=get_tag_a, fset=None, fdel=None)

    def get_href(self) -> str:
        return self._href

    href = property(fget=get_href, fset=None, fdel=None)

    def get_tag_li(self) -> str:
        return self._tag_li

    tag_li = property(fget=get_tag_li, fset=None, fdel=None)

    def get_title(self) -> str:
        return self._title

    title = property(fget=get_title, fset=None, fdel=None)


class ParseAnimals(Wikipedia):

    def __init__(self) -> None:
        super(ParseAnimals, self).__init__()

        self.animal_tag_id: str = 'mw-pages'

        self._alphabetic_animals: dict[str: int] = {}

        self.start_page: str = FIRST_PAGE_WITH_ANIMALS
        self.next_page_url: None | str = None
        self.is_next_page: bool = True

        # Specially calculated, before complete.
        self.total_pages: int = 206
        self.page_number: int = 1

        self.parse_animals()

    def __str__(self) -> str:
        result = '\n'
        for letter, count in self._alphabetic_animals.items():
            result += f'{letter}: {count}\n'

        return result

    @property
    def parsed_page(self) -> element.Tag:
        if self.next_page_url is not None:
            url = self.url + self.next_page_url
            page = requests.get(self.url + self.next_page_url).text
        else:
            url = self.start_page
            page = requests.get(self.start_page).text

        soup = BeautifulSoup(page, PARSER)
        return soup.find(self.page_tag, id=self.animal_tag_id)

    @property
    def progress(self) -> int:
        return int(self.page_number / self.total_pages * 100)

    def parse_animals(self) -> None:
        sys.stdout.write(
            'Parsing the number of animals per letter has begun. Stand by!\n'
        )
        while self.is_next_page:
            self.add_animals_from_page()
            is_next_page = (
                self.parsed_page.find_all(self.tag_a)[-1].text
                == self.next_page_str
            )

            if is_next_page:
                self.next_page_url = (
                    self.parsed_page.find_all(self.tag_a)[-1].attrs.get(
                        self.href
                    )
                )
                self.page_number += 1
                sys.stdout.write(f'\rProgress: {self.progress}%')
                sys.stdout.flush()
            else:
                self.is_next_page = is_next_page

    def add_animals_from_page(self) -> None:
        animal_list = self.parsed_page.find_all(self.tag_li)
        for animal in animal_list:
            try:
                first_letter = animal.get_text(self.title)[0]
            except IndexError:
                raise Exception(
                    'Something went wrong, it is impossible to detect the '
                    'name of the animal. Try again.'
                )

            try:
                self._alphabetic_animals[first_letter] += 1
            except KeyError:
                self._alphabetic_animals[first_letter] = 1

    def get_json(self) -> str:
        sys.stdout.write('\n')
        return json.dumps(
            self._alphabetic_animals, indent=4, ensure_ascii=False
        )

# def _get_part_text(text: str, start: int, page_size: int):
#     znaki = list('!.?;:,')
#     try:
#         if text[page_size + start - 1] in znaki and text[page_size + start] != '.':
#             return [text[start: page_size + start], page_size]
#         else:
#             if text[start + page_size] == '.':
#                 res_txt = text[start: page_size + start-2]
#             else:
#                 res_txt = text[start: page_size + start]
#             yes_ind = [res_txt.rfind('!'), res_txt.rfind('.'),
#                        res_txt.rfind(','), res_txt.rfind(':'),
#                        res_txt.rfind(';'), res_txt.rfind('?')]
#             res_ind = []
#             for i in yes_ind:
#                 if i is not None:
#                     res_ind.append(i)
#             ind = max(res_ind)

#             return [res_txt[:ind + 1], ind + 1]
#     except IndexError:
#         num = len(text[start:])
#         return [text[start:], num]

import os
from pprint import pprint

BOOK_PATH = 'book/Bredberi_Marsianskie-hroniki.txt'


def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    end_simbol = ['.', ',', '!', ':', ';', '?']
    end = start+page_size
    while text[end:][:1] in end_simbol:
        end -= 1
    text = text[start:end]
    text = text[: max(map(text.rfind, end_simbol))+1]
    return text, len(text)



book: dict[int, str] = {}
PAGE_SIZE = 1050


def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as file:
      string: str = file.read()
    key: int = 1
    start = 0
    while start < len(string):
        txt, length = _get_part_text(string, start, PAGE_SIZE)
        book[key] = txt.lstrip(' \n')
        key += 1
        start += length


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(os.getcwd(), BOOK_PATH))
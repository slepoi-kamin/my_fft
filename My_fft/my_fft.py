from cmath import exp, pi
import pathlib
import inspect
import re


class TimeData:
    """
    Contains time dada and frequency analysis data.
    """

    def __init__(self, path: pathlib.Path):
        self.__set_text_data(path)
        self.__set_data()
        self._fft = None

    def __set_text_data(self, path: pathlib.Path):
        self.text_data = read_from_file(path)

    def __set_data(self):
        handled_data = handle_text_data(self.text_data)
        self.data = make_dict_from_data(handled_data)

    @property
    def fft(self):
        if self._fft is None:
            self._set_fft()
        return self.fft

    def _set_fft(self):
        self._fft = {key: calc_fft_recursively(self.data[key])
                     for key in self.data if key.lower != 'time'}


def make_dict_from_data(list_data):
    """
    Check if "time" is first column name. Transpose data and float it.
    :param list_data: list
    :return: dict
    """
    if is_columns_have_names(list_data):
        col_names = list_data[0]
        data = transpose_list(list_data[1:])
        return {col_names[i]: make_data_float(data[i]) for i in range(len(col_names))}
    else:
        raise ValueError(f'No column with name "test" at [0][0] position of data.\n'
                         f'{get_function_info()} \n'
                         f'Inputted data: {list_data}.')


def make_data_float(input_data):
    if isinstance(input_data, list):
        float_data = [make_data_float(elm) for elm in input_data]
    else:
        float_data = float(input_data)
    return float_data


def is_columns_have_names(data):
    if data[0][0].lower() == 'time':
        return True
    else:
        return False


def transpose_list(list_data):
    """
    Transpose list.
    :param list_data: list
    :return: list
    """
    return list(map(list, zip(*list_data)))


def read_from_file(path):
    """
    Read data from file.
    :param path: pathlib.Path
    :return: data
    """
    if is_type_is(path, pathlib.Path) and not path.exists():
        raise FileExistsError(f'File {path} not exists. \n'
                              f'{get_function_info()} \n')
    else:
        # noinspection PyTypeChecker
        with open(path, 'r') as file_name:
            text_data = file_name.read()
        return text_data


def del_comment_lines(text_data_list: list[str]):
    """
    Returns comment lines from strings.
    :param text_data_list: list[str]
    :return: list[str]
    """
    if is_type_is(text_data_list, list):
        for i in range(len(text_data_list)):
            text_data = text_data_list[i]
            for symbol in ('#', '!', '$'):
                if symbol in text_data:
                    text_data_list[i] = text_data[:text_data.find(symbol)].strip()
        return remove_elements(text_data_list, '')


def remove_elements(iter_data, value):
    """
    Remove elements from list or tuple.
    :param iter_data: list or tuple
    :param value: element value or tuple of elements values
    """
    if is_type_is(iter_data, (list, tuple)):
        iterable_value = make_it_list(value)
        clear_data = [x for x in iter_data if all([x != y for y in iterable_value])]
        return clear_data


def handle_text_data(text_data):
    """
    Handling text data.
    :param text_data: str
    :return: list[list]
    """
    if is_type_is(text_data, str):
        string_data = split_text(text_data, '\n')
        clear_string_data = del_comment_lines(string_data)
        return [split_text(x, ('\t', ' ', ','))
                for x in remove_elements(clear_string_data, [[]])]


def is_type_is(my_data, data_type):
    """
    Check if type od data is suggested type and generates TypeError in other case.
    Like function isinstance, but with raising exception.
    """
    iter_data_type = make_it_list(data_type)
    if not any(isinstance(my_data, d_type) for d_type in iter_data_type):
        raise TypeError(f'Wrong type of input data. Expected data type: {data_type}.\n'
                        f'{get_function_info()} \n'
                        f'Inputted data type: {type(my_data)}.')
    return True


def make_it_list(value):
    """
    Check if value is list or tuple. If it is not make list(value).
    """
    if not any(isinstance(value, iter_type) for iter_type in (list, tuple)):
        iter_value = [value]
    else:
        iter_value = value
    return iter_value


def split_text(text, char):
    """
    Split string with chars and remove all empty strings ''.
    :param text: string
    :param char: char or list/ tuple of chars
    :return: list
    """
    iter_char = make_it_list(char)
    if is_type_is(text, str) and all(char not in text for char in iter_char):
        raise ValueError(f'No symbol {char} in string.\n'
                         f'{get_function_info()} \n'
                         f'Inputted string: {text}.')
    else:
        return remove_elements(re.split('|'.join(iter_char), text), '')


def calc_fft_recursively(data):
    """
    FFT calculation
    :param data: list of float
    :return: list of complex
    """
    if not is_list_of_float(data):
        raise TypeError(f'Wrong type of input data. Expected data type: list[float]. \n'
                        f'{get_function_info()} \n'
                        f'Inputted data: {data}.')
    data_len = len(data)
    if data_len <= 1:
        return data
    even = calc_fft_recursively(data[0::2])
    odd = calc_fft_recursively(data[1::2])
    t = [exp(-2j * pi * k / data_len) * odd[k] for k in range(data_len // 2)]
    return [even[k] + t[k] for k in range(data_len // 2)] + \
           [even[k] - t[k] for k in range(data_len // 2)]


def is_list_of_float(data):
    """
    Check if data is list of float.
    :param data:
    :return: bool
    """
    return False if not isinstance(data, list) else all(isinstance(x, float) for x in data)


def get_function_info():
    """
    Return information about current function
    """
    info_object = inspect.stack()[1]
    info = f'File name: {info_object[1]};\n' \
           f'function name: {info_object[3]}.'
    return info


if __name__ == '__main__':
    pass

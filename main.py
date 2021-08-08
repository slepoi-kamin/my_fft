from cmath import exp, pi
import pathlib
import inspect


class TimeData:

    def __init__(self, path: pathlib.Path):
        self.__import_time_data(path)

    def __import_time_data(self, path: pathlib.Path):
        read_from_file(path)


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
        return text_data_list


def remove_elements(iter_data, value):
    """
    Remove elements from list or tuple.
    :param iter_data: list or tuple
    :param value: element value or tuple of elements values
    """
    if is_type_is(iter_data, (list, tuple)):
        if not any(isinstance(value, iter_type) for iter_type in (list, tuple)):
            iterable_value = [value]
        else:
            iterable_value = value
        clear_data = [x for x in iter_data if all([x != y for y in iterable_value])]
        return clear_data


# TODO: finish this function
def handle_text_data(text_data):
    string_data = split_text(text_data)

    clear_string_data = del_comment_lines(string_data)


def is_type_is(my_data, data_type):
    """
    Check if type od data is suggested type and generates TypeError in other case.
    Like function isinstance, but with raising exception.
    """
    if not any(isinstance(data_type, iter_type) for iter_type in (list, tuple)):
        iter_data_type = [data_type]
    else:
        iter_data_type = data_type
    if not any(isinstance(my_data, d_type) for d_type in iter_data_type):
        raise TypeError(f'Wrong type of input data. Expected data type: {data_type}.\n'
                        f'{get_function_info()} \n'
                        f'Inputted data type: {type(my_data)}.')
    return True


# TODO: add tuple possibility for char
def split_text(text, char):
    if is_type_is(text, str) and char not in text:
        raise ValueError(f'No symbol {char} in string.\n'
                         f'{get_function_info()} \n'
                         f'Inputted string: {text}.')
    else:
        return list(map(lambda x: x.strip(), text.split(char)))


# def split_data_to_list_of_str(text_data):
#     if '\n' not in text_data:
#         raise ValueError(f'No strings in data.\n'
#                          f'{get_function_info()} \n'
#                          f'Inputted data: {text_data}.')
#     return text_data.split('\n')


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
    # print(' '.join("%5.3f" % abs(f)
    #                for f in calc_fft_recursively([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0])))

    # data = 'Time \tdata1 ,data2\n' \
    #        '0.001 0.0\t 0.0 \n' \
    #        ' 0.001\t 0.0    1.0 \n' \
    #        '0.001 ,1.0\t0.0\n' \
    #        '0.001\t  1.0,  1.0\n'



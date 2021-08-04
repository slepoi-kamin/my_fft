from cmath import exp, pi
import inspect


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

    print(' '.join("%5.3f" % abs(f)
                   for f in calc_fft_recursively([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0])))

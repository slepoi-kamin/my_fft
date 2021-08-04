import pytest

from main import *


@pytest.mark.parametrize('test_input, expected', [
    ([], []),
    ([0.0, 0.0, 0.0, 0.0], [0j, 0j, 0j, 0j]),
    ([1.0, 1.0, 1.0, 1.0], [4 + 0j, 0j, 0j, 0j]),
])
def test_calc_fft_recursively_simple(test_input, expected):
    assert calc_fft_recursively(test_input) == expected, \
        f'ValueError: calc_fft_recursively({test_input}) == ' \
        f'{calc_fft_recursively(test_input)}, expected {expected}'


@pytest.mark.parametrize('test_input', [
    ([0]), '1', 'a', ([1.0, 1]), 1.0, ([1.0, '1']), ([1.0, True]), True,
])
def test_calc_fft_recursively_type_error(test_input):
    with pytest.raises(TypeError):
        calc_fft_recursively(test_input)


def test_calc_fft_recursively_full():
    test_input = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]
    expected = [4.0, 2.613, 0.0, 1.082, 0.0, 1.082, 0.0, 2.613]
    abs_complex = [round(abs(complex), 3) for complex in calc_fft_recursively(test_input)]
    assert abs_complex == expected, \
        f'ValueError: [round(abs(complex), 3) for complex ' \
        f'in calc_fft_recursively({test_input}) ' \
        f'== {abs_complex}, expected {expected}'


@pytest.mark.parametrize('test_input, expected', [
    (0, False),
    ([1.0, 1], False),
    (0.0, False),
    ('1.0', False),
    ('[1.0, 0.0]', False),
    ([1.0, 0.0], True),
    ([1.0, '0.0'], False),
])
def test_is_list_of_float(test_input, expected):
    assert is_list_of_float(test_input) == expected, \
        f'TypeError: is_list_of_float({test_input}) == ' \
        f'{is_list_of_float(test_input)}, expected {expected}'


def test_get_function_info():
    current_info_object = inspect.stack()[0]
    current_func_info = f'File name: {current_info_object[1]};\n' \
                        f'function name: {current_info_object[3]}.'
    assert get_function_info() == current_func_info, \
        f'ValueError: get_function_info() == \n{get_function_info()}\n' \
        f'    Expected: \n{current_func_info} '

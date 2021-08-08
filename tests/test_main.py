import pytest
import uuid
from main import *


CONTENT = 'time data1 data2\n1 2 3\n4 5 6'


@pytest.fixture
def tmp_file(tmp_path):
    temp_file = tmp_path / "tmp_file"
    temp_file.write_text(CONTENT)
    return temp_file


@pytest.fixture
def td(tmp_file):
    td = TimeData(tmp_file)
    return td


@pytest.fixture
def tmp_file_not_exists():
    return pathlib.Path(uuid.uuid4().hex)


class TestTimeData:

    def test_init(self, td):
        expected_dict = {
            'time': [1.0, 4.0],
            'data1': [2.0, 5.0],
            'data2': [3.0, 6.0],
        }
        assert td.text_data == CONTENT
        assert td.data == expected_dict
        # noinspection PyProtectedMember
        assert td._fft is None


class TestMakeDictFromData:

    def test_some_args(self):
        arg = [
            ['time', 'data1', 'data2'],
            ['1', '2', '3'],
            ['4', '5', '6'],
        ]
        expected = {
            'time': [1.0, 4.0],
            'data1': [2.0, 5.0],
            'data2': [3.0, 6.0],
        }
        assert make_dict_from_data(arg) == expected

    def test_value_error(self):
        with pytest.raises(ValueError):
            make_dict_from_data([['1', '2']])


class TestTransposeList:

    @pytest.mark.parametrize('args, expected', [
        ([[1, 2], [3, 4]], [[1, 3], [2, 4]]),
    ])
    def test_some_data(self, args, expected):
        assert transpose_list(args) == expected


class TestIsColumnsHaveNames:

    def test_true(self):
        arg = [['Time']]
        assert is_columns_have_names(arg) is True

    def test_false(self):
        arg = [['tim']]
        assert is_columns_have_names(arg) is False


class TestMakeDataFloat:

    @pytest.mark.parametrize('args, expected', [
        ('1', 1.0),
        (1, 1.0),
        (['1', '2'], [1.0, 2.0]),
        ([['1', '2'], [3, 4]], [[1.0, 2.0], [3.0, 4.0]]),
    ])
    def test_some_args(self, args, expected):
        assert make_data_float(args) == expected


class TestHandleTextData:

    def test_wrong_args_format(self):
        with pytest.raises(TypeError):
            handle_text_data([1, 2])

    def test_some_args(self):
        args = '! comment\n' \
               '\n' \
               'abc abc, abc # comment \n' \
               '$ comment \n' \
               ' abc\t abc\tabc\n' \
               'abc abc,abc'
        expected = [['abc', 'abc', 'abc'],
                    ['abc', 'abc', 'abc'],
                    ['abc', 'abc', 'abc']]
        assert handle_text_data(args) == expected


class TestMakeItList:

    @pytest.mark.parametrize('args, expected', [
        ('a', ['a']), ((1, 2), (1, 2)), ([1, 2], [1, 2]),
    ])
    def test_some_args(self, args, expected):
        assert make_it_list(args) == expected


class TestRemoveElements:

    @pytest.mark.parametrize('args', [
        ('a', 'str'),
        (1, 'int'),
    ])
    def test_unexpected_data_type(self, args):
        with pytest.raises(TypeError):
            remove_elements(*args)

    @pytest.mark.parametrize('args, expected', [
        ((['a', '', 'a'], ''), ['a', 'a']),
        ((['a', '', ''], ''), ['a']),
        ((['', '', ''], ''), []),
        ((['a', '', 'a'], ('', 'a')), []),
        ((['a', '', 'b', 'c'], ['', 'a']), ['b', 'c']),
        ((('a', '', 'a'), ''), ['a', 'a']),
        ((['a', [], 'a'], [[]]), ['a', 'a']),
    ])
    def test_some_data(self, args, expected):
        assert remove_elements(*args) == expected


class TestIsTypeIs:

    @pytest.mark.parametrize('args', [
        ('a', str),
        ([], list),
        (1, int),
        (0.0, float),
    ])
    def test_expected_data_types(self, args):
        assert is_type_is(*args) is True

    @pytest.mark.parametrize('args', [
        ('a', list),
        ([], float),
        (1, str),
        (0.0, int),
    ])
    def test_unexpected_data_types(self, args):
        with pytest.raises(TypeError):
            is_type_is(*args)

    @pytest.mark.parametrize('args', [
        ([], (list, float)),
        (1, [int, str]),
    ])
    def test_iterable_expected_data_types(self, args):
        assert is_type_is(*args) is True

    @pytest.mark.parametrize('args', [
        ('a', (list, float)),
        ([], [float, tuple]),
    ])
    def test_iterable_unexpected_data_types(self, args):
        with pytest.raises(TypeError):
            is_type_is(*args)


class TestSplitText:

    @pytest.mark.parametrize('args', [
        ('a!a$a#aa\ta', '\n'),
        ('a!a$a#a\naa', '\t'),
    ])
    def test_value_error(self, args):
        with pytest.raises(ValueError):
            split_text(*args)

    @pytest.mark.parametrize('args', [
        (1, '\n'),
        (1.0, '\n'),
        ([], '\n'),
        ((1, 2), '\n'),
    ])
    def test_type_error(self, args):
        with pytest.raises(TypeError):
            split_text(*args)

    @pytest.mark.parametrize('args, expected', [
        (('a!a$a#a\na\ta', '\n'), ['a!a$a#a', 'a\ta']),
        (('a!a$a#a\na\ta', '\t'), ['a!a$a#a\na', 'a']),
        (('a!a$a#  a\na\ta', ' '), ['a!a$a#', 'a\na\ta']),
    ])
    def test_some_data(self, args, expected):
        assert split_text(*args) == expected

    @pytest.mark.parametrize('args', [
        ('ccacbccbcaa', ('g', 'h')),
        ('ccacbccbcaa', ['g', 'h']),
    ])
    def test_value_error_with_list_of_chars(self, args):
        with pytest.raises(ValueError):
            split_text(*args)

    @pytest.mark.parametrize('args, expected', [
        (('ccacbccbcaa', ('a', 'b')), ['cc', 'c', 'cc', 'c']),
        (('ccacbccbcaa', ['a', 'j']), ['cc', 'cbccbc']),
    ])
    def test_some_args_with_list_of_chars(self, args, expected):
        assert split_text(*args) == expected


# class TestSplitDataToListOfStr:
#
#     def test_wrong_value(self):
#         with pytest.raises(ValueError):
#             split_data_to_list_of_str('argslkjsldkjfl ksljdfl \t lkjslfd')
#
#     @pytest.mark.parametrize('args, expected', [
#         ('ab\nc', ['ab', 'c']),
#         ('a\nb\nc', ['a', 'b', 'c']),
#         ('\na\nb\nc\n', ['', 'a', 'b', 'c', '']),
#     ])
#     def test_some_inputs(self, args, expected):
#         assert split_data_to_list_of_str(args) == expected


class TestDelCommentLines:

    @pytest.mark.parametrize('args', [('sd', 1), 'dsfds'])
    def test_wrong_data_type(self, args):
        with pytest.raises(TypeError):
            del_comment_lines(*args)

    @pytest.mark.parametrize('args, expected', [
        ([], []),
        (['#aaa'], []),
        (['a!aa'], ['a']),
        (['aaa$'], ['aaa']),
        ([' a a #aa'], ['a a']),
        ([' a a #aa', ' a! a aa', ' a a a$a'], ['a a', 'a', 'a a a']),
    ])
    def test_different_data(self, args, expected):
        assert del_comment_lines(args) == expected


class TestReadFromFile:

    def test_file_exists(self, tmp_file_not_exists):
        with pytest.raises(FileExistsError):
            read_from_file(tmp_file_not_exists)

    @pytest.mark.parametrize('args', [tmp_file, 'temp_file.txt'])
    def test_wrong_path_format(self, args):
        with pytest.raises(TypeError):
            read_from_file(*args)

    def test_file_content(self, tmp_file):
        assert read_from_file(tmp_file) == CONTENT


class TestCalcFFTRecursively:

    @pytest.mark.parametrize('test_input, expected', [
        ([], []),
        ([0.0, 0.0, 0.0, 0.0], [0j, 0j, 0j, 0j]),
        ([1.0, 1.0, 1.0, 1.0], [4 + 0j, 0j, 0j, 0j]),
    ])
    def test_calc_fft_recursively_simple(self, test_input, expected):
        assert calc_fft_recursively(test_input) == expected, \
            f'ValueError: calc_fft_recursively({test_input}) == ' \
            f'{calc_fft_recursively(test_input)}, expected {expected}'

    @pytest.mark.parametrize('test_input', [
        ([0]), '1', 'a', ([1.0, 1]), 1.0, ([1.0, '1']), ([1.0, True]), True,
    ])
    def test_calc_fft_recursively_type_error(self, test_input):
        with pytest.raises(TypeError):
            calc_fft_recursively(test_input)

    def test_calc_fft_recursively_full(self):
        test_input = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0]
        expected = [4.0, 2.613, 0.0, 1.082, 0.0, 1.082, 0.0, 2.613]
        abs_complex = [round(abs(compl), 3) for compl in calc_fft_recursively(test_input)]
        assert abs_complex == expected, \
            f'ValueError: [round(abs(complex), 3) for complex ' \
            f'in calc_fft_recursively({test_input}) ' \
            f'== {abs_complex}, expected {expected}'


class TestIsListOfFloat:

    @pytest.mark.parametrize('test_input, expected', [
        (0, False),
        ([1.0, 1], False),
        (0.0, False),
        ('1.0', False),
        ('[1.0, 0.0]', False),
        ([1.0, 0.0], True),
        ([1.0, '0.0'], False),
    ])
    def test_is_list_of_float(self, test_input, expected):
        assert is_list_of_float(test_input) == expected, \
            f'TypeError: is_list_of_float({test_input}) == ' \
            f'{is_list_of_float(test_input)}, expected {expected}'


class TestGetFunctionInfo:

    def test_get_function_info(self):
        current_info_object = inspect.stack()[0]
        current_func_info = f'File name: {current_info_object[1]};\n' \
                            f'function name: {current_info_object[3]}.'
        assert get_function_info() == current_func_info, \
            f'ValueError: get_function_info() == \n{get_function_info()}\n' \
            f'    Expected: \n{current_func_info} '

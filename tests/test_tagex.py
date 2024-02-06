import pytest
from src import __main__ as main

# def tagex_variable_result(tagex_variable):
# reading_regex = False
# for char in tagex_variable:
#     if char == "/":
#         reading_regex = True
# variables = {
#     "dir0": {
#         "def": "[2020-10-30] Post Human- Survival Horror",
#         "res": "[2020-10-30] Post Human- Survival Horror",
#     },
#     "date": {
#         "def": "/[(\d*)]/{variables}",
#         "res": "2018-12-10",
#     },
#     "year": {"def": "/\d\{3\}/{date}"},
# }

@pytest.mark.parametrize(
    "tagex_variable, expected_evaluation",
    [
        ("this is Static.", "this is Static."),  # no regex returns same string
        ("/(.*)/hello", "hello"),  # match all regex group returns same string w/o regex
        # ("/.*/hello", ""),  # no capture group remove
        # ("/.*/hello world", ""),  # no capture group evaluates to nothing
        # ("/(.*)/hello world", "hello world"),  # works with whitespace
        # ("/(.*)/HelloWorld", "Hello World"),  # works with capital letters
        # (
        #     "/(\w*)\s(\w*)/hello world",
        #     "hello",
        # ),  # multiple capture groups uses only first group
        # ("hello world /.*/sausage", "hello world"),  # use regex on substring
        # (
        #     "/.*/sausage //hello world",
        #     "hello world",
        # ),  # '//' cancels regex for upcoming substring
        # (
        #     "/(.*)/sausage //hello /(.*)/world",
        #     "sausage world",
        # ),  # multiple regex expressions per substring
        # ("//hello world/.*/sausage", "hello world"),
        # ("/", "/"),
        # ("/(.*)/hello/", "hello"),
    ],
)
def test_tagex_variable_result(tagex_variable, expected_evaluation):
    assert main.tagex_variable_result(tagex_variable) == expected_evaluation

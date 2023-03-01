from io import StringIO

from sqltask_lib.parser import JinjaCommentParser


def open_reader(text):
    return StringIO(text)


def parse_comment(text):
    return JinjaCommentParser().parse_top_comment(text)


def run_test(expected_comment, template_content):
    result = parse_comment(template_content)
    assert expected_comment == result


def test_parses_only_comment():
    text = "{#\nline1\nline2\n#}"
    expected_comment = "line1\nline2"
    run_test(expected_comment, text)


def test_parses_first_comment():
    text = "{#\nline1\nline2\n#}\n{#\nline3\n#}\n"
    expected_comment = "line1\nline2"
    run_test(expected_comment, text)


def test_parses_when_no_comment():
    text = "no comment"
    expected_comment = ""
    run_test(expected_comment, text)


def test_parses_ignores_white_spaces():
    text = " {#\nhi\n #} "
    expected_comment = "hi"
    run_test(expected_comment, text)


def test_parses_text_first_then_comment_returns_empty():
    text = "text\n{#\ncomment#} "
    expected_comment = ""
    run_test(expected_comment, text)


def test_parses_when_starts_with_blank_line_with_spaces():
    text = "  \n{#\ncomment\n#} "
    expected_comment = "comment"
    run_test(expected_comment, text)


def test_parses_inline_open_comment():
    text = "{#line1\nline2\n#}"
    expected_comment = "line1\nline2"
    run_test(expected_comment, text)


def test_parses_inline_close_comment():
    text = "{#\nline1\nline2#}"
    expected_comment = "line1\nline2"
    run_test(expected_comment, text)


def test_parses_inline_both_inline_comment():
    text = "{#line1\nline2#}"
    expected_comment = "line1\nline2"
    run_test(expected_comment, text)


def test_parses_oneline_comment():
    text = "{#line1#}"
    expected_comment = "line1"
    run_test(expected_comment, text)


def test_parses_without_commend_end_returns_empty():
    text = "{#line1"
    expected_comment = ""
    run_test(expected_comment, text)

from sqltask_lib.parser import IniParser


def parse_section_body(title, text):
    return IniParser(text).get(title)


def test_parse_one_section_body():
    text = "[long_description]\nline1\nline2"
    expected_result = "line1\nline2"
    result = parse_section_body("long_description", text)
    assert expected_result == result


def test_parse_multiple_section_bodies():
    text = "[long_description]\nthis is long\ndescription\n[oneline_description]\nthis is oneliner"
    assert "this is long\ndescription\n" == parse_section_body("long_description", text)
    assert "this is oneliner" == parse_section_body("oneline_description", text)


def test_parse_non_existent_section_returns_empty():
    text = "no section"
    assert "" == parse_section_body("short_description", text)

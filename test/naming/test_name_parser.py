import pytest
from st_librarian.naming import TaskNameParser, TaskName

def parse(str_name):
    return TaskNameParser().parse(str_name)


def assert_equals(expected_name, str_name):
    name = parse(str_name)
    assert expected_name == name


def n(action, main, second):
    return TaskName(action=action, main_entity=main, secondary_entity=second)


test_values = [
    (n("Add", "Activity", "Perspective"), "add_activity_to_perspective"),
    (n("Add", "Category", None), "add_category"),
    (n("Add", "Category", None), "add_category"),
    (n("Add", "Dynamic Entity", None), "add_dynamic_entity"),
    (n("Add", "Dynamic Entity Field", None), "add_dynamic_entity_field"),
    (n("Remove", "Entitlement", "Agent"), "remove_entitlement_from_agent"),
    (n("Add", "Agent", None), "add_agent_for_development"),
    (n("Add", "Activity", "Perspective"), "add_activity_to_perspective_with_seq_no"),
]


@pytest.mark.parametrize("expected,test_input", test_values)
def test_some(expected, test_input):
    assert_equals(expected, test_input)

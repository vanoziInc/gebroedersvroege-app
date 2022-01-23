import pytest

# test_my_application.py
@pytest.mark.frontendtest
def test_example_is_working(page):
    page.goto("https://example.com")
    assert page.inner_text('h1') == 'Example Domain'
    page.click("text=More information")
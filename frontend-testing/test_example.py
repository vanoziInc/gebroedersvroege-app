import pytest

def test_example_is_working(page):
    page.goto("http://frontend.localhost/auth/login")
    assert page.inner_text('//input[@data-test="email-input"]/preceding-sibling::label') == 'E-mail adres'
from typing import Any

import pytest
from pytest_asyncio import is_async_test

pytest_plugins = ("app.tests.fixtures",)


def pytest_collection_modifyitems(items: Any) -> None:
    """
    https://pytest-asyncio.readthedocs.io/en/stable/how-to-guides/run_session_tests_in_same_loop.html
    pyproject.toml 의
    [tool.pytest.ini_options]
    asyncio_default_fixture_loop_scope = "session"

    설정은 fixture 의 scope 만 변경한다...! 이 설정만 하면 다른 모든 test 함수는 session scope 의 loop 를 쓰지 않는다.
    이 함수야말로 모든 테스트가 같은 루프를 쓰게 해준다. (아니 왜 이렇게 만들었나...)
    """
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)

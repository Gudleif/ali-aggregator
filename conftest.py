import pytest
from django.core.cache import cache

@pytest.fixture(autouse=True)
def clear_cache_before_each_test():
    """
    Эта фикстура запускается АВТОМАТИЧЕСКИ (autouse=True) перед каждым тестом.
    Она полностью очищает кэш, гарантируя, что тесты работают в изолированной и чистой среде.
    """
    cache.clear()
    yield
    cache.clear()
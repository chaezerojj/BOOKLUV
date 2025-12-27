from django.test import TestCase
from django.db import connections
from django.core.cache import cache

class InfrastructureTest(TestCase):
    def test_database_connection(self):
        """DB 연결 확인"""
        db_conn = connections['default']
        try:
            db_conn.cursor()
        except Exception:
            self.fail("DB 연결에 실패했습니다!")

    def test_redis_connection(self):
        """Redis 연결 확인 (캐시 사용 시)"""
        cache.set('connection_test', 'ok', timeout=5)
        self.assertEqual(cache.get('connection_test'), 'ok')
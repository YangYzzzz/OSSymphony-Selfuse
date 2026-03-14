"""Unit tests for gateway/session.py."""

import threading
import time

from gateway.session import SessionManager


class TestSessionManager:
    def test_create_returns_unique_tokens(self):
        sm = SessionManager()
        t1 = sm.create_session("http://w1:9100", 0)
        t2 = sm.create_session("http://w1:9100", 1)
        assert t1 != t2

    def test_get_returns_correct_session(self):
        sm = SessionManager()
        token = sm.create_session("http://w1:9100", 3)
        sess = sm.get_session(token)
        assert sess is not None
        assert sess.worker_url == "http://w1:9100"
        assert sess.local_env_id == 3

    def test_get_updates_last_activity(self):
        sm = SessionManager()
        token = sm.create_session("http://w1:9100", 0)
        sess = sm.get_session(token)
        old_activity = sess.last_activity
        time.sleep(0.05)
        sm.get_session(token)
        assert sess.last_activity > old_activity

    def test_get_nonexistent_returns_none(self):
        sm = SessionManager()
        assert sm.get_session("nonexistent") is None

    def test_remove_then_get_returns_none(self):
        sm = SessionManager()
        token = sm.create_session("http://w1:9100", 0)
        removed = sm.remove_session(token)
        assert removed is not None
        assert removed.token == token
        assert sm.get_session(token) is None

    def test_remove_nonexistent_returns_none(self):
        sm = SessionManager()
        assert sm.remove_session("nope") is None

    def test_cleanup_expired_removes_old_sessions(self):
        sm = SessionManager(timeout=0.05)
        sm.create_session("http://w1:9100", 0)
        sm.create_session("http://w1:9100", 1)
        time.sleep(0.1)
        expired = sm.cleanup_expired()
        assert len(expired) == 2
        assert sm.count == 0

    def test_cleanup_expired_keeps_fresh_sessions(self):
        sm = SessionManager(timeout=10.0)
        sm.create_session("http://w1:9100", 0)
        expired = sm.cleanup_expired()
        assert len(expired) == 0
        assert sm.count == 1

    def test_count_property(self):
        sm = SessionManager()
        assert sm.count == 0
        sm.create_session("http://w1:9100", 0)
        sm.create_session("http://w1:9100", 1)
        assert sm.count == 2
        sm.remove_session(sm.get_session(sm.create_session("http://w1:9100", 2)).token)
        # created 3, removed 1
        assert sm.count == 2

    def test_concurrent_create_thread_safety(self):
        sm = SessionManager()
        tokens = []
        lock = threading.Lock()

        def create_many():
            for _ in range(100):
                tok = sm.create_session("http://w1:9100", 0)
                with lock:
                    tokens.append(tok)

        threads = [threading.Thread(target=create_many) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(tokens) == 400
        assert len(set(tokens)) == 400  # all unique
        assert sm.count == 400

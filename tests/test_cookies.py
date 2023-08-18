import unittest, datetime, time

import jwt

import src.cookies as cookies


class TestCookies(unittest.TestCase):

    @staticmethod
    def mock_cookie(secret, dt, payload={}):
        return jwt.encode(payload | { "exp": datetime.datetime.utcnow() + dt }, secret)

    def test_new_cookie(self):
        secret = "abc123"
        payload = { "key": "value" }
        dt = datetime.timedelta(seconds=5)

        jwt_result = self.mock_cookie(secret, dt, payload)
        cookie_result = cookies.new_cookie(secret=secret, exp=dt, payload=payload)

        self.assertEqual(jwt_result, cookie_result)

    def test_validate_cookie(self):
        secret = "123abc"
        dt = datetime.timedelta(seconds=1)
        cookie = self.mock_cookie(secret, dt)

        self.assertTrue(cookies.validate_cookie(cookie, secret=secret))
        time.sleep(2)
        self.assertFalse(cookies.validate_cookie(cookie, secret=secret))

    def test_get_cookie(self):
        secret = "1a2b3c"
        dt = datetime.timedelta(seconds=1)
        payload = { "key": "value" }

        cookie = self.mock_cookie(secret, dt, payload)
        result1 = cookies.get_cookie(cookie, secret=secret)

        self.assertEqual(result1, payload)
        time.sleep(2)

        result2 = cookies.get_cookie(cookie, secret=secret)
        self.assertEqual(result2, {})

    def test_get_cookie_from(self):
        secret = "1a2b3c"
        dt = datetime.timedelta(seconds=5)
        payload = { "key": "value" }
        source = {
            "cookie": self.mock_cookie(secret, dt, payload)
        }
        result = cookies.get_cookie_from(source, "cookie", secret=secret)
        self.assertEqual(payload, result)


if __name__ == "__main__":
    unittest.main()
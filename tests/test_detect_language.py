import unittest
from unittest.mock import patch
from io import StringIO
from scripts.detect_language import main

config_path = "../scripts/language_detection_rules.json"
program_name = "program_name"


class TestCLIProgram(unittest.TestCase):
    test_apps = [
        (["apps/befunge-hello-world", config_path], "befunge"),
        (["apps/c-hello-world", config_path], "c"),
        (["apps/java-hello-world", config_path], "java"),
        (["apps/js-hello-world", config_path], "js"),
        (["apps/python-hello-world", config_path], "python"),
        (["apps/ts-hello-world", config_path], "js"),
    ]

    def _test_app(self, args, expected_result):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main(root_path=args[0], config_path=args[1])
            result = mock_stdout.getvalue().strip()
            self.assertEqual(expected_result, result)

    def _test_from_list(self, index):
        args, expected_result = self.test_apps[index]
        self._test_app(args=args, expected_result=expected_result)

    def test_all_befunge(self):
        return self._test_from_list(0)

    def test_all_C(self):
        return self._test_from_list(1)

    def test_all_java(self):
        return self._test_from_list(2)

    def test_all_javascript(self):
        return self._test_from_list(3)

    def test_all_python(self):
        return self._test_from_list(4)

    def test_all_typeScript(self):
        return self._test_from_list(5)


if __name__ == "__main__":
    unittest.main()

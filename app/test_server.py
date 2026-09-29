import unittest

from app.server import api_run, safe_web_path


class ServerTests(unittest.TestCase):
    def test_rejects_unknown_implementation(self):
        with self.assertRaises(ValueError):
            api_run("imaginary")

    def test_web_paths_stay_in_root(self):
        self.assertEqual(safe_web_path("/").name, "index.html")
        with self.assertRaises(ValueError):
            safe_web_path("/../experiment/allocator_ungated.py")

    def test_real_conformant_run(self):
        report = api_run("conformant")
        self.assertTrue(report["verified"])
        self.assertEqual(report["passed"], 6)


if __name__ == "__main__": unittest.main()

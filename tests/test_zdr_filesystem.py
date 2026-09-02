import os
import unittest
from security.zdr_filesystem import ZDRFilesystemScrubber

class TestZDRFilesystemScrubber(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_zdr_payload.tmp"
        with open(self.test_file, "w") as f:
            f.write("confidential_pii_credit_card_4111222233334444")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_secure_scrub_file_deletes_and_cleans(self):
        self.assertTrue(os.path.exists(self.test_file))
        result = ZDRFilesystemScrubber.secure_scrub_file(self.test_file)
        self.assertTrue(result)
        self.assertFalse(os.path.exists(self.test_file))

    def test_scrub_directory_cleans_all(self):
        test_dir = "test_zdr_dir"
        os.makedirs(test_dir, exist_ok=True)
        file1 = os.path.join(test_dir, "node1.dat")
        file2 = os.path.join(test_dir, "node2.dat")
        with open(file1, "w") as f: f.write("node1_data")
        with open(file2, "w") as f: f.write("node2_data")

        count = ZDRFilesystemScrubber.scrub_directory(test_dir)
        self.assertEqual(count, 2)
        self.assertFalse(os.path.exists(test_dir))

if __name__ == "__main__":
    unittest.main()

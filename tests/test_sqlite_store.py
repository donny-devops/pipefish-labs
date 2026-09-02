import unittest
from sdk.sqlite_store import SQLiteStore

class TestSQLiteStore(unittest.TestCase):
    def setUp(self):
        self.store = SQLiteStore(":memory:")

    def tearDown(self):
        self.store.close()

    def test_save_and_retrieve_execution(self):
        eid = self.store.save_execution(
            scenario="receptionist",
            status="COMPLETED",
            nodes=8,
            handoff_mode="mistral_native",
            payload={"caller": "test"}
        )
        record = self.store.get_execution(eid)
        self.assertIsNotNone(record)
        self.assertEqual(record["scenario"], "receptionist")
        self.assertEqual(record["nodes_executed"], 8)
        self.assertEqual(record["status"], "COMPLETED")

    def test_log_step(self):
        eid = self.store.save_execution(
            scenario="sales",
            status="RUNNING",
            nodes=1,
            handoff_mode="mistral_native",
            payload={}
        )
        self.store.log_step(eid, 0, "Lead Enrichment", "COMPLETED")
        record = self.store.get_execution(eid)
        self.assertIsNotNone(record)

if __name__ == "__main__":
    unittest.main()

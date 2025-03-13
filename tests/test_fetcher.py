import unittest
from src.pubmed_fetcher.fetcher import fetch_pubmed_papers

class TestPubMedFetcher(unittest.TestCase):
    def test_fetch_papers(self):
        papers = fetch_pubmed_papers("cancer treatment", max_results=2)
        self.assertGreater(len(papers), 0)
        self.assertIn("PubmedID", papers[0])

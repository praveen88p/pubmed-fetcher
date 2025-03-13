# pubmed_fetcher/cli.py
import argparse
import logging
from src.pubmed_fetcher.fetcher import fetch_pubmed_papers, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.info(f"Fetching papers for query: {args.query}")
    papers = fetch_pubmed_papers(args.query)

    if args.file:
        save_to_csv(papers, args.file)
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()

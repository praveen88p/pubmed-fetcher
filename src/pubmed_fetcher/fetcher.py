# pubmed_fetcher/fetcher.py
import requests
import logging
import pandas as pd
import re
from typing import List, Dict, Optional

import requests
import logging
from typing import List, Dict

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

# Company-related heuristics
COMPANY_KEYWORDS = {"Inc.", "Ltd.", "Pharma", "Biotech", "Therapeutics", "Diagnostics", "Sciences", "Laboratories"}
ACADEMIC_KEYWORDS = {"University", "Institute", "College", "Hospital", "School", "Research Center"}
COMPANY_EMAIL_DOMAINS = {"@pfizer.com", "@novartis.com", "@gsk.com", "@merck.com", "@roche.com"}

def fetch_pubmed_papers(query: str, max_results: int = 10) -> List[Dict]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }

    try:
        response = requests.get(PUBMED_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "esearchresult" not in data or "idlist" not in data["esearchresult"]:
            logging.warning("No results found for query.")
            return []

        pubmed_ids = data["esearchresult"]["idlist"]
        return fetch_paper_details(pubmed_ids)

    except requests.RequestException as e:
        logging.error(f"Error fetching papers from PubMed: {e}")
        return []

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "json"
    }

    try:
        response = requests.get(PUBMED_FETCH_URL, params=params)
        response.raise_for_status()
        data = response.json()

        papers = []
        for pubmed_id in pubmed_ids:
            paper_data = data["result"].get(pubmed_id, {})
            title = paper_data.get("title", "Unknown Title")
            pub_date = paper_data.get("pubdate", "Unknown Date")
            authors = extract_authors(paper_data)

            # Extract non-academic authors and their affiliations
            non_academic_authors = extract_company_affiliations(authors)

            papers.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": [a["name"] for a in non_academic_authors],
                "Company Affiliation(s)": [a["company"] for a in non_academic_authors],
                "Corresponding Author Email": get_corresponding_author_email(authors)
            })

        return papers

    except requests.RequestException as e:
        logging.error(f"Error fetching paper details from PubMed: {e}")
        return []

def extract_authors(paper_data: Dict) -> List[Dict]:
    authors = []
    for author in paper_data.get("authors", []):
        name = author.get("name", "Unknown")
        email = author.get("email", "")
        affiliations = author.get("affiliations", [])
        authors.append({"name": name, "email": email, "affiliations": affiliations})
    return authors

def extract_company_affiliations(authors: List[Dict]) -> List[Dict]:
    non_academic_authors = []
    
    for author in authors:
        name = author.get("name", "Unknown")
        email = author.get("email", "")
        affiliations = author.get("affiliations", [])
        
        # Check if the author's email belongs to a known company domain
        if email and any(email.endswith(domain) for domain in COMPANY_EMAIL_DOMAINS):
            non_academic_authors.append({"name": name, "company": email.split("@")[1]})
            continue  # No need to check further if email confirms company affiliation

        # Check affiliations for company presence
        for aff in affiliations:
            if is_non_academic(aff):
                non_academic_authors.append({"name": name, "company": aff})
                break  # Stop at the first valid company affiliation
    
    return non_academic_authors

def is_non_academic(affiliation: str) -> bool:
    if not affiliation:
        return False
    
    # Check for company-related keywords
    if any(keyword in affiliation for keyword in COMPANY_KEYWORDS):
        return True
    
    # Exclude known academic institutions
    if any(keyword in affiliation for keyword in ACADEMIC_KEYWORDS):
        return False

    return True  # Default to assuming it's a company if not explicitly academic

def get_corresponding_author_email(authors: List[Dict]) -> str:
    
    for author in authors:
        if author.get("email"):
            return author["email"]
    return "Not Available"

def save_to_csv(papers: List[Dict], filename: str):
    
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    logging.info(f"Results saved to {filename}")

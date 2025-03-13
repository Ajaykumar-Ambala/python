import argparse
import csv
import sys
import re
from Bio import Entrez
from itertools import zip_longest  # Fix for mismatch in author & affiliation lists

# Set your email and API key for NCBI Entrez API
Entrez.email = "your_email@example.com"  # Change this to your actual email
Entrez.api_key = "your_ncbi_api_key"  # Optional: Add your NCBI API key

# List of keywords to detect company affiliations
COMPANY_KEYWORDS = ["pharma", "biotech", "therapeutics", "laboratories", "inc", "ltd", "gmbh", "corporation"]

def fetch_pubmed_papers(query, debug=False):
    """Fetches PubMed papers based on the given query."""
    try:
        with Entrez.esearch(db="pubmed", term=query, retmax=50) as handle:
            record = Entrez.read(handle)
        
        pubmed_ids = record.get("IdList", [])
        papers = []
        
        for pubmed_id in pubmed_ids:
            with Entrez.efetch(db="pubmed", id=pubmed_id, rettype="medline", retmode="text") as handle:
                article = handle.read()
            
            title_match = re.search(r'TI  - (.+)', article)
            title = title_match.group(1) if title_match else "Unknown Title"

            date_match = re.search(r'DP  - (\d{4})', article)
            publication_date = date_match.group(1) if date_match else "Unknown Date"

            authors = re.findall(r'AU  - (.+)', article)
            affiliations = re.findall(r'AD  - (.+)', article)

            non_academic_authors = []
            company_affiliations = []

            for author, affil in zip_longest(authors, affiliations, fillvalue="No Affiliation Provided"):
                if any(keyword in affil.lower() for keyword in COMPANY_KEYWORDS):
                    non_academic_authors.append(author)
                    company_affiliations.append(affil)

            # Improved email extraction regex
            email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", article)
            corresponding_email = email_match.group(0) if email_match else "Not Available"

            if company_affiliations:
                papers.append([pubmed_id, title, publication_date, ", ".join(non_academic_authors), ", ".join(company_affiliations), corresponding_email])

            if debug:
                print(f"Processed {pubmed_id}: {title}")

        return papers
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return []

def save_to_csv(papers, filename):
    """Saves paper details to a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["PubMed ID", "Title", "Publication Date", "Non-academic Authors", "Company Affiliations", "Corresponding Author Email"])
            writer.writerows(papers)
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed with company affiliations.")
    parser.add_argument("query", help="PubMed search query")  
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file")

    args = parser.parse_args()
    
    papers = fetch_pubmed_papers(args.query, args.debug)
    
    if args.file:
        save_to_csv(papers, args.file)
    else:
        for paper in papers:
            print(" | ".join(paper))

if __name__ == "__main__":
    main()

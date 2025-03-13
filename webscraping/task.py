import arxiv
import csv
import re

# Function to fetch research papers based on a query
def fetch_papers(query):
    search = arxiv.Search(
        query=query,
        max_results=100,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    return search.results()

# Function to check if any author is affiliated with a pharmaceutical or biotech company
def is_pharma_biotech_affiliation(author):
    pharma_biotech_keywords = ['pharmaceutical', 'biotech', 'pharma', 'biotechnology']
    return any(keyword in author.affiliation.lower() for keyword in pharma_biotech_keywords if author.affiliation)

# Main program
def main():
    query = input("Enter your query: ")
    papers = fetch_papers(query)

    # List to store the results
    results = []

    for paper in papers:
        for author in paper.authors:
            if author.affiliation and is_pharma_biotech_affiliation(author):
                results.append({
                    'Title': paper.title,
                    'Authors': ", ".join([str(author) for author in paper.authors]),
                    'Affiliations': ", ".join([author.affiliation for author in paper.authors if author.affiliation]),
                    'Published Date': paper.published.strftime('%Y-%m-%d'),
                    'URL': paper.pdf_url
                })
                break

    # Save the results as a CSV file
    with open('research_papers.csv', 'w', newline='') as csvfile:
        fieldnames = ['Title', 'Authors', 'Affiliations', 'Published Date', 'URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to research_papers.csv with {len(results)} records.")

if __name__ == "__main__":
    main()

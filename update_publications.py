import json
from scholarly import scholarly
import time

# List of professors (you can add more as needed)
professors = [
    'Professor A',
    'Professor B',
    'Professor C'
]

def get_publications(professor_name):
    """
    Get publications for a given professor from Google Scholar using scholarly.
    """
    try:
        # Search for the professor on Google Scholar
        search_query = scholarly.search_author(professor_name)
        author = next(search_query)  # Get the first result
        author_id = author['id']
        
        # Fetch the publications
        publications = scholarly.fill(author, sections=['publications'])['publications']
        
        # Prepare a list of publications in the desired format
        pub_list = []
        for pub in publications:
            pub_data = {
                'title': pub['bib']['title'],
                'authors': pub['bib']['author'],
                'journal': pub['bib'].get('journal', 'N/A'),
                'year': pub['bib'].get('pub_year', 'N/A'),
                'link': pub.get('url', 'N/A')
            }
            pub_list.append(pub_data)
        
        return pub_list
    
    except Exception as e:
        print(f"Error retrieving publications for {professor_name}: {e}")
        return []

def load_existing_publications():
    """
    Load the existing publications from publications.json file.
    """
    try:
        with open('publications.json', 'r') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # If the file doesn't exist or is empty, return an empty list

def update_publications(professors):
    """
    Update the publications.json file by aggregating publications from multiple professors.
    Add only new publications that are not already present.
    """
    all_publications = load_existing_publications()  # Load existing publications
    
    # Create a set of existing publication titles and links for quick lookup
    existing_titles = {pub['title'] for pub in all_publications}
    existing_links = {pub['link'] for pub in all_publications}
    
    for professor in professors:
        print(f"Fetching publications for {professor}...")
        publications = get_publications(professor)
        
        # Filter out publications that are already in the existing list
        new_publications = [pub for pub in publications if pub['title'] not in existing_titles and pub['link'] not in existing_links]
        
        # Add the new publications to the list
        all_publications.extend(new_publications)
        
        # Add the titles and links of the new publications to the existing sets
        for pub in new_publications:
            existing_titles.add(pub['title'])
            existing_links.add(pub['link'])
        
        # Sleep to avoid being rate-limited by Google Scholar
        time.sleep(5)

    # Save the updated publications to a JSON file
    with open('publications.json', 'w') as json_file:
        json.dump(all_publications, json_file, indent=4)
    print("publications.json has been updated.")

if __name__ == '__main__':
    update_publications(professors)

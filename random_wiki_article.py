import wikipediaapi
import requests

# Function to get a random Wikipedia article title using MediaWiki API
def get_random_article_title(language='en'):
    url = f"https://{language}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "random",
        "rnnamespace": 0, # Only get articles (namespace 0)
        "rnlimit": 1,
        "format": "json"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        title = data['query']['random'][0]['title']
        return title
    except requests.exceptions.RequestException as e:
        print(f"Error fetching random article title: {e}")
        return None

# Helper function to print sections recursively
def print_sections(sections, level=0):
    for s in sections:
        # Indent based on section level
        indent = "  " * level
        # Print section title and a snippet of text
        print(f"{indent}## {s.title}")
        # Limit text preview to first 200 characters for brevity
        print(f"{indent}{s.text[:200]}...")

        # Recursively print subsections
        if s.sections:
            print_sections(s.sections, level + 1)

# Main part of the script
if __name__ == "__main__":
    # Specify your project's user agent
    # Replace 'MyProjectName' and 'merlin@example.com' with your actual project name and contact
    user_agent = 'RandomWikiReflectionTool (YourProjectName <your_email@example.com>)'
    language = 'en' # You can change the language here

    random_title = get_random_article_title(language)

    if random_title:
        print(f"Fetching article: {random_title}")

        # Initialize Wikipedia API
        wiki_wiki = wikipediaapi.Wikipedia(
            user_agent=user_agent,
            language=language,
            extract_format=wikipediaapi.ExtractFormat.WIKI # Or ExtractFormat.HTML
        )

        page = wiki_wiki.page(random_title)

        if page.exists():
            print("\n" + "=" * 50) # Top separator
            print(f"Article: {page.title}")
            print("=" * 50 + "\n") # Bottom separator for title

            # Print Summary
            print("Summary:")
            print("-" * 10)
            print(page.summary)
            print("\n") # Add a newline after summary

            # Print Sections
            if page.sections:
                print("Sections:")
                print("-" * 10)
                print_sections(page.sections)
                print("\n") # Add a newline after sections

            # Print Categories
            if page.categories:
                print("Categories:")
                print("-" * 10)
                # Categories are returned as a dictionary-like object
                for category_title in sorted(page.categories.keys()):
                    # Print the full category title
                    print(f"- {category_title}")
                print("\n")

        else:
            print(f"Article '{random_title}' not found.")
    else:
        print("Could not retrieve a random article title.") 
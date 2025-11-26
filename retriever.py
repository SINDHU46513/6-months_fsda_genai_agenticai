import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser

# Define the schema for the index
schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))

# Specify the index directory
index_dir = 'indexdir'

# Create the index directory if it doesn't exist
os.makedirs(index_dir, exist_ok=True)

# Create the index
ix = create_in(index_dir, schema)

# Add documents to the index
writer = ix.writer()
writer.add_document(title='Eiffel Tower', content='The Eiffel Tower is iconic.')
writer.add_document(title='Louvre Museum', content='The Louvre Museum is famous for its art.')
writer.commit()  # Commit changes to the index

def retrieve_information(query):
    with ix.searcher() as searcher:
        query_parser = QueryParser("content", ix.schema)  # Create a query parser
        parsed_query = query_parser.parse(query)  # Parse the user's query
        
        results = searcher.search(parsed_query, limit=1)  # Search for the query
        
        if results:
            return results[0]['content']  # Return the content of the first result
        else:
            return None  # Return None if no results found

# Example usage
query = "iconic"
result = retrieve_information(query)
print(result)  # Output: The Eiffel Tower is iconic.


# Loads data for both books and movies, returning a dictionary with two keys, 'books' and 'movies', one for
# each subset of the collection.
def load_collections():
    # Load the two collections.
    book_collection, max_book_id = load_collection("books.csv")
    movie_collection, max_movie_id = load_collection("movies.csv")
    # Check for error.
    if book_collection is None or movie_collection is None:
        return None, None
    # Return the composite dictionary.
    return {"books": book_collection, "movies": movie_collection}, max(max_book_id, max_movie_id)

# Loads a single collection and returns the data as a dictionary.  Upon error, None is returned.
def load_collection(file_name):
    max_id = -1
    try:
        # Create an empty collection.
        collection = {}

        # Open the file and read the field names
        collection_file = open(file_name, "r")
        field_names = collection_file.readline().rstrip().split(",")

        # Read the remaining lines, splitting on commas, and creating dictionaries (one for each item)
        for item in collection_file:
            field_values = item.rstrip().split(",")
            collection_item = {}
            for index in range(len(field_values)):
                if (field_names[index] == "Available") or (field_names[index] == "Copies") or (field_names[index] == "ID"):
                    collection_item[field_names[index]] = int(field_values[index])
                else:
                    collection_item[field_names[index]] = field_values[index]
            # Add the full item to the collection.
            collection[collection_item["ID"]] = collection_item
            # Update the max ID value
            max_id = max(max_id, collection_item["ID"])

        # Close the file now that we are done reading all of the lines.
        collection_file.close()

    # Catch IO Errors, with the File Not Found error the primary possible problem to detect.
    except FileNotFoundError:
        print("File not found when attempting to read", file_name)
        return None
    except IOError:
        print("Error in data file when reading", file_name)
        return None

    # Return the collection.
    return collection, max_id

def display_collection(x):
    count = 0
    for k,v in x.items():
        if "Director" in v.keys():
            # this is a movie
            print("ID:", k)
            print("Title:", v["Title"])
            print("Director:", v["Director"])
            print("Length:", v["Length"])
            print("Genre:", v["Genre"])
            print("Year:", v["Year"])
            print("Copies:", v["Copies"])
            print("Available:", v["Available"])
            print()
            count += 1
            if count % 10 == 0:
                print("Press m to quit or <enter> to continue:")
                choice = input()
                if choice == "m":
                    return
                else:
                    continue

        else:
            # this is a book
            print("ID:", k)
            print("Title:", v["Title"])
            print("Author:", v["Author"])
            print("Publisher:", v["Publisher"])
            print("Pages:", v["Pages"])
            print("Year:", v["Year"])
            print("Copies:", v["Copies"])
            print("Available:", v["Available"])
            print()
            count += 1
            if count % 10 == 0:
                print("Press m to quit or <enter> to continue:")
                choice = input()
                if choice == "m":
                    return
                else:
                    continue

def add_book(collection, max_id):
    new_book = {}  # Create an empty dictionary to store book details

    # Assume the user will provide necessary details for the new book.
    new_book["ID"] = max_id + 1  # Increment the ID for the new book
    new_book["Title"] = input("Enter the title of the book: ")
    new_book["Author"] = input("Enter the author of the book: ")
    new_book["Publisher"] = input("Enter the publisher of the book: ")
    new_book["Pages"] = int(input("Enter the number of pages: "))
    new_book["Year"] = int(input("Enter the publication year: "))
    new_book["Copies"] = int(input("Enter the number of copies available: "))
    new_book["Available"] = new_book["Copies"]  # Initially, all copies are available

    # Add the new book to the collection
    collection[new_book["ID"]] = new_book

    print("New book added successfully.")
    return collection, new_book["ID"]  # Return the updated collection and max_id

def add_movie(collection, max_id):
    new_movie = {}  # Create an empty dictionary to store movie details

    # Collect user input for the new movie
    try:
        new_movie["ID"] = max_id + 1  # Increment the ID for the new movie
        new_movie["Title"] = input("Enter the title of the movie: ")
        new_movie["Director"] = input("Enter the director of the movie: ")
        new_movie["Length"] = input("Enter the length of the movie: ")
        new_movie["Genre"] = input("Enter the genre: ")  # Store the genre as a string
        new_movie["Year"] = int(input("Enter the release year: "))
        new_movie["Copies"] = int(input("Enter the number of copies available: "))
        new_movie["Available"] = new_movie["Copies"]  # Initially, all copies are available

        # Add the new movie to the collection
        collection[new_movie["ID"]] = new_movie

        print("New movie added successfully.")
        return collection, new_movie["ID"]  # Return the updated collection and max_id

    except ValueError:
        print("Invalid input. Please enter a valid number for year and copies.")
        # You might add more specific error handling based on the expected input format
        # Retry adding the movie or handle the error as per your requirements
        return collection, max_id  # Return the original collection and max_id due to the error

# Assuming you have a dictionary of operations and the collection available

# Display the menu of commands and get user's selection.  Returns a string with  the user's reauexted command.
# No validation is performed.
def prompt_user_with_menu():
    print("\n\n********** Welcome to the Collection Manager. **********")
    print("COMMAND    FUNCTION")
    print("  ci         Check in an item")
    print("  co         Check out an item")
    print("  ab         Add a new book")
    print("  am         Add a new movie")
    print("  db         Display books")
    print("  dm         Display movies")
    print("  qb         Query for books")
    print("  qm         Query for movies")
    print("  x          Exit")
    return input("Please enter a command to proceed: ")
def query_collection(collection):
    query = input("Enter your query string: ").lower()

    matching_items = []
    count = 0

    for item_id, item_info in collection.items():
        # Check if the query string matches any item details
        if (query in item_info["Title"].lower()) or (query in item_info.get("Author", "").lower()) or (query in item_info.get("Publisher", "").lower()) or (query in item_info.get("Director", "").lower()) or (query in item_info.get("Genre", "").lower()):
            matching_items.append((item_id, item_info))

    if matching_items:
        print("Matching Items:")
        for item_id, item_info in matching_items:
            count += 1
            if "Director" in item_info:
                print("Movie ID:", item_id)
                print("Title:", item_info["Title"])
                print("Director:", item_info["Director"])
                print("Length:", item_info["Length"])
                print("Genre:", item_info["Genre"])
                print("Year:", item_info["Year"])
                print("Copies:", item_info["Copies"])
                print("Available:", item_info["Available"])
                print()
            else:
                print("Book ID:", item_id)
                print("Title:", item_info["Title"])
                print("Author:", item_info["Author"])
                print("Publisher:", item_info["Publisher"])
                print("Pages:", item_info["Pages"])
                print("Year:", item_info["Year"])
                print("Copies:", item_info["Copies"])
                print("Available:", item_info["Available"])
                print()

            if count % 10 == 0:
                print("Press 'm' to quit or <Enter> to continue:")
                choice = input()
                if choice.lower() == "m":
                    return

    else:
        print("No items found matching the query.")

def check_in_item(library_collections, item_id):
    book_collection = library_collections.get("books", {})
    movie_collection = library_collections.get("movies", {})

    if item_id in book_collection:
        collection = book_collection
        item_type = "book"
    elif item_id in movie_collection:
        collection = movie_collection
        item_type = "movie"
    else:
        print("The entered item ID is not valid. Please enter a valid ID.")
        return

    if collection[item_id]["Available"] < collection[item_id]["Copies"]:
        collection[item_id]["Available"] += 1
        print(f"{item_type.capitalize()} checked in successfully.")
    else:
        print(f"All copies are already available, so this {item_type} cannot be checked in.")

def check_out_item(library_collections, item_id):
    book_collection = library_collections.get("books", {})
    movie_collection = library_collections.get("movies", {})

    if item_id in book_collection:
        collection = book_collection
        item_type = "book"
    elif item_id in movie_collection:
        collection = movie_collection
        item_type = "movie"
    else:
        print("The entered item ID is not valid. Please enter a valid ID.")
        return

    if collection[item_id]["Available"] > 0:
        collection[item_id]["Available"] -= 1
        print(f"{item_type.capitalize()} checked out successfully.")
    else:
        print(f"No copies are available for this {item_type}.")

# This is the main program function.  It runs the main loop which prompts the user and performs the requested actions.
def main():
    # Load the collections, and check for an error.
    library_collections, max_existing_id = load_collections()

    if library_collections is None:
        print("The collections could not be loaded. Exiting.")
        return
    print("The collections have loaded successfully.")

    # user enters "x" to exit the program.  Calls the appropriate function that corresponds to the requested operation.

    operation = ""
    while operation != "x":

        # Map operations to functions
        operations = {
            "ci": lambda: check_in_item(library_collections, int(input("Enter the ID to check in: "))),
            "co": lambda: check_out_item(library_collections, int(input("Enter the ID to check out: "))),
            "ab": add_book,
            "am": add_movie,
            "db": lambda: display_collection(library_collections["books"]),
            "dm": lambda: display_collection(library_collections["movies"]),
            "qb": lambda: query_collection(library_collections["books"]),
            "qm": lambda: query_collection(library_collections["movies"]),
        }
        while True:
            operation = prompt_user_with_menu()
            if operation == "x":
                break  # Exit the loop if 'x' is entered

            # Check if the operation exists in the dictionary, then execute the corresponding function
            if operation in operations:
                if operation in ["db", "dm", "qb", "qm","ci","co"]:
                    operations[operation]()  # Call the function directly
                else:
                    max_existing_id = operations[operation](
                        library_collections.get("books" if "ab" in operation else "movies", {}), max_existing_id)
            else:
                print("Unknown command. Please try again.")

# Kick off the execution of the program.
main()



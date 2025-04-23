from new import scrape_college_website, clean_and_store_data, load_college_data, process_message, learn_from_conversation

def test_scraping_and_storage():
    # Scrape data from the website
    scraped_data = scrape_college_website()
    if scraped_data:
        print("Scraped Data:", scraped_data)
        
        # Clean and store the scraped data
        clean_and_store_data(scraped_data)
        
        # Load the stored data and print it
        stored_data = load_college_data()
        print("Stored Data:", stored_data)

def test_message_processing():
    # Example user message
    message = "Tell me about the courses"
    
    # Process the message and return relevant data
    response = process_message(message)
    print("Message Response:", response)

def test_learning_from_conversation():
    # Simulate a new piece of data being added
    message = "add_new_data: New course in Machine Learning"
    response = learn_from_conversation(message, "New course in Machine Learning")
    print("Learning Response:", response)

# Test each function
test_scraping_and_storage()
test_message_processing()
test_learning_from_conversation()

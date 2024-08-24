import pandas as pd
import requests                                   # Importing Libraries
from bs4 import BeautifulSoup


class ArticleExtractor:
    def __init__(self):
        self.data = pd.read_excel(r'C:\Users\Saarthak\Desktop\Test assignment 2\Input.xlsx')        #Add file path for Input.xlsx
        self.article_data = []

    def extract_articles(self):
        for i, url in enumerate(self.data['URL']):                                  #data is the dataframe containing information in Input.xlsx
            try:
                response = requests.get(url)                                        #creating get request on url
                soup = BeautifulSoup(response.text, 'html.parser')                  #parsing text in the url using BeautifulSoup library
                article_title = soup.find('title').text                             #Extrating title

                # Check for multiple specific div classes for article content
                article_content_classes = [
                    "td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type",
                    "td-post-content tagdiv-type"
                ]
                article_text = None
                for class_name in article_content_classes:                         #Extracting article text by accessing divs of the webpage
                    article_content = soup.find("div", class_=class_name)
                    if article_content:
                        article_text = article_content.get_text(strip=True, separator='\n')
                        break

                if not article_text:
                    print(f"No article text found for URL: {url}")
                    continue

                # Save the article text to a text file
                filename = f"{self.data['URL_ID'][i]}.txt" 
                file_path = r"C:\Users\Saarthak\Desktop\Test assignment 2\Text Files"
                with open(f"{file_path}\{filename}.txt", 'w+', encoding='utf-8') as file:   #Writing the text files in the same directory under Text files folder
                    file.writelines(article_title)
                    file.writelines("\n\n")
                    file.writelines(article_text)

                self.article_data.append({
                    'URL_ID': f"blackassign00{i+1}",
                    'URL': url,
                    'article_title': article_title,
                    'article_text': article_text
                })
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {url}, Skipping...")

    def save_to_csv(self):                                                    # function for saving csv into same directory, contains text and title for corresponding url_id and url
        df = pd.DataFrame(self.article_data)
        df.to_csv(r"C:\Users\Saarthak\Desktop\Test assignment 2\final1.csv", index=False)

# Instantiate the class
article_extractor = ArticleExtractor()

# Extract articles
article_extractor.extract_articles()

# Save extracted data to CSV
article_extractor.save_to_csv()

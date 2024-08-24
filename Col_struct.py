import os
import pandas as pd
import nltk

class Col_Structure:
    def __init__(self):               
        self.positive_dictionary, self.negative_dictionary = self.load_master_dictionary()

    def load_master_dictionary(self):                           #loading master_dictionary
        master_dict_folder = r"C:\Users\Saarthak\Desktop\Test assignment 2\MasterDictionary-20240402T090309Z-001\MasterDictionary"
        positive_file = os.path.join(master_dict_folder, "positive-words.txt")
        negative_file = os.path.join(master_dict_folder, "negative-words.txt")

        with open(positive_file, "r") as f:                                               
            positive_words = [line.strip() for line in f.readlines() if line.strip()]             #creating list of positive words from positive-words.txt

        with open(negative_file, "r") as f:
            negative_words = [line.strip() for line in f.readlines() if line.strip()]             #creating list of positive words from negative-words.txt

        return set(positive_words), set(negative_words)

    def Col_Structure_Primary(self, data):
            updated_list = []

            for i, j, article_text in zip(data['URL_ID'], data['URL'], data['article_text']):
                # Tokenize words using nltk
                if not isinstance(article_text, str):
                    article_text = str(article_text)
                preprocessed_word = nltk.word_tokenize(article_text.lower())

                # 1. POSITIVE SCORE
                positive_count = [word for word in preprocessed_word if word in self.positive_dictionary]
                positive_score = len(positive_count)

                # 2. NEGATIVE SCORE
                negative_count = [word for word in preprocessed_word if word in self.negative_dictionary]
                negative_score = len(negative_count)

                # 3. POLARITY SCORE
                polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

                # 4. SUBJECTIVITY SCORE
                subjective_score = (positive_score + negative_score) / ((len(preprocessed_word)) + 0.000001)

                # 5. AVG SENTENCE LENGTH
                total_sentences = len(nltk.tokenize.sent_tokenize(article_text))
                avg_sentence_length = round(len(preprocessed_word) / total_sentences, 0)

                # 6. PERCENTAGE OF COMPLEX WORDS and 9. COMPLEX WORD COUNT
                Percentage_of_Complex_words, total_num_of_complex_words_count = self.calculate_complexity_percentage(preprocessed_word)

                # 7. FOG INDEX
                FOG_Index = 0.4 * (avg_sentence_length + Percentage_of_Complex_words)

                # 8. AVG NUMBER OF WORDS PER SENTENCE
                Average_Number_of_Words_Per_Sentence = round(len(article_text.split()) / total_sentences, 0)

                # 10. WORD COUNT
                Word_Count = len(preprocessed_word)

                # 11. SYLLABLE PER WORD
                syllable_per_word = sum(self.count_syllables_per_word(word) for word in preprocessed_word)

                # 12. PERSONAL PRONOUNS
                personal_pronouns = self.Personal_pronoun_count(preprocessed_word)

                # 13. AVG WORD LENGTH
                avg_word_length = round(self.Average_Word_Length(preprocessed_word), 0) if len(preprocessed_word) > 0 else 0

                final_dict = {
                    'URL_ID': i,
                    'URL': j,
                    'POSITIVE_SCORE': positive_score,
                    'NEGATIVE_SCORE': negative_score,
                    'POLARITY_SCORE': polarity_score,
                    'SUBJECTIVITY_SCORE': subjective_score,
                    'AVG_SENTENCE_LENGTH': avg_sentence_length,
                    'PERCENTAGE_OF_COMPLEX_WORDS': Percentage_of_Complex_words,
                    'FOG_INDEX': FOG_Index,
                    'AVG_NUMBER_OF_WORDS_PER_SENTENCE': Average_Number_of_Words_Per_Sentence,
                    'COMPLEX_WORD_COUNT': total_num_of_complex_words_count,
                    'WORD_COUNT': Word_Count,
                    'SYLLABLE_PER_WORD': syllable_per_word,
                    'PERSONAL_PRONOUNS': personal_pronouns,
                    'AVG_WORD_LENGTH': avg_word_length
                }
                updated_list.append(final_dict)

            df = pd.DataFrame(updated_list)
            df.to_csv("C:\\Users\\Saarthak\\Desktop\\Test assignment 2\\Output.csv", index=False)

            return df

    def calculate_complexity_percentage(self, words):
        total_words = len(words)
        complex_words = [word for word in words if self.count_syllables_per_word(word) > 2]
        total_complex_words = len(complex_words)
        percentage_complex_words = (total_complex_words / total_words) * 100 if total_words > 0 else 0
        return percentage_complex_words, total_complex_words

    def count_syllables_per_word(self, word):
        vowels = "aeiouy"
        exceptions = ["es", "ed"]
        count = 0
        if len(word) <= 3:  # Single or double-letter words are typically single syllables
            return 1

        for i in range(len(word)):
            if i == 0 and word[i] in vowels:
                count += 1
            elif word[i] in vowels and word[i - 1] not in vowels:
                count += 1

        # Handle exceptions
        for exception in exceptions:
            if word.endswith(exception):
                count -= 1
                break  # If an exception is found, break out of the loop

        # Ensure that the count is at least 1
        if count == 0:
            count += 1

        return count

    def Personal_pronoun_count(self, words):
        personal_pronouns = ["i", "we", "my", "ours", "us"]
        count = sum(1 for word in words if word.lower() in personal_pronouns)
        return count

    def Average_Word_Length(self, words):
        total_chars = sum(len(word) for word in words)
        avg_word_length = total_chars / len(words) if len(words) > 0 else 0
        return avg_word_length


# Example usage
data = pd.read_csv("C:\\Users\\Saarthak\\Desktop\\Test assignment 2\\final2.csv")         #Use csv that has cleaned text 
analyzer = Col_Structure()
output_df = analyzer.Col_Structure_Primary(data)
print(output_df)


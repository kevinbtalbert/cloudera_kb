# Copyright 2023 Cloudera, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from cleantext import clean

# Download required NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def clean_text(text):
    # Tokenize text into sentences
    sentences = sent_tokenize(text)
    
    clean_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        
        # Handle words with internal capitalization
        new_words = []
        for word in words:
            # Identify words that have a capital letter not at the start (considering alphanumeric characters only)
            split_words = re.sub('([a-z0-9])([A-Z])', r'\1 \2', word)
            new_words.append(split_words)
        
        # Re-form the sentence
        clean_sentence = ' '.join(new_words)
        clean_sentences.append(clean_sentence)
    
    # Combine the cleaned sentences back into a paragraph
    clean_text = ' '.join(clean_sentences)
    
    # Optional: Convert to lower case
    # clean_text = clean_text.lower()
    
    return clean_text

def split_text_file(text, word_limit=200):
    sentences = sent_tokenize(text)
    word_count = 0
    text_chunks = []
    new_text = ""

    for sentence in sentences:
        sentence_words = sentence.split()
        sentence_word_count = len(sentence_words)

        if word_count + sentence_word_count > word_limit:
            text_chunks.append(new_text.strip())
            word_count = 0
            new_text = ""

        new_text += sentence + " "
        word_count += sentence_word_count

    # Add the last remaining part, if any
    if new_text:
        text_chunks.append(new_text.strip())
    
    return text_chunks

def process_files(root_directory):
    root_name = os.path.basename(root_directory)
    parent_dir = os.path.dirname(root_directory)
    clean_root_directory = os.path.join(parent_dir, "clean_" + root_name)
    
    for subdir, _, files in os.walk(root_directory):
        new_subdir = subdir.replace(root_directory, clean_root_directory)
        if not os.path.exists(new_subdir):
            os.makedirs(new_subdir)
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(subdir, file), 'r', encoding='utf-8') as f:
                    text = f.read()
                cleaned_text = clean_text(text)
                split_text = split_text_file(cleaned_text)

                for i, chunk in enumerate(split_text):
                    if file.endswith('.txt'):
                        file = file[:-4]
                    filename = (file + "_" + str(i) + ".txt")
                    with open(os.path.join(new_subdir, filename), 'w', encoding='utf-8') as f:
                        
                        f.write(chunk)

if __name__ == "__main__":
    root_directory = './data/2_website_contents'
    process_files(root_directory)

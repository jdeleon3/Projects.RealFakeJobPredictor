import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import pickle
import textstat 
from scipy.sparse import hstack
from sklearn.preprocessing import StandardScaler
import os

class TextClassifier:
    def __init__(self):
        """
        Initialize the TextClassifier with a DataFrame containing job descriptions and their corresponding labels.
        """        
        self.vectorizer = TfidfVectorizer(analyzer='word', stop_words='english', lowercase=True)
        self.scaler = StandardScaler()
        self.stopwords_list = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        
    def clean_text(self, text: str) -> str:
        """
        Clean the input text by removing special characters and converting to lowercase.
        """
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'[^\x00-\x7F]', '', text)
        return text
    
    def tokenize_and_stem_text(self, text: str) -> list:
        """
        Tokenize and stem the input text.
        """
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")
        tokens = word_tokenize(text)
        tokens = [self.stemmer.stem(word) for word in tokens if word not in self.stopwords_list]
        return tokens

    def fit(self, df: pd.DataFrame, columnName: str = 'description'):
        """
        Fit the TF-IDF vectorizer to the job descriptions in the DataFrame.
        columnName: str = 'description': The name of the column containing job descriptions.
        """ 
        
        if df is None or df.empty:
            raise ValueError("DataFrame is empty or not provided.")
        if columnName not in df.columns:
            raise ValueError(f"Column '{columnName}' not found in DataFrame.")
                
        df[columnName] = df[columnName].apply(self.clean_text)      
        df[f"{columnName}_tokens"] = df[columnName].apply(self.tokenize_and_stem_text)
        df[f"{columnName}_wordcount"] = df[f"{columnName}_tokens"].apply(len)
        df[f"{columnName}_readability"] = df[columnName].apply(lambda x: textstat.flesch_reading_ease(x)).fillna(0).astype(float)
        df[f"{columnName}_complexity"] = df[columnName].apply(lambda x: textstat.text_standard(x, float_output=True)).fillna(0).astype(float)                

        self.vectorizer.fit(df[f"{columnName}_tokens"].apply(lambda x: ' '.join(x)))        
        self.scaler.fit(df[[f"{columnName}_wordcount", f"{columnName}_readability", f"{columnName}_complexity"]].values)

        return self
    
    def transform(self, df: pd.DataFrame, columnName: str = 'description', return_dense: bool = False):
        """
        Transform the job descriptions into TF-IDF features.
        return_dense: bool = False: If True, return dense array, else sparse matrix.
        """
        if df is None or df.empty:
            raise ValueError("DataFrame is empty or not provided.")
        if columnName not in df.columns:
            raise ValueError(f"Column '{columnName}' not found in DataFrame.")
        
        df[columnName] = df[columnName].apply(self.clean_text)      
        df[f"{columnName}_tokens"] = df[columnName].apply(self.tokenize_and_stem_text)
        df[f"{columnName}_wordcount"] = df[f"{columnName}_tokens"].apply(len)
        df[f"{columnName}_readability"] = df[columnName].apply(lambda x: textstat.flesch_reading_ease(x)).fillna(0).astype(float)
        df[f"{columnName}_complexity"] = df[columnName].apply(lambda x: textstat.text_standard(x, float_output=True)).fillna(0).astype(float)

        d = self.vectorizer.transform(df[f"{columnName}_tokens"].apply(lambda x: ' '.join(x)))        
        d_columns = list(self.vectorizer.get_feature_names_out())
        
        xtra = df[[f"{columnName}_wordcount", f"{columnName}_readability", f"{columnName}_complexity"]].values
        xtra = self.scaler.transform(xtra)

        x = hstack([d, xtra]).tocsr()
        x_columns = d_columns + [f"{columnName}_wordcount", f"{columnName}_readability", f"{columnName}_complexity"]
        
        if return_dense:
            return x.toarray(), x_columns
        
        return x, x_columns

    def fit_transform(self, df: pd.DataFrame, columnName: str = 'description', return_dense: bool = False):
        """
        Fit the TF-IDF vectorizer and transform the job descriptions into TF-IDF features.
        return_dense: bool = False: If True, return dense array, else sparse matrix.
        """
        
        if df is None or df.empty:
            raise ValueError("DataFrame is empty or not provided.")
        if columnName not in df.columns:
            raise ValueError(f"Column '{columnName}' not found in DataFrame.")
        
        self.fit(df, columnName)
        return self.transform(df, columnName, return_dense)
    
    def save_tfidf_vectorizer(self, filename: str):
        """
        Save the TF-IDF vectorizer to a file.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"TF-IDF vectorizer saved to {filename}")        

    def load_tfidf_vectorizer(self, filename: str):
        """
        Load the TF-IDF vectorizer from a file.
        """
        if not filename.endswith('.pkl'):
            raise ValueError("Filename must end with '.pkl'")
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' does not exist.")
        
        with open(filename, 'rb') as f:
            self.vectorizer = pickle.load(f)
        print(f"TF-IDF vectorizer loaded from {filename}")

    def save_scaler(self, filename: str):
        """
        Save the scaler to a file.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"Scaler saved to {filename}")

    def load_scaler(self, filename: str):
        """
        Load the scaler from a file.
        """
        if not filename.endswith('.pkl'):
            raise ValueError("Filename must end with '.pkl'")
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' does not exist.")
        
        with open(filename, 'rb') as f:
            self.scaler = pickle.load(f)
        print(f"Scaler loaded from {filename}")

if __name__ == "__main__":

    df = pd.read_csv('data/job_posting_data.csv')
    df.dropna(inplace=True)  # Drop rows with missing values
    print(f"DataFrame:\n{df.head()}")
    classifier = TextClassifier()
    x, cols = classifier.fit_transform(df, 'description')
    #Uncomment the following line to save the TF-IDF vectorizer to a file
    #classifier.save_tfidf_vectorizer('tfidf_vectorizer.pkl')
    print(f"Preprocessed data shape: {x.shape}")
    #use classifier.fit_transform(df, 'description', return_dense=True) to get dense array
    #if you want to see the dense array, uncomment the following lines
    x_dense, cols = classifier.transform(df, 'description', return_dense=True)    
    print(f"Preprocessed data:\n{x_dense[:5]}")
    
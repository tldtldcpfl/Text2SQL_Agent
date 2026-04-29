# all-minilm base 임베딩 
import warnings
warnings.filterwarnings('ignore')
from sentence_transformers import SentenceTransformer, util
import shutil
import os
import datasets
print(datasets.__version__)
from datasets import load_dataset

# load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

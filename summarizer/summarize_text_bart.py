import torch
import transformers
from transformers import BartTokenizer, BartForConditionalGeneration

torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

def summarize_bart(text):
    article_input_ids = tokenizer.batch_encode_plus([text.replace('\n','')], return_tensors='pt', max_length=1024,truncation=True)['input_ids'].to(torch_device)
    summary_ids = model.generate(article_input_ids,
                              num_beams=4,
                              length_penalty=2.0,
                              max_length=200,
                              min_length=100,
                              no_repeat_ngram_size=3)
    summary_txt = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
    return summary_txt
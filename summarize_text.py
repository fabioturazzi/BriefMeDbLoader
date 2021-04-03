from transformers import pipeline
from rouge import Rouge
import time
from gensim.summarization import summarize

#function to summarize text
def summarize_with_pipeline(text):
    # Initialize the HuggingFace summarization pipeline
    summarizer = pipeline("summarization")
    start_time = time.time()
    text_to_sum = text
    while True:
        try:
            #try bart summarize if the text is not too long
            summarized1 = summarizer(text_to_sum, min_length=100, max_length=200)
            break
        except:
            #if the text is too long, use extractive summary method to reduced the size
            text_to_sum = summarize(text_to_sum, ratio=(0.95))
    #print(text_to_sum)
    end_time = time.time()
    total_time = end_time - start_time

    return summarized1[0]['summary_text'] #, total_time

#function to evaluate summary
def evaluate_summary(my_string, summary):
    # evaluate
    rouge = Rouge()

    #to use rouge, all sentences must be on the same line
    no_line = "".join(my_string.splitlines())
    scores = rouge.get_scores(no_line, summary)
    return scores

# #generate summary (list of dictionary) and time of execution
# summary_dic, time = summarize_with_pipeline(to_tokenize_full)
# #get the summary string
# summary = summary_dic[0]['summary_text']
# print(summary)
# score = evaluate_summary(to_tokenize_full,summary)
# print("ROUGE evaluation: ", score, "in", time)







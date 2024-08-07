#import neccessory libraries
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from transformers import pipeline

import chromedriver_binary
from urllib.request import urlopen
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver as selenium_webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from googletrans import Translator

from io import BytesIO
import base64
from wordcloud import WordCloud 
import matplotlib.pyplot as plt

#flask object
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']

    # Your Selenium code for Twitter search and data collection
    service = webdriver.chrome.service.Service(executable_path=r'C:\Users\amrit\Desktop\kerala_tourism\chromedriver-win64\chromedriver.exe')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get("https://twitter.com/explore")
    driver.maximize_window()
    time.sleep(3)
    username = driver.find_element(By.CLASS_NAME,"r-1dz5y72.r-13qz1uu")     
    # username.click()
    username.send_keys("scrapy632356143")  
    time.sleep(3)                      
    next=driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
    next.click()
    time.sleep(3)
    password = driver.find_element(By.CLASS_NAME,"r-deolkf.r-homxoj ")     
    # password.click()
    password.send_keys("scrapy673002")  
    time.sleep(3)                        
    login=driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
    login.click()
    time.sleep(4)

    explore=driver.find_element(By.XPATH,'//*[@data-testid="AppTabBar_Explore_Link"]')
    explore.click()
    time.sleep(2)

    search_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input'

    # Find the search element and send keys
    search_element = driver.find_element(By.XPATH, search_xpath)
    search_element.send_keys(search_query)
    search_element.send_keys(Keys.ENTER)
    time.sleep(3)

    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1, total_height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(i))
    data= driver.find_elements(By.XPATH,'//*[@data-testid="tweetText"]')
    twit1=[]

    for d in data:
        print(d.text)
        twit1.append(d.text)


    df=pd.DataFrame({'post':twit1})
    # df.to_csv('twitter_data11111111.csv')

    df.to_csv('twitter_data11111111000.csv')

    #translate anotherb langauage to English
    translator = Translator()
    df['post'] = df['post'].apply(lambda x: translator.translate(x, dest='en').text)
    #sentiment analysis using pipeline transformers
    df = df['post']
    nlp_sentence = pipeline('sentiment-analysis')

    def predict_toxicity(comment):
        sentiment = nlp_sentence(comment)
        return sentiment[0]['label']
    def count_toxicity(df):
        positive_count = 0
        negative_count = 0
        for comment in df:
            sentiment = predict_toxicity(comment)
            if sentiment == 'NEGATIVE':
                
                positive_count += 1
            else:
                negative_count += 1
    
        total_comments = positive_count + negative_count
        positive_percentage = (positive_count / total_comments) * 100
        negative_percentage = (negative_count / total_comments) * 100
        return positive_percentage, negative_percentage
    #get the analysis percentage
    positive_percentage_total, negative_percentage_total = count_toxicity(df)
    positive_percentage=(f"Percentage of Positive comments: {positive_percentage_total:.2f}%")
    negative_percentage=(f"Percentage of Negative comments: {negative_percentage_total:.2f}%")
    
    text = df.values 

    # Generate Word Cloud
    wordcloud = WordCloud().generate(str(text))

    # Convert Word Cloud image to base64 to display in HTML
    img = BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()


    # Visualize the results
    
    labels = ['POSITIVE', 'NEGATIVE']
    counts = [positive_percentage_total, negative_percentage_total]

    plt.figure(figsize=(4,3))  # Adjust figure size if needed

    plt.bar(labels, counts)
    plt.title('Positive vs. Negative Twitter Posts')


    # Save plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Convert the plot image to base64 encoding
    img_base64plot = base64.b64encode(img.getvalue()).decode()
    
    plt.close()  # Close the plot to release memory


    return render_template('boot.html', positive_percentage=positive_percentage, negative_percentage=negative_percentage, img_base64=img_base64,img_base64plot=img_base64plot)

if __name__ == '__main__':
    app.run(debug=True)
###############################word cloud generating##############################


# import pandas as pd
# from googletrans import Translator
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud 

# translator = Translator()
# df = pd.read_csv('twitter_data11111111000.csv')

# df['post'] = df['post'].apply(lambda x: translator.translate(x, dest='en').text)
# df = df['post']

# text = df.values 

# wordcloud = WordCloud().generate(str(text))

# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()



##################################flask################################

# ... (Previous Flask code remains the same)

# from io import BytesIO
# import base64

# # ... (Your existing Flask routes)

# @app.route('/wordcloud')
# def generate_wordcloud():
#     # Read the translated Twitter data
#     translator = Translator()
#     df = pd.read_csv('twitter_data11111111000.csv')

#     df['post'] = df['post'].apply(lambda x: translator.translate(x, dest='en').text)
#     df = df['post']

#     text = df.values 

#     # Generate Word Cloud
#     wordcloud = WordCloud().generate(str(text))

#     # Convert Word Cloud image to base64 to display in HTML
#     img = BytesIO()
#     wordcloud.to_image().save(img, format='PNG')
#     img.seek(0)
#     img_base64 = base64.b64encode(img.getvalue()).decode()

#     return render_template('wordcloud.html', img_base64=img_base64)

# if __name__ == '__main__':
#     app.run(debug=True)




####################################html################################################



# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Word Cloud</title>
# </head>
# <body>
#     <h1>Word Cloud</h1>
#     <img src="data:image/png;base64,{{ img_base64 }}" alt="Word Cloud">
# </body>
# </html>






            #     # Generate Word Cloud
            #     wordcloud = WordCloud().generate(str(sentiment))

            #     # Convert Word Cloud image to base64 to display in HTML
            #     img = BytesIO()
            #     wordcloud.to_image().save(img, format='PNG')
            #     img.seek(0)
            #     positive_cloud = base64.b64encode(img.getvalue()).decode()

            #     positive_count += 1
            #     return positive_cloud

            # else:
            #                     # Generate Word Cloud
            #     wordcloud = WordCloud().generate(str(sentiment))

            #     # Convert Word Cloud image to base64 to display in HTML
            #     img = BytesIO()
            #     wordcloud.to_image().save(img, format='PNG')
            #     img.seek(0)
            #     negative_cloud = base64.b64encode(img.getvalue()).decode()

            #     negative_count += 1
            #     return negative_cloud
    
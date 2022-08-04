import os

from flask import Flask, request, redirect, url_for, render_template, session, after_this_request, jsonify
from utils import get_base_url, dict_to_str, fetch_transcript
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled,  VideoUnavailable # doesn't work

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 5000
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url + 'static')


app.secret_key = os.urandom(64)


def summarize(transcript):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    

    #apply dict2str func from util.py
    text = dict_to_str(transcript)
    print(text)
    output = summarizer(text, max_length=130, min_length=30, do_sample=False)
    #get the unprocessed data from session, name it with data\
    string_output = ''
    print(output)
    for i in output:
        string_output += i['summary_text']
    return string_output

# set up the routes and logic for the webserver
@app.route(f'{base_url}')
def home():
    return render_template('index.html')



#Transcript scraping
@app.route(f'{base_url}/scraping/', methods=["POST"])
def scraping():

    video_id = request.form['prompt']
    
    transcript = YouTubeTranscriptApi.get_transcript(video_id)


    print(transcript)
    #returning to the result page for update
    return redirect(url_for('home'))



# TEST
@app.route('/response', methods=['GET', 'POST'])
def response():
    # this is a test function, the data should be exactly like summary variable
    @after_this_request
    def add_header(res):
        res.headers.add('Access-Control-Allow-Origin', '*')
        return res

    if request.method == 'POST':
        video_id = request.get_json()['data'] # string video id 
    
    transcript = fetch_transcript(video_id)
    summarized_transcript = summarize(transcript)
    print(type(summarized_transcript))
    summary = [{"time": 95, "summary" : summarized_transcript}]

    # time here is second, easy to convert from datetime 
    # summary = [{"time": 95, "summary": "Trump ordered a travel ban on citizens from several Muslim-majority countries, diverted military funding towards building a wall on the U.S.–Mexico border, and implemented a policy of family separations for apprehended migrants. He signed the Tax Cuts and Jobs Act of 2017, which cut taxes for individuals and businesses and rescinded the individual health insurance mandate penalty of the Affordable Care Act. He appointed 54 federal appellate judges and three United States Supreme Court justices. In foreign policy, Trump initiated a trade war with China and withdrew the U.S. from the proposed Trans-Pacific Partnership trade agreement, the Paris Agreement on climate change, and the Iran nuclear deal. Trump met with North Korean leader Kim Jong-un three times, but made no progress on denuclearization. He reacted slowly to the COVID-19 pandemic, ignored or contradicted many recommendations from health officials in his messaging, and promoted misinformation about unproven treatments and the need for testing. "},
    #            {"time": 211, "summary": "Trump is the only president in American history to have been impeached twice. After he pressured Ukraine to investigate Biden in 2019, he was impeached by the House of Representatives for abuse of power and obstruction of Congress in December. The Senate acquitted him of both charges in February 2020. The House of Representatives impeached Trump a second time in January 2021, for incitement of insurrection. The Senate acquitted him in February, after he had already left office. Following his presidency, Trump has remained heavily involved in the Republican Party, including through fundraisers and by making over 140 political endorsements. Scholars and historians rank Trump as one of the worst presidents in American history."}]
    return jsonify(summary) # always return JSON data !!


# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = ''

    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)



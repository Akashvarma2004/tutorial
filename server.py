# from flask import Flask, request, jsonify
# import tweepy
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# from flask_cors import CORS
# import os


# app = Flask(__name__)
# CORS(app)

# # Twitter API setup
# BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # Replace with your actual bearer token
# CONSUMER_KEY = os.getenv("CONSUMER_KEY")
# CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
# client = tweepy.Client(
#     bearer_token=BEARER_TOKEN,
#     consumer_key=CONSUMER_KEY,
#     consumer_secret=CONSUMER_SECRET,
#     access_token=ACCESS_TOKEN,
#     access_token_secret=ACCESS_TOKEN_SECRET
# )

# # Fetch the latest tweets from a user
# def fetch_latest_tweets(username, max_results=10):
#     try:
#         response = client.get_user(username=username)
#         if not response.data:
#             return {"error": "User not found"}, 404

#         user_id = response.data.id
#         tweets = client.get_users_tweets(
#             id=user_id,
#             max_results=max_results,
#             tweet_fields=["created_at", "text"],
#         )
#         if not tweets.data:
#             return {"error": "No tweets found for this user"}, 404

#         return {"tweets": [tweet.text for tweet in tweets.data]}, 200
#     except tweepy.TweepyException as e:
#         return {"error": f"Tweepy Error: {e}"}, 500
#     except Exception as ex:
#         return {"error": f"Unexpected Error: {ex}"}, 500

# # Summarize tweets using a pre-trained model
# def summarize_tweets(tweets, model_name="t5-small"):
#     try:
#         tokenizer = AutoTokenizer.from_pretrained(model_name)
#         model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
#         input_text = "Summarize the following tweets into a single post:\n" + "\n".join(tweets)
#         inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
#         summary_ids = model.generate(
#             inputs.input_ids,
#             max_length=150,
#             num_beams=5,
#             early_stopping=True
#         )
#         summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#         return {"summary": summary}, 200
#     except Exception as ex:
#         return {"error": f"Error in summarization: {ex}"}, 500

# # API to fetch tweets
# @app.route("/api/fetch_tweets", methods=["GET"])
# def fetch_tweets_api():
#     username = request.args.get("username")
#     if not username:
#         return jsonify({"error": "Username is required"}), 400
#     result, status = fetch_latest_tweets(username)
#     return jsonify(result), status

# # API to summarize tweets
# @app.route("/api/summarize", methods=["POST"])
# def summarize_api():
#     data = request.json
#     if not data or "tweets" not in data:
#         return jsonify({"error": "Tweets data is required"}), 400
#     result, status = summarize_tweets(data["tweets"])
#     return jsonify(result), status

# # Run the Flask server
# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, request, jsonify, render_template, send_from_directory
import tweepy
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask_cors import CORS
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# Twitter API setup
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Fetch the latest tweets from a user
def fetch_latest_tweets(username, max_results=10):
    try:
        response = client.get_user(username=username)
        if not response.data:
            return {"error": "User not found"}, 404

        user_id = response.data.id
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=max_results,
            tweet_fields=["created_at", "text"],
        )
        if not tweets.data:
            return {"error": "No tweets found for this user"}, 404

        return {"tweets": [tweet.text for tweet in tweets.data]}, 200
    except tweepy.TweepyException as e:
        return {"error": f"Tweepy Error: {e}"}, 500
    except Exception as ex:
        return {"error": f"Unexpected Error: {ex}"}, 500

# Summarize tweets using a pre-trained model
def summarize_tweets(tweets, model_name="t5-small"):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        input_text = "Summarize the following tweets into a single post:\n" + "\n".join(tweets)
        inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = model.generate(
            inputs.input_ids,
            max_length=150,
            num_beams=5,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return {"summary": summary}, 200
    except Exception as ex:
        return {"error": f"Error in summarization: {ex}"}, 500

# Serve the frontend
@app.route("/")
def index():
    return render_template("index.html")

# API to fetch tweets
@app.route("/api/fetch_tweets", methods=["GET"])
def fetch_tweets_api():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400
    result, status = fetch_latest_tweets(username)
    return jsonify(result), status

# API to summarize tweets
@app.route("/api/summarize", methods=["POST"])
def summarize_api():
    data = request.json
    if not data or "tweets" not in data:
        return jsonify({"error": "Tweets data is required"}), 400
    result, status = summarize_tweets(data["tweets"])
    return jsonify(result), status

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True)

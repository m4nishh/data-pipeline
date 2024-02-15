from flask import Flask, request, jsonify
import threading
import text_processing as tp
import scraper as scraper
import scraper.landing_crawl as landing_crawl
import chatgpt as cg
from app import main

app = Flask(__name__)

@app.route('/greet')
def index():
  return 'Hello brandos!'
  
@app.route('/get-keywords', methods= ["POST"])
def get_keywords():
  body = request.data.decode("utf-8")
  if not body:
        return jsonify(isError= True,
                    message= "Bad request",
                    statusCode= 422,
                    data= "request body should have text"), 422
  input = body.splitlines()
  try:
    kw_set = tp.process_text(input_keywords=input)
    kw_list = ", ".join(list(kw_set))
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data= kw_list), 200
  except Exception as e:
    return jsonify(isError= True,
                    message= "Failed",
                    statusCode= 500,
                    data= str(e)), 500

@app.route('/generate', methods= ["POST"])
def generate_article():
  body = request.data.decode("utf-8")
  if not body:
        return jsonify(isError= True,
                    message= "Bad request",
                    statusCode= 422,
                    data= "request body should have text"), 422
  input = body.split(',')
  try:
    article = cg.create_content(keywords=input)
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data= article), 200
  except Exception as e:
    return jsonify(isError= True,
                    message= "Failed",
                    statusCode= 500,
                    data= str(e)), 500

@app.route('/sitemap-urls', methods= ["GET"])
def sitemap_urls():
  website = request.data.decode("utf-8")
  if not website:
        return jsonify(isError= True,
                    message= "Bad request",
                    statusCode= 422,
                    data= "request body should have text"), 422
  try:
    urls = scraper.get_end_urls_from_sitemap(robots=website+"/robots.txt")
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data= urls), 200
  except Exception as e:
    return jsonify(isError= True,
                    message= "Failed",
                    statusCode= 500,
                    data= str(e)), 500

@app.route('/landing-urls', methods= ["GET"])
def landing_urls():
  website = request.data.decode("utf-8")
  if not website:
        return jsonify(isError= True,
                    message= "Bad request",
                    statusCode= 422,
                    data= "request body should have text"), 422
  try:
    urls = landing_crawl.get_l1_urls(landing_page=website)
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data= urls), 200
  except Exception as e:
    return jsonify(isError= True,
                    message= "Failed",
                    statusCode= 500,
                    data= str(e)), 500
  
def serve():
  threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()
  main()

serve()
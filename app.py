from flask import Flask, render_template
import asyncio
from src.main import get_filtered_comments

app = Flask(__name__)

@app.route("/")
def index():
    # Run the async function in the event loop
    filtered_comments = asyncio.run(get_filtered_comments())
    return render_template("jobs.html", jobs=filtered_comments)

if __name__ == "__main__":
    app.run(debug=True)
from pymongo import MongoClient

client = MongoClient()
db = client.myopenmic
videos = db.videos

from flask import Flask, render_template

app = Flask(__name__)

# # OUR MOCK ARRAY OF PROJECTS
# videos = [
#     { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
#     { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
# ]


@app.route('/')
def videos_index():
    """Show all videos."""
    return render_template('videos_index.html', videos=videos.find())


@app.route('/videos/new')
def videos_new():
    """Create a new video."""
    return render_template('videos_new.html', video={}, title='New video')

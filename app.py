from pymongo import MongoClient

client = MongoClient()
db = client.myopenmic
videos = db.videos

from flask import Flask, render_template, request, redirect, url_for

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

app.route('/videos', methods=['POST'])
def videos_submit():
    """Submit a new video."""
    video = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split(),
        'created_at': datetime.now()
    }
    print(video)
    video_id = videos.insert_one(video).inserted_id
    return redirect(url_for('videos_show', video_id=video_id))

@app.route('/videos/<video_id>')
def videos_show(video_id):
    """Show a single video."""
    video = videos.find_one({'_id': ObjectId(video_id)})
    video_comments = comments.find({'video_id': ObjectId(video_id)})
    return render_template('videos_show.html', video=video, comments=video_comments)

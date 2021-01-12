import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/myopenmic')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
videos = db.videos
comments = db.comments


app = Flask(__name__)

@app.route('/About')
def videos_index():
    """Show all videos."""
    return render_template('videos_index.html', videos=videos.find())

@app.route('/')
def about():
    """Create About page"""
    return render_template('About.html')

@app.route('/videos/new')
def videos_new():
    """Create a new video."""
    return render_template('videos_new.html', video={}, title='New video')

@app.route('/videos', methods=['POST'])
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

@app.route('/videos/<video_id>/edit')
def videos_edit(video_id):
    """Show the edit form for a video."""
    video = videos.find_one({'_id': ObjectId(video_id)})
    return render_template('videos_edit.html', video=video, title='Edit video')

@app.route('/videos/<video_id>', methods=['POST'])
def videos_update(video_id):
    """Submit an edited video."""
    updated_video = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    videos.update_one(
        {'_id': ObjectId(video_id)},
        {'$set': updated_video})
    return redirect(url_for('videos_show', video_id=video_id))

@app.route('/videos/<video_id>/delete', methods=['POST'])
def videos_delete(video_id):
    """Delete one video."""
    videos.delete_one({'_id': ObjectId(video_id)})
    return redirect(url_for('videos_index'))

########## COMMENT ROUTES ##########

@app.route('/videos/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'video_id': ObjectId(request.form.get('video_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('videos_show', video_id=request.form.get('video_id')))

@app.route('/videos/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('videos_show', video_id=comment.get('video_id')))

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

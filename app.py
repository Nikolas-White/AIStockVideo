pip install flask flask_sqlalchemy boto3

from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import boto3
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
app.config['UPLOAD_FOLDER'] = './uploads'
db = SQLAlchemy(app)

# S3 Configuration (Optional)
s3 = boto3.client('s3')

# Database Model
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    tags = db.Column(db.String(500), nullable=False)

# Upload video and tags
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded'}), 400

    video = request.files['video']
    tags = request.form.get('tags')
    
    if video and tags:
        filename = secure_filename(video.filename)
        video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save metadata to database
        new_video = Video(filename=filename, tags=tags)
        db.session.add(new_video)
        db.session.commit()

        return jsonify({'message': 'Video uploaded successfully!'}), 201
    else:
        return jsonify({'error': 'Missing video or tags'}), 400

# Search videos by tags
@app.route('/search', methods=['GET'])
def search_videos():
    search_term = request.args.get('q')
    if not search_term:
        return jsonify({'error': 'No search term provided'}), 400

    results = Video.query.filter(Video.tags.contains(search_term)).all()
    video_list = [{'filename': video.filename, 'tags': video.tags} for video in results]
    return jsonify(video_list), 200

# Download video
@app.route('/download/<filename>', methods=['GET'])
def download_video(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

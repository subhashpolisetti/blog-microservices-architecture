from flask import Flask, request, jsonify, abort
from models import User, Post

app = Flask(__name__)

# User routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.get_all_users()
    return jsonify(users)

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.get_user_by_id(id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@app.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    email = request.json['email']
    User.create_user(name, email)
    return jsonify({'status': 'User created'}), 201

# Post routes
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.get_all_posts()
    return jsonify(posts)

@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.get_post_by_id(id)
    if post is None:
        abort(404)

    # Get user info for the post
    user = User.get_user_by_id(post['user_id'])
    user_data = user if user else {'error': 'User not found'}
    post['user'] = user_data
    return jsonify(post)

@app.route('/posts', methods=['POST'])
def create_post():
    title = request.json['title']
    content = request.json['content']
    user_id = request.json['user_id']
    Post.create_post(title, content, user_id)
    return jsonify({'status': 'Post created'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

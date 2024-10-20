from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock data for posts
posts = []

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/posts', methods=['GET'])
def get_posts():
    logger.info(f"Retrieved {len(posts)} posts")
    return jsonify(posts)

@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = next((post for post in posts if post['id'] == id), None)
    if post is None:
        logger.info(f"Post with id {id} not found")
        return jsonify({'error': 'Post not found'}), 404

    # Get user info from the User Service
    user_service_url = os.getenv('USER_SERVICE_URL', 'http://user-service:5002')
    try:
        user = requests.get(f'{user_service_url}/users/{post["user_id"]}')
        user.raise_for_status()
        user_data = user.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching user data: {str(e)}")
        user_data = {'error': 'User not found'}

    post['user'] = user_data
    logger.info(f"Retrieved post with id {id}")
    return jsonify(post)

@app.route('/posts', methods=['POST'])
def create_post():
    try:
        title = request.json['title']
        content = request.json['content']
        user_id = request.json['user_id']
        new_post = {
            'id': len(posts) + 1,
            'title': title,
            'content': content,
            'user_id': user_id
        }
        posts.append(new_post)
        logger.info(f"Created new post: {title} by user {user_id}")
        return jsonify({'status': 'Post created', 'post': new_post}), 201
    except KeyError as e:
        logger.error(f"Missing field in create post request: {str(e)}")
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Error creating post: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)

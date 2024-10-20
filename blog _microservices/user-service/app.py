from flask import Flask, request, jsonify
from models.models import User
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.get_all_users()
        logger.info(f"Retrieved {len(users)} users")
        return jsonify(users)
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.get_user_by_id(id)
        if user is None:
            logger.info(f"User with id {id} not found")
            return jsonify({'error': 'User not found'}), 404
        logger.info(f"Retrieved user with id {id}")
        return jsonify(user)
    except Exception as e:
        logger.error(f"Error retrieving user {id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/users', methods=['POST'])
def create_user():
    try:
        name = request.json['name']
        email = request.json['email']
        User.create_user(name, email)
        logger.info(f"Created new user: {name}, {email}")
        return jsonify({'status': 'User created'}), 201
    except KeyError as e:
        logger.error(f"Missing field in create user request: {str(e)}")
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

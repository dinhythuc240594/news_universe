"""
Main application file - initialization for Flask app và register routes
"""
from dotenv import load_dotenv
from flask import Flask, request

from config import envConfig
from database import init_db

from client_routes import client_bp
from admin_routes import admin_bp

load_dotenv()  # Load varibale enviroment from file .env

def create_app():
    """
    Factory function to create Flask application
    
    Args:
        envConfig: Class contain config for enviroment
        
    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(envConfig)

    # initialization database
    init_db()

    app.register_blueprint(client_bp)
    app.register_blueprint(admin_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*50)
    print("  Website News - Flask Server")
    print("="*50)
    print(f"  Server to run: http://localhost:5000")
    print(f"  Home: http://localhost:5000/")
    print(f"  Admin: http://localhost:5000/admin/login")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)

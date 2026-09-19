import os
from backend.app import create_app

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    print(f"\n==========================================================")
    print(f" MediCare Smart Healthcare Platform Starting")
    print(f" Local Web Server: http://{host}:{port}")
    print(f" REST API Health:  http://{host}:{port}/api/health")
    print(f"==========================================================\n")
    app.run(host=host, port=port, debug=True)

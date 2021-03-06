from api.app import create_app
from config import ApiConfig

app = create_app(ApiConfig)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

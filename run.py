from data_inpi import create_app
from dotenv import load_dotenv

load_dotenv(".flaskenv")

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

import psycopg2, os, dotenv

dotenv.load_dotenv()

connection = psycopg2.connect(
    database="devdevdb",
    host=os.getenv("POSTGRES_HOST"),
    user=os.getenv("POSTGRES_USERNAME"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("POSTGRES_PORT")
)
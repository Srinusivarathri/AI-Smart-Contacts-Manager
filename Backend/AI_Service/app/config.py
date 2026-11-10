import os
from dotenv import load_dotenv

load_dotenv()

CONTACTS_SERVICE_URL=os.getenv("CONTACTS_SERVICE_URL","http://localhost:5002")
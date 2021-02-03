# Celestial

Setup:
1. Download python
2. Use git bash to clone the repo
3. Clone the gihub repo
- in git bash: git clone https://github.com/Primdahl26/Celestial
4. Setup and activate virtualenv:
- in git bash:
python -m venv venv
- in git bash:
source venv/scripts/activate

first command creates virtual env and second enables

5. Install the requirments using git bash
- in git bash:
pip install -r req.txt
6. Finally run the application
- in git bash:
python run.py
7. You can now connect to the wesite on your localhost: 
- http://localhost:1337

IMPORTANT!
- To run the app - create a .env file containing the API key in the following format:

THE_MOVIE_DB_API_KEY={API_KEY}
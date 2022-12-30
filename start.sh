echo "Cloning Repo...."
git clone https://github.com/mdiskrequestbot/mdiskrequestbot.git /mdiskrequestbot
cd /mdiskrequestbot
pip3 install -r requirements.txt
echo "Starting Bot...."
python3 main.py

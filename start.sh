echo "Cloning Repo...."
git clone https://github.com/mdiskrequestbot/mdiskrequestbot.git /MdiskrequestBot
cd /MdiskrequestBot
pip3 install -r requirements.txt
echo "Starting Bot...."
python3 main.py

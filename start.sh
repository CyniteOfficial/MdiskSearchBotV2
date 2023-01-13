echo "Cloning Repo...."
git clone https://github.com/Goodnightmovies/MdiskSearchBotV2.git /goodnightmoviesBotV2
cd /goodnightmoviesBotV2
pip3 install -r requirements.txt
echo "Starting Bot...."
python3 main.py

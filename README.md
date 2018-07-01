# adi-zar
Web testing with selenium
# Requirements
- Ubuntu 16.04, Desktop or server edition does not matter
- Docker 18.03.1-ce, build 9ee9f40 ([instructions](https://docs.docker.com/install/linux/docker-ce/ubuntu/))
- docker-compose version 1.21.2, build a133471 (instructions below)
- Python 3.6 or higher
- git

# Install instructions
#### docker-compose
You have to download the binary, change it to execute and (optional) move it somewhere in the PATH 
```bash
wget https://github.com/docker/compose/releases/download/1.21.2/docker-compose-Linux-x86_64
chmod 744 /usr/local/bin/docker-compose
sudo mv docker-compose-Linux-x86_64 /usr/local/bin/docker-compose
```

# Run instructions
### Run selenium grid instructions for Ubuntu
- clone this repository
```bash
git clone https://github.com/nichitapavel/adi-zar
```
- change directory to repository
```bash
cd adi-zar/
```
- run docker containers  
This will run on foreground, to stop it press CTRL + C.  
The first time it will take a while until Selenium Grid is ready, this is because is downloading
docker images from the docker hub, how fast will it do it depends on your internet speed.
```bash
docker-compose up
```
- visit selenium hub console  
optionaly you can visit the selenium hub page when docker compose is done, take your computer ip
(command line: `ip a`), open a browser and go to `http://<your computer ip>:4444/grid/console`

### Run the client with tests
This part actually can be done from any OS, steps can vary.
- create a virtual environment for your the tests and activate it
```bash
sudo apt update
sudo apt install python3-venv
python3 -m venv .venv
. .venv/bin/activate
```
- install pip packages
```bash
pip install -r requirements.txt
``` 
- IMPORTANT: update the config.json to match your setup, otherwise it won't work 100%
- run the tests
```bash
pytest
```
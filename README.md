# Cole's Pokemon Skill  
### Introduction
An Amazon Alexa skill written in Python 3 and utilizing flask-ask.  The script was inspired by the game 'Let's Go Pikachu' and is used to allow my son to get specific Pokemon information (e.g. vulnerabilities) easily from his Echo Dot device.

The script greets the user and asks them to provide the name of a Pokemon to hear about.  A lookup is then performed on the website [https://pokemon.gameinfo.io/](https://pokemon.gameinfo.io/), utilzing the built-in Pokemon dictionary.  

>New or larger dictionaries can be easily created using code from the following gist:
	[https://gist.github.com/mikepitagno/6c9681bf1188eddc3db49f36d712c361](https://gist.github.com/mikepitagno/6c9681bf1188eddc3db49f36d712c361)  
	
Finally, the data is parsed and returned to the user via Alexa.  

Several python modules are required for the application to run successfully.  The Flask server need to be accessible on the public Internet for Amazon to reach it.  If this is not possible, a tool like ngrok can be used for establishing a secure tunnel to the web server running on your localhost.
### Installation Notes / Prerequisites
#### Python Modules:
**lxml**
	pip3 install lxml

*Note: depends libxml2-dev and libxslt1-dev packages; Debian/Ubuntu Install: sudo apt install libxml2-dev libxslt1-dev
*
**requests**
	pip3 install requests

**flask and flask-ask**
	pip3 install flask 
	pip3 install flask-ask

#### Flask Server Layout:
>pi@pi-lego:~ $ tree --dirsfirst /home/pi/FLASK  
/home/pi/FLASK  
└── POKEMON  
    ├── templates  
    │   └── main.html  
    ├── pokemon_skill.py3  
    └── templates.yaml  

>2 directories, 3 files

#### ngrok:
>pi@pi-lego:~/NGROK $ unzip ngrok-stable-linux-arm.zip
Archive:  ngrok-stable-linux-arm.zip
  inflating: ngrok   
  
>pi@pi-lego:~/NGROK $ ./ngrok authtoken <Auth Token Code> 
Authtoken saved to configuration file: /home/pi/.ngrok2/ngrok.yml  

>pi@pi-lego:~/NGROK $ ./ngrok http 5000

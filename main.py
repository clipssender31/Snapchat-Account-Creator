import httpx, random, string,os,pyfiglet, ctypes; from pypasser import reCaptchaV3 as solver; from concurrent.futures import ThreadPoolExecutor; from itertools import cycle; from random_user_agent.user_agent import UserAgent;from random_user_agent.params import SoftwareName, OperatingSystem


def menu():
    print(pyfiglet.figlet_format(f"Clips SnapCreator"))
    print("Author: clipssender#2920")
    ctypes.windll.kernel32.SetConsoleTitleW("Clips SnapCreator | Created by clipssender#2920 | .gg/p9fGBAHa | github.com/clipssender31")

    
def random_pass():
    return ''.join([random.choice(string.digits + string.ascii_letters) for i in range(16)])


class bcolors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


CreatedAccs=0
FailedAccs=0
def GetProxy():
    with open('./Data/Proxies.txt', 'r') as temp_file:
        proxy = [line.rstrip('\n') for line in temp_file]
    return proxy


proxy = GetProxy()

proxy_pool = cycle(proxy )


def GetProxies():
    proxy = next(proxy_pool)
    if len(proxy.split(':')) == 4:
        splitted = proxy.split(':') 
        return f"http://{splitted[2]}:{splitted[3]}@{splitted[0]}:{splitted[1]}" # Converts ip:port:user:pass format to user:pass@ip:port
    return f'http://{proxy}'


#def check_username(): whole function just for checking usernames but got slow so I just resorted to using the same code in the main function, it made things faster.
    

def register():
    global CreatedAccs
    global FailedAccs
    while True:
        try:
            software_names = [SoftwareName.CHROME.value]
            operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
            user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
            proxy = {"http": f"{GetProxies}"}
            user_agent = user_agent_rotator.get_random_user_agent()
            randompass=''.join([random.choice(string.digits + string.ascii_letters) for i in range(8)])
            client = httpx.Client(
                headers={
                'Accept-Encoding':'gzip',
                'Accept-Language': 'en-US;q=1',
                'Accept': 'application/json',
                'Connection': 'keep-alive',
                'uaser-agent': f"{user_agent}"},
                proxies=GetProxies(), 
                timeout=30
                )

            name="".join([random.choice(string.digits + string.ascii_letters) for i in range(10)])
            client.get('https://accounts.snapchat.co/accounts/signup?client_id=ads-apireferrer=https%253A%252F%252Fads.snapchat.com%252Fgetstarted&ignore_welcome_email=true')
            xsrfff_token=client.cookies['xsrf_token']
            checkuser=client.post('https://accounts.snapchat.com/accounts/get_username_suggestions', data={'requested_username': f'{name}', 'xsrf_token': xsrfff_token})

            if checkuser.json()['reference']['status_code'] == 'OK':
                print(f'{bcolors.RED}[USERNAME]{bcolors.RESET} {bcolors.MAGENTA}Username is available: {bcolors.GREEN}{name}{bcolors.RESET}')
            else:
                print(f'{bcolors.RED}[USERNAME]{bcolors.RESET} {bcolors.RED}Username is taken: {bcolors.GREEN}{name}{bcolors.RESET}.{bcolors.RED} Trying again...{bcolors.RESET}')
                continue

            randomd = "".join([random.choice(string.digits + string.ascii_letters) for i in range(10)])

            xtoken=client.get('https://accounts.snapchat.co/accounts/signup?client_id=ads-api&referrer=https%253A%252F52Fads.snapchat.com%252Fgettarted&ignre_welcome_email=true') #get new xsrf token
            xsrf_token=client.cookies['xsrf_token']
            if xtoken.status_code==200:  
                print(f'{bcolors.RED}[XSRF]{bcolors.RESET} {bcolors.BLUE}Got xsrf Token: {xsrf_token}{bcolors.RESET}')

            data={
            'flrst_name': 'Mick', 
            'last_name': 'Shumacher', 
            'userame': f"{name}", 
            'pasword': f'{randompass}', 
            'birthday': '2000-01-31', 
            'email': f'{randomd}@gmail.com',
            'xsrf_token': xsrf_token, 
            'g-recaptcha-rsponse': solver("https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LezjdAZAAAAAD1FaW81QpkkplPNzCNnIOU5anHw&co=aHR0cHM6Ly9hY2NvdW50cy5zbmFwY2hhdC5jb206NDQz&hl=en&v=M-QqaF9xk6BpjLH22uHZRhXt&size=invisible&badge=inline&cb=9qlf8d10oqh9", proxy),
            'client_id': 'ads-api', 
            'referrer': 'https://ads.snapchat.com/getstarted', 
            'ignore_welcome_email': 'false'}


            res=client.post('https://acounts.snapchat.co/acconts/register', data=data)

            if res.status_code==200:
                print(f'{bcolors.RED}[GENERATOR]{bcolors.RESET} {bcolors.GREEN}Account created: {name}:{randompass}{bcolors.RESET}')
                with open('Out/Accounts.txt', 'a') as f:
                    f.write(f'{name}:{randompass}\n')
                    f.close()
            else:
                print(f'{bcolors.RED}[GENERATOR]{bcolors.RESET} {bcolors.RED}Account not created: {name}. Trying again...{bcolors.RESET}')
                register()
        except Exception as e:
            print(f'An error has occured: {e}')
if __name__ == "__main__":
    os.system("cls")
    
    menu()
    
    threadAmount=input(f'{bcolors.RED}Thread Amount: {bcolors.RESET}')
    
    threadAmount = 1 if threadAmount == "" else int(threadAmount)
    threads = []
    
    with ThreadPoolExecutor(max_workers=threadAmount) as reg:  

        for x in range(threadAmount):

            reg.submit(register)

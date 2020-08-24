import requests

class VRV9519BWAC23:
    target = 'http://192.168.1.254'

    def __init__(self):
        self.session = requests.Session()
    
    def usr_signin(self, pwd):
        # Send authentication data
        self.session.post(url=f'{self.target}/cgi-bin/login.cgi', data={ 'pws': pwd })
    
    def usr_signed(self):
        data = self.session.get(url=self.target + '/html/lan_device_table.stm').text.splitlines()
        return False if 'Alice' in data else True # Ty Alice <3

    def usr_signout(self):
        self.session.cookies.clear()
    
    def devices(self):
        devices = []

        # Validate session
        if not self.usr_signed(): self.usr_signin()

        # Read devices
        data = self.session.get(url=self.target + '/html/lan_device_table.stm').text.splitlines()

        # Filter data
        name, addr, mac, conn = None, None, None, None
        for line in data:
            if line.startswith('connect_name') and '"' in line:
                name = line.split('"')[1]
            if line.startswith('connect_ipv4') and '"' in line:
                addr = line.split('"')[1]
            if line.startswith('connect_mac') and '"' in line:
                mac = line.split('"')[1]
            if line.startswith('connect_status') and '"' in line:
                conn = ( True if line.split('"')[1] == 'Active' else False )
                devices.append({ 'name': name, 'address': addr, 'mac': mac, 'connected': conn })

        return devices

    def log(self):
        messages = []

        # Validate session
        if not self.usr_signed(): self.usr_signin()

        # Read token
        r = self.session.get(url=self.target + '/html/system_log.stm')
        lines = r.text.splitlines()

        # Extract LOG data
        firstLine = False
        idMsg, timestamp, typeMsg, level, msg = None, None, None, None, None
        for line in lines:
            if firstLine:
                if line == '':
                    firstLine = False

            if firstLine:
                if line.startswith('id'):
                    idMsg = int(line.split('=\'')[1][:1])
                if line.startswith('timestamp'):
                    timestamp = line.split('=\'')[1][:-2].replace('.', '-')
                if line.startswith('type'):
                    typeMsg = int(line.split('=\'')[1][:1])
                if line.startswith('level'):
                    level = int(line.split('=\'')[1][:1])
                if line.startswith('message'):
                    msg = line.split('=\'')[1][:-2]
                    messages.append({ 'id': idMsg, 'timestamp': timestamp, 'type': typeMsg, 'level': level, 'msg': msg })

            if line == 'var message = new Array();':
                firstLine = True

        return messages
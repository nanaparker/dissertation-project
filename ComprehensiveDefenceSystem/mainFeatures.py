import os
import re
import time
import socket
import hashlib
import win32con
import requests
import platform
import win32file
import concurrent.futures
import mysql.connector as sql


# -------------------------------------------------DATABASE CLASS-------------------------------------------------------
class mySQL:
    def __init__(self, ip):
        try:
            self.conn = sql.connect(user='remoteUser', password='myFINALpr3s3nt@t10n', database="thesisDB", host=ip, port=3306, auth_plugin='caching_sha2_password')
            self.cursor = self.conn.cursor()
            print(self.conn)
        except:
            self.__init__(ip)

    def conn(self):
        print(self.conn)

    def login(self, user, pwd):
        hash_pwd = hashlib.sha256(pwd.encode()).hexdigest()
        query = "SELECT * FROM thesisDB.Users where Email = %s and Password = %s"
        self.cursor.execute(query, (user, hash_pwd))
        log_result = self.cursor.fetchone()
        if log_result == None:
            return [0, None]
        else:
            return [1, log_result[0]]
            
        
    def settingsRetrieval(self, user):
        query = f"SELECT * FROM thesisDB.Settings where UserID = '{user}'"
        self.cursor.execute(query)
        settings_row = self.cursor.fetchone()
        return settings_row
    
    def settingsUpdate(self, user, set1=0, set2=0, set3=0):
        query = f"UPDATE thesisDB.Settings SET Set_1 = {int(set1)}, Set_2 = {int(set2)}, Set_3 = {int(set3)} WHERE UserID = '{user}'"
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return 1
        except:
            print("Unable to Update")
            return 0



# -------------------------------------------------ANTI-VIRUS CLASS-------------------------------------------------------
class AV:
    # Here the virus signatures are downloaded and stored in a variable
    def __init__(self):
        self.results = []
        self.retrieveSignatures()
        self.malHashes = open("virusSignatures.bav", "r")
        self.read_malHashes = self.malHashes.readlines()
        self.malHashes.close()
        self.realTime = []


    #--------------------------------------------DETECTION--------------------------------------------------
    # retrieveSignatures: Download the virus signatures
    def retrieveSignatures(self):
        link = "https://raw.githubusercontent.com/anic17/Batch-Antivirus/master/VirusDataBaseHash.bav"
        r = requests.get(link, stream=True)
        if r.ok:
            with open("virusSignatures.bav", 'wb') as file:
                for x in r:
                    file.write(x)
        else:
            pass
    

    # md5_hash: returns the sha hash of a provided file
    def sha_hash(self, file):
        if os.path.getsize(file) > 30000000:
            return -1

        try:
            with open(file, "rb") as f:
                bytes = f.read()
                hash = hashlib.sha256(bytes).hexdigest()
                f.close()
            return hash
        except PermissionError:
            pass
    

    # malHashDetection: compares the hash of a file against the virus signatures
    def malHashDetection(self, filePath):
        try:
            hashCheck = self.sha_hash(filePath)

            for f in self.read_malHashes:
                if f.split(':')[0] == hashCheck:
                    return "Malicious Item: " + f.split(':')[1] + " Scanned File: " + filePath
            return 0
        except PermissionError:
            pass


    # folderScan: Performing a thorough scan on the provided folder, placing the
    #             discovered files in a list, and breaking that list into chunks
    def folderScan(self, dir):
        dir_list = list()

        for dirPath, _, filename in os.walk(dir):
            dir_list += [os.path.join(dirPath, file) for file in filename]

        n = int(len(dir_list)/100)
        final = [dir_list[i * n:(i + 1) * n] for i in range((len(dir_list) + n - 1) // n )]
        return final


    # threadCreator: Here, threads are created to handle the list derived from the
    #                folderScan function. Each sublist is sent to loadDistribution
    #                as an argument
    def threadCreator(self, items):
        try:
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=len(items))
            pool_array = []

            for item in items:
                t = pool.submit(self.loadDistribution, item) 
                pool_array.append(t)

            time.sleep(0.02)    

        except PermissionError:
            pass


    # loadDistribution: Here, the sublists sent from threadCreator are further broken down
    #                   and sent to malwareHashDetection as file paths for the detection to
    #                   take place
    def loadDistribution(self, item):
        for var in item:
            result = self.malwareChecker(var)
            if result != 0:
                self.results.append(result)


    # reportCard: This function presents the results derived after the execution of all other
    #             functions
    def reportCard(self):
        time.sleep(2)
        if len(self.results) > 0:
            return self.results
        else:
            return "No malware detected!"


    # scanning: This function performs the entire signature-based detection once run
    def scanning(self, dir):
        directory_list = self.folderScan(dir)
        self.threadCreator(directory_list)
        return self.reportCard()


    def malwareChecker(self, filePath):
        hash_malware = self.sha_hash(filePath)

        malwareHash = open("VirusDataBaseHash copy.bav", "r")
        read_malwareHash = malwareHash.read()
        malwareHash.close()

        if read_malwareHash.find(hash_malware) != -1:
            return "Malware found at " + filePath
        else:
            return 0



# ------------------------------------------VULNERABILITY SCANNER CLASS---------------------------------------------
class VScanner:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())

    def pre_portScan(self):
        print("------------------------PORT SCAN------------------------")
        self.portScanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.portScanner.settimeout(10)

        ports = []
        self.open_port = []
        for i in range(1,1024):
            ports.append(i)

        sublists = [ports[i:i + 256] for i in range(0, len(ports), 256)]



        pool = concurrent.futures.ThreadPoolExecutor(max_workers=8)
        pool_array = []
        count = 0
        for sub in sublists:
            t = pool.submit(self.scanning, sub) 
            pool_array.append(t)

        time.sleep(0.02)

    def scanning(self, items):
        for item in items:
            if not self.portScanner.connect_ex((self.host, item)):
                self.open_port.append(item)
            else:
                pass
            time.sleep(0.02)


    def reportCard(self):
        time.sleep(300)
        if len(self.open_port) > 0:
            return self.open_port
        else:
            return [0]
        
    def portScan(self):
        self.pre_portScan()
        return self.reportCard()


    # This section is responsible for discovering information about the System's OS and provide feedback
    def osDetection(self):
        print("------------------------OS INFO DETECTION------------------------")
        device_props = platform.uname()
        eol = self.retrieveEOL(device_props[0].lower(), device_props[3])
        return [device_props[0], device_props[2], device_props[3], eol]


    def retrieveEOL(self, system, version):
            link = "https://endoflife.date/api/"+system+".json"
            try:
                request = requests.get(link)
                if request.status_code == 200:
                    response = request.json()
                    for resp in response:
                        if resp['latest'] == version:
                            return resp['eol']
            except:
                self.retrieveEOL(system, version)


    def dir_spaces(self):
        print("------------------------DIRECTORY WHITESPACE DETECTION------------------------")
        space_list = []
        for a , _, _ in os.walk("C:\\Users\\" + os.environ.get('USERNAME')):
            if bool(re.search(r"\s", a)):
                space_list.append(a)
            
        return space_list

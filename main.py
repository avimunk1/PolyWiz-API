# This is a sample Python script.

import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import date
from datetime import datetime
from datetime import time

cTime = datetime.now()
cTime = cTime.strftime("%H:%M:%S")
print("Current Time =", cTime)
cDate = str(date.today())
print("datetiime=", cDate)
cDtaeTme = str(cDate) + str(cTime)
data: str = ""


class polwizApi:

    def __init__(self,client_id):
        self.config = get_cofig()
        self.base_url = "https://polywizz.com/api/"
        self.un = self.config["un"]
        self.up = self.config["up"]
        print("config set user name =",self.un)
        self.client_id: int = client_id
        self.company_id = 1
        self.session_id:str = ""

    def login_to_personal(self, company_id):
        self.company_id = company_id
        session_id = -1
        print("login with", self.client_id, self.company_id)
        header = {"content-type": "application/json"}
        url = self.base_url + "/login_personal_area/?client_id={}&company_id={}".format(self.client_id, company_id)
        response = requests.get(url, auth=HTTPBasicAuth(self.un, self.up), headers=header, verify=True)
        writeLog("OTP request with user id {} to company {} http status={}".format(self.client_id, company_id,response.status_code))
        print("otp requested from companyid",company_id)
        if response.status_code == 200:
            self.session_id = response.json()["session_id"]
            print("otp request status ={} and session id={}".format(response.status_code,self.session_id))
        else:
            print("login failled with status", response.status_code, self.un, self.up,response.text)
            exit()
        return response.status_code

    def feed_otp(self,smsCode):
        client_id = self.client_id
        company_id = self.company_id

        userInfo = {
            "company_id": "{}".format(self.company_id),
            "sms_code": smsCode,
            "session_id":self.session_id,
            "client_id": self.client_id}
        header = {"content-type": "application/json"}
        url = self.base_url + "feed_otp_personal_area/"
        response = requests.post(url, data=json.dumps(userInfo), auth=HTTPBasicAuth(self.un, self.up), headers=header, verify=True)
        writeLog("login to personal data with user id {} to company {} http status={}".format(client_id,company_id,response.status_code))
        #print("JD=", json.dumps(userInfo))
        if response.status_code == 200:print(response.status_code, response.content)
        else: print("feed OTP failed with status", response.status_code, response.content)
        return response.status_code

    def getDataAsZip(self): # this will download a copy of the actual policy
        print("starting DAZIP")
        OutFileName = "files/DataasZip{}.zip".format(self.client_id)
        print("get data as zip with", self.client_id)
        header = {"content-type": "application/json"}
        url = self.base_url+ "/get_data_as_zip/?client_id={}".format(self.client_id)
        response = requests.get(url, auth=HTTPBasicAuth(self.un, self.up), headers=header, verify=True)
        writeLog("downloading policy with user id {} http status={}".format(self.client_id,response.status_code))
        if response.status_code == 200:
            with open(OutFileName, "wb") as code:
                code.write(response.content)
            print("download zip ready", response.status_code)
        else:
            print("download zip failled with status", response.status_code)
            exit()
        return response.status_code

    def download_reports(self):
        client_id = self.client_id
        base_url = self.base_url
        un = self.un
        up = self.up
        OutFileName = "files/downloadReports{}.xlsx".format(client_id)
        print("download reports with c_Id", client_id)
        header = {"content-type": "application/json"}
        url = base_url + "download_report/ ?client_id={}&download_format=excel&report_sections =policy".format(client_id)
        response = requests.get(url, auth=HTTPBasicAuth(un, up), headers=header, verify=True)
        if response.status_code == 200:
            writeLog("download report successfully downloaded as {}".format(OutFileName))
            with open(OutFileName,"wb") as code:
                code.write(response.content)
                code.close()
            print("download har data ready", response.status_code,response.content)
        else:
            print("download har data zip failled with status", response.status_code, response.content, un, up)
            writeLog("download report failed with status {}".format(response.status_code))
            exit()
        return response.status_code

    def get_har_data(self):
        client_id = self.client_id
        base_url = self.base_url
        un = self.un
        up = self.up
        OutFileName = "files/har{}.zip".format(client_id)
        print("get_har_data with", client_id)
        header = {"content-type": "application/json"}
        url = base_url + "get_har_data/?client_id={}&download_format=zip".format(client_id)
        response = requests.get(url, auth=HTTPBasicAuth(un, up), headers=header, verify=True)
        if response.status_code == 200:
            writeLog("har data successfully downloaded as {}".format(OutFileName))
            with open(OutFileName, "wb") as code:
                code.write(response.content)
                code.close()
            print("download har data ready", response.status_code)
        else:
            print("download har data zip failled with status", response.status_code, response.content,un, up)
            writeLog("har data failed with status {}".format(response.status_code))
            exit()
        return response.status_code


def createClient():
    base_url = "https://polywizz.com/api/"
    config = get_cofig()
    un = config["un"]
    up = config["up"]
    client_id = -1
    userInfo = {
        "first_name": "אבי",
        "last_name": "מונק",
        "phone": "0543330652",
        "id_number": "022026587",
        "id_issuing_date": "2013-07-14"}
    header = {"content-type": "application/json"}
    url = base_url + "create_client/"
    response = requests.post(url, data=json.dumps(userInfo), auth=HTTPBasicAuth(un, up), headers=header, verify=True)
    if response.status_code == 200:
        client_id = response.json()["client_id"]
        data = "client id {} created".format(client_id)
        writeLog(data,newlog=True)
    else:
        print("request failed with status code", response.status_code, response.json()["detail"])
        data = ("request failed with status code".format(response.status_code))
        writeLog(data,newlog=True)
    return client_id

def writeLog(data,newlog=False):
    cTime = datetime.now()
    cTime = cTime.strftime("%H:%M:%S")
    cDate = str(date.today())
    cDtaeTme = str(cDate) + str(cTime)
    if newlog:line = "newSession:\ndate:{}  {} data:{}\n".format(cDate, cTime, data)
    else:line = "date:{}  {} data:{}\n".format(cDate, cTime, data)
    logfilename = "logs/" + str(cDate) + ".txt"
    file = open(logfilename, 'a')
    file.write(line)
    file.close()

def get_cofig():
    path = "/Users/avimunk/PycharmProjects/config/polwiz/"
    configFileName = "Poywiz_Config.json"
    file = open(path + configFileName, 'r')
    data = file.read()
    obj = json.loads(data)
    return obj

def main():
    #myCompanies = [1, 2, 5]
    myCompanies = [2]
    getHarData: bool = True
    runLogin = False
#ido C_id 548974
    client_id = 559707
    if not client_id:
        client_id = createClient()  # create client in PW
        print("new client created", client_id)
    retryCounter = 0
    instance = client_id
    instance=polwizApi(client_id)
    if getHarData: g_har_data = instance.get_har_data()
    #company_id = input("companyid")
    if runLogin:
        for c in myCompanies:
            company_id = c
            getSMSstatus = instance.login_to_personal(company_id) # get OTP
            smsCode = input("code")
            login = instance.feed_otp(smsCode) # login with OTP
            if login != 200 and retryCounter == 0:
                login = instance.feed_otp(smsCode)
                retryCounter = 1
            print("response login = ",login)

    dazip = instance.getDataAsZip()
    DR = instance.download_reports()

if __name__ == '__main__':
    main()

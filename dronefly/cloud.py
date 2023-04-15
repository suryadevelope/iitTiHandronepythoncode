import __main__

import pyrebase
from dronekit import connect, VehicleMode, LocationGlobalRelative
from getmac import get_mac_address
# Python Imports
import time
# import stream

import vehicleinfo
from datetime import datetime


import json

dictionary ={}

def writetofile(dir1):
    with open("dronefly/cred.json", "w") as outfile:
        jsonString = json.dumps(dictionary)
        outfile.write(jsonString)
        outfile.close()


time_in_utc = datetime.utcnow()
formatted_time_in_utc = time_in_utc.strftime("%d/%m/%Y %H:%M:%S")

frame_count =0

macaddress = get_mac_address().upper()
print(macaddress)

firebaseConfig = {
  'apiKey': "AIzaSyCuUifAzJuGIfWzn-_rehNl9cnFov04zvM",
  'authDomain': "drug-delivery-5fab8.firebaseapp.com",
  'databaseURL': "https://drug-delivery-5fab8-default-rtdb.firebaseio.com",
  'projectId': "drug-delivery-5fab8",
  'storageBucket': "drug-delivery-5fab8.appspot.com",
  'messagingSenderId': "992844257605",
  'appId': "1:992844257605:web:c53b5b5f4e3a22f069062c",
  'measurementId': "G-RBMZBFCQLQ"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
ignorecloud = {}
ignorecloud["status"] = 0

def Cloudint():
 

    #retrive data

    
    daltitude = db.child("device/"+macaddress+"/altitude").get().val()
    dcl = db.child("device/"+macaddress+"/dcl").get().val()
    ddl = db.child("device/"+macaddress+"/ddl").get().val()
    dinfo = db.child("device/"+macaddress+"/dinfo").get().val()
    ddrive = db.child("device/"+macaddress+"/drive").get().val()
    Dstatus = db.child("device/"+macaddress+"/Dstatus").get().val()
    QRid = db.child("device/"+macaddress+"/id").get().val()
    vconnect = db.child("device/"+macaddress+"/vconnect").get().val()
    vrtlmode = db.child("device/"+macaddress+"/rtl").get().val()
    confirm_delivery = db.child("device/"+macaddress+"/confirm_delivery").get().val()

    if daltitude == None:
        db.child("device/"+macaddress+"/altitude").set("0")
        db.child("device/"+macaddress+"/dcl").set("0,0")
        db.child("device/"+macaddress+"/ddl").set("0,0")
        db.child("device/"+macaddress+"/dinfo").set("null")
        db.child("device/"+macaddress+"/drive").set(0)
        db.child("device/"+macaddress+"/Dstatus").set(["ONLINE",formatted_time_in_utc])
        db.child("device/"+macaddress+"/id").set("null")
        db.child("device/"+macaddress+"/vconnect").set(0)
        db.child("device/"+macaddress+"/rtl").set(0)
        dictionary["altitude"] = "0"
        dictionary["dcl"] = "0,0"
        dictionary["ddl"] = "0,0"
        dictionary["dinfo"] = "null"
        dictionary["drive"] = 0
        dictionary["id"] = "null"
        dictionary["vconnect"] = 0
        dictionary["confirm_delivery"] = 0
        dictionary["rtl"] = 0
        dictionary["Dstatus"] = ["ONLINE",formatted_time_in_utc]
        time.sleep(0.2)
    else:
        dictionary["altitude"] = daltitude
        dictionary["dcl"] = dcl
        dictionary["ddl"] = ddl
        dictionary["dinfo"] = dinfo
        dictionary["drive"] = ddrive
        dictionary["id"] = QRid
        dictionary["vrtl"] = vrtlmode
        dictionary["vconnect"] = vconnect
        dictionary["confirm_delivery"] = confirm_delivery
        dictionary["Dstatus"] = Dstatus
    print(vconnect)
    if int(vconnect)==1:
        db.child("device/"+macaddress+"/vconnect").set(0)
        vconnect = 0
        dictionary["vconnect"] = vconnect

    if int(ddrive )== 1:
        db.child("device/"+macaddress+"/drive").set(0)
        ddrive = 0
        dictionary["drive"] = ddrive

    if int(vrtlmode) == 1:
        db.child("device/"+macaddress+"/rtl").set(0)
        dictionary["vrtl"] = 0
    if int(confirm_delivery)==1:
        db.child("device/"+macaddress+"/confirm_delivery").set(0)
        dictionary["confirm_delivery"] = 0


    time.sleep(1)
    if str(Dstatus[0]) == "OFFLINE":
        db.child("device/"+macaddress+"/Dstatus").set(["ONLINE",formatted_time_in_utc])
        Dstatus[0] = "ONLINE"
        Dstatus[1] = formatted_time_in_utc
        dictionary["Dstatus"] = Dstatus
        time.sleep(0.2)
        

    if daltitude != None:
       
        def stream_handler(message):
            # print(message["event"]) # put
            print(message["path"]) # /-K7yGTTEp7O549EzTYtI
            # print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
            
            if ignorecloud["status"] == 0:
                if message["path"] == "/altitude":
                    daltitude = message["data"]
                    dictionary["altitude"] = daltitude

                # elif message["path"] == "/dcl":
                #     dcl = message["data"]
                #     __main__.__updatefromcloud("dcl",dcl)
                elif message["path"] == "/ddl":
                    ddl = message["data"]
                    dictionary["ddl"] = ddl

                elif message["path"] == "/confirm_delivery":
                    dcon = message["data"]
                    dictionary["confirm_delivery"] = dcon
                elif message["path"] == "/drive":
                    ddrive = message["data"]
                    dictionary["drive"] = ddrive

                elif message["path"] == "/id":
                    qrcodeid = message["data"]
                    dictionary["id"] = qrcodeid
                elif message["path"] == "/rtl":
                    vrtlmode = message["data"]
                    dictionary["vrtl"] = vrtlmode

                elif message["path"] == "/Dstatus/0":
                    Dstatus = message["data"]
                    if str(Dstatus) == "OFFLINE":
                        __cloudupload("Dstatus",["ONLINE",formatted_time_in_utc])
                    dictionary["Dstatus"] = ["ONLINE",formatted_time_in_utc]

                elif message["path"] == "/vconnect":
                    vconnect = message["data"]
                    if int(vconnect) == 0:
                        __cloudupload("vconnect",1)
                        dictionary["vconnect"] = 1

                writetofile(dictionary)                

            else:
                ignorecloud["status"]=0
                dictionary["status"] = 0

                writetofile(dictionary)
            
        my_stream = db.child("device/"+macaddress).stream(stream_handler)
    # stream.streamfetchdata("cloudqrid",QRid)
    writetofile(dictionary)
    return [daltitude,dcl,ddl,ddrive,QRid,vrtlmode]

    ############################INIT DEVICE#####################################

def __cloudupload(path,data):
    if firebase:
        ignorecloud["status"] = 1
        db.child("device/"+macaddress+"/"+path).set(data)
        dictionary[path] = data
        writetofile(dictionary)
        ignorecloud["status"] = 0
        time.sleep(2)
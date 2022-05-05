# UDPPingerClient.py
# We will need the following module to generate randomized lost packets
from base64 import decode
from email import header, message
from http import client
from logging import exception, raiseExceptions
from re import A
import sys
import socket

from numpy import byte

# Create a UDP socket
UDP_IP_ADDRESS = "10.77.13.251"   #10.77.47.75    127.0.0.1  10.77.36.208 10.77.13.251
UDP_PORT_NO = 42069   #12000   #42069
Message = bytes()
bufferSize= 100
# create a socket with a 1s timeout.
clientSock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clientSock.connect((UDP_IP_ADDRESS,UDP_PORT_NO))  #12000 42069

clientSock.settimeout(1)

MessageTypeAck= 0
MessageTypeHello=1
MessageRequestId=2
MessageRequestList=3
MessageListResponse=4
MessageRecipeResponse=5
MessageGoodbye=6
MessageError=7
MessageNotFound=8



messagecounter = 0 
messagecounter+=1




def calculateChecksum(buffer:bytes):
    lrc = 0
    for b in buffer:
        lrc = (lrc + b) & 0xFF
    lrc = (((lrc ^ 0xFF) + 1) & 0xFF)
    return lrc


def Yes(buffersize:int):
    return buffersize.to_bytes(4,'big')

def No(buffersize:int):
    return buffersize.to_bytes(4,'big')

def Header(MessageNumber: int,MessageType,NumberOfParts,ProgressOfMessage,Checksum,Data):

    header = bytearray(MessageNumber.to_bytes(1, 'big')
    +MessageType.to_bytes(1,'big')
    +NumberOfParts.to_bytes(1,'big')  # the 1 is the number of bytes
    +ProgressOfMessage.to_bytes(1,'big')
    +(0).to_bytes(4, 'big')
    + Data)

    check = calculateChecksum(header)

    header[4] = check
    #print(header)
    
    return bytes(header)


def RequestId(MessageNumber: int,MessageType,NumberOfParts,ProgressOfMessage,Checksum,Data):
    
    requestid = bytearray(MessageNumber.to_bytes(1, 'big')
    +MessageType.to_bytes(2,'big')
    +NumberOfParts.to_bytes(1,'big')  # the 1 is the number of bytes
    +ProgressOfMessage.to_bytes(1,'big')
    +Checksum.to_bytes(1,'big')
    +(0).to_bytes(3, 'big')
    + Data)
     
    return bytes(requestid)




#def Fields(MessageNumber: int,MessageType, NumberOfParts, Checksum)






def decode(data:bytes):
    dataA = bytearray(data)
    header = dataA[0:8]
    messagenumber = header[0]
    messagetype = header[1]
    numberofparts = header[2]
    progressofmessage = header[3]
    checksum = header[4]
    dataR = bytes(dataA[8:]) 


    dataA[4] = 0


    if checksum != calculateChecksum(bytes(dataA)):
            raise Exception


    return(messagenumber,messagetype,numberofparts,progressofmessage,'''Checksum''',dataR)




def HelloHeader(buffersize:int):
    return buffersize.to_bytes(4,'big')

def RequestId(buffersize:int):
    return buffersize.to_bytes(4, 'big')

while (True):


    packet = clientSock.send(Header(1,1,1,1,0,HelloHeader(1024)))
    
   
    #hello_packet = clientSock.send(Header(1,1,1,1,0,HelloHeader(1024)))
    
    # sent1 = clientSock.send(RequestId(1))
    #sent = clientSock.send(Header(1,MessageTypeAck,1,1,0,Message))



    #welcomeFromServer = clientSock.recvfrom(1024)
    #print(welcomeFromServer)


    #Get message from server and print it
    #print('test')
    msgFromServer = clientSock.recvfrom(1024)
    try:
        decodedmessage = decode(msgFromServer[0])
        #server_size = int.from_bytes(server_hello, 'big')
        server_hello = "Message from Server {}".format(decodedmessage[5])
        print(server_hello)
    except:
        print('The Checksum failed and the program will now close')
        quit()


    # clientSock.send(Header(1,1,1,1,0,b'Hello Back'))

    while (True):
        choice = input('Would you like to request a recipe? Type Yes or No to say Goodbye\n')
        try:
                if choice != 'Yes' and choice != 'No':
                    raise Exception ('Please type Yes or No (Case-sensitive)')
                else: 
                    if choice == 'Yes':
                    # clientSock.send(Yes(1024))
                        #choice, address = clientSock.recvfrom(1024)
                        #print(choice.decode('UTF-8'))

                        
                            header2 = Header(1, MessageRequestList,1,1, 0, bytes())
                            #print(header2)
                            clientSock.send(header2)
                            #Get message from server and print it
                            msgFromServer = clientSock.recvfrom(1024)                    
                            try:
                                
                                decodedmessage = decode(msgFromServer[0])
                                server_hello = decodedmessage[5].decode()
                                print(server_hello)

                            except:
                                print('The Checksum failed and the program will now close')
                                quit()


                        
                            # I want to request a recipe list type yes or type no to quit 
                            choice2 = input("ID:")
                            if choice2 != '1' or choice2 != '2' or choice2 != '3' or choice2 != '4' or choice2 != '5':
                                print(' Not Found :(')
                            header3 = Header(2,MessageRequestId,1,1,0,choice2.encode())
                            clientSock.send(header3)

                        
                            #Get message from server and print it
                            
                            
                            #decodedmessage = decode(msgFromServer[0])
                            #print(msgFromServer)
                            msgFromServer = clientSock.recvfrom(1024)
                            decodedmessage = decode(msgFromServer[0])

                         
                            #print(decodedmessage[5].decode())
                            
                            result = bytearray(decodedmessage[5]) 

                        
                            
                            if  decodedmessage[2] > 1:
                                while decodedmessage[2] != decodedmessage[3]:
                                    clientSock.send(Header(2,0,1,decodedmessage[3],0,bytes()))
                                    msgFromServer2 = clientSock.recvfrom(1024)
                                    decodedmessage = decode(msgFromServer2[0])
                                    #print (decodedmessage[5].decode())
                                    result += decodedmessage[5]
                                    
                                #decodedmessage = decode(msgFromServer)
                                #print(decodedmessage)
                                clientSock.send(Header(2,0,1,decodedmessage[3],0,bytes()))

                            print(result.decode())
                            try:
                                    decodedmessage = decode(msgFromServer[0])
                                    server_hello = decodedmessage[5].decode()
                                    #print(server_hello)
                            except:
                                    print('The Checksum failed and the program will now close')
                                    quit()

                    

                
        except Exception as error:
                        print(error)









        if choice == 'No':
                    goodbye_packet = Header(3,MessageGoodbye,1,1,0,bytes())
                    clientSock.send(goodbye_packet)
                    #msgFromServer, _ = clientSock.recvfrom(1024)
                    #decodedmessage = decode(msgFromServer)
                    print('Goodbye')
                    quit()
                    
        
        #clientSock.send(Header(0, MessageGoodbye,1,1,0,bytes()))
        #choice,address =clientSock.recvfrom(1028)
        #print(choice.decode('UTF-8'))
    #str(decodedmessage)
    #print(str(decodedmessage))





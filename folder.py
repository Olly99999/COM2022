#import folder

from pkg_resources import EGG_DIST

#from client import calculateChecksum



def calculateChecksum(buffer:bytes):
    lrc = 0
    for b in buffer:
        lrc = (lrc + b) & 0xFF
    lrc = (((lrc ^ 0xFF) + 1) & 0xFF)
    return lrc

def MessageGoodbye(buffersize:int):
    return buffersize.to_bytes(4,'big')
    
def Header(MessageNumber: int,MessageType,NumberOfParts,ProgressOfMessage,Checksum,Data):

    header = bytearray(MessageNumber.to_bytes(1, 'big')
    +MessageType.to_bytes(1,'big')
    +NumberOfParts.to_bytes(1,'big')  # the 1 is the number of bytes
    +ProgressOfMessage.to_bytes(1,'big')
    #+Checksum.to_bytes(1,'big')
    +(0).to_bytes(4, 'big')
    + Data)

    check = calculateChecksum(header)
    header[4] = check
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


def HelloHeader(buffersize:int):
    return buffersize.to_bytes(4,'big')

def decode(data:bytes):
    dataA = bytearray(data)
    header = dataA[0:8]
    messagenumber = header[0]
    messagetype = header[1]
    numberofparts = header[2]
    progressofmessage = header[3]
    checksum = header[4]
    dataR = bytes(dataA[8:]) 


    return(messagenumber,messagetype,numberofparts,progressofmessage,checksum,dataR)


MessageTypeAck= 0
MessageTypeHello=1
MessageRequestId=2
MessageRequestList=3
MessageListResponse=4
MessageRecipeResponse=5
MessageGoodbye=6
MessageError=7
MessageNotFound=8

'''This messages sends the list of recipes and the server internal ids for those recipes.
This message must the list the recipes in the format:
ID:name
Different ID, name pairs must be separated by a new line character, so a message with
3 ids must be formatted as:
ID1:name1\nID2:name2\nID3:name3
And this text data should be encoded as UTF-8.'''


recipes = {
 1:'Roast Chicken',
 2:'Burger',
 3:'Paella',
 4:'Sushi',
 5:'Steak'
}

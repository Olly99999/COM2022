# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
from audioop import add
from base64 import encode
import random
from socket import *
from tabnanny import check
from typing_extensions import Self

from grpc import server
from folder import MessageRecipeResponse
from folder import MessageRequestList
from folder import MessageGoodbye
#from client import MessageListResponse
from folder import Header, HelloHeader, MessageRequestId, MessageTypeHello, RequestId,decode,MessageListResponse,MessageGoodbye
#from client import Header, HelloHeader, MessageRequestId, MessageTypeHello, RequestId,decode

#

recipes = {
 1:'Roast Chicken',
 2:'Burger',
 3:'Paella',
 4:'Sushi',
 5:'Steak'
}

str1 ="Choose a number between 1-5: \n 1:'Roast Chicken', 2:'Burger', 3:'Paella', 4:'Sushi', 5:'Steak'"
recipestring = str1


multilinestring1= '''STEP 1
Heat oven to 190C/fan 170C/gas 5. Have a shelf ready in the middle of the oven without any shelves above it.

STEP 2
Scatter 1 roughly chopped onion and 2 roughly chopped carrots over the base of a roasting tin that fits the whole 1 ½ kg chicken, but doesn’t swamp it.

STEP 3
Season the cavity of the chicken liberally with salt and pepper, then stuff with 2 lemon halves and a small bunch of thyme, if using.

STEP 4
Sit the chicken on the vegetables, smother the breast and legs all over with 25g softened butter, then season the outside with salt and pepper.

STEP 5
Place in the oven and leave, undisturbed, for 1 hr 20 mins – this will give you a perfectly roasted chicken. To check, pierce the thigh with a skewer and the juices should run clear.

STEP 6
Carefully remove the tin from the oven and, using a pair of tongs, lift the chicken to a dish or board to rest for 15-20 mins. As you lift the dish, let any juices from the chicken pour out of the cavity into the roasting tin.

STEP 7
While the chicken is resting, make the gravy. Place the roasting tin over a low flame, then stir in 1 tbsp flour and sizzle until you have a light brown, sandy paste.

STEP 8
Gradually pour in 250ml chicken stock, stirring all the time, until you have a thickened sauce.

STEP 9
Simmer for 2 mins, using a wooden spoon to stir, scraping any sticky bits from the tin.

STEP 10
Strain the gravy into a small saucepan, then simmer and season to taste. When you carve the bird, add any extra juices to the gravy.'''

multilinestring2= '''Step 1. I would suggest preparing a day ahead before grilling. Blend the sirloin chuck, brisket, and short rib ground beef, then mix with some egg. Patty into 8 oz patties and then refrigerator for 24 hours before using; this will help the patties stay together and won’t come apart as you are grilling them.

Step 2. Ensure the grill is scorching hot before putting the patties on the grill. Now season the patties with salt and pepper and add a little oil. Make sure to roll the sides of the patties to season them with salt and pepper thoroughly.

Step 3. Look for the hottest part of the grill, and place the burger patties on the grill. It usually occupies about 2/3 of the top of the grill. The real secret is to move the patties as little as possible once you place the burger patties on the grill. Make sure burgers are at room temperature for 10 minutes before grilling.

Step 4. Begin preparing or presenting the burger buns as the burgers are cooking. Season the buns with salt and pepper, and crisp them on both sides on the grill.

Step 5. Season the thick-sliced onions with some salt and pepper. Add some oil and place onions on the grill as the buns and burgers cook.

Step 6. Grill each burger patty for 3 1/2 to 4 minutes on both sides. Now start basting your patties by brushing them on each side. It is just about two minutes before they are taken off the grill to add some more flavor.
Step 7. Thirty seconds before the patties come off the grill, you need to season the patties again. Then add your jack cheese to the patties to melt while the burgers are still on the grill.

Step 8. Before taking the burger patties off the grill, set up the Brioche buns with a mustard mayo blend, lettuce, and tomatoes. First, you start by placing a tablespoon full of mustard mayo blend on both sides of the top and bottom of the bun. Then gently fold the lettuce to fit onto the bun and press down on the lettuce, making sure it stays folded.

Step 9. After the mustard mayo blend and lettuce, add a thick slice of tomato on top of the lettuce, season the tomato with salt and pepper, and add a dab of more mayo.
Step 10. Add the burgers on each of the present dressed Brioche buns. Place the grilled onions on top of each patty; finish by placing the top bun.'''

multilinestring3='''STEP 1
Heat the olive oil in a large frying pan or wok. Add the onion and soften for 5 mins.

STEP 2
Add the smoked paprika, thyme and paella rice, stir for 1 min, then splash in the sherry, if using. Once evaporated, stir in the chopped tomatoes and chicken stock.

STEP 3
Season and cook, uncovered, for about 15 mins, stirring now and again until the rice is almost tender and still surrounded with some liquid.

STEP 4
Stir in the seafood mix and cover with a lid. Simmer for 5 mins, or until the seafood is cooked through and the rice is tender. Squeeze over the lemon juice, scatter over the parsley and serve with the lemon wedges.'''

multilinestring4= '''STEP 1
KIDS the writing in bold is for you. ADULTS the rest is for you. TO MAKE SUSHI ROLLS: Pat out some rice. Lay a nori sheet on the mat, shiny-side down. Dip your hands in the vinegared water, then pat handfuls of rice on top in a 1cm thick layer, leaving the furthest edge from you clear.

STEP 2
Spread over some Japanese mayonnaise. Use a spoon to spread out a thin layer of mayonnaise down the middle of the rice.

STEP 3
Add the filling. Get your child to top the mayonnaise with a line of their favourite fillings – here we’ve used tuna and cucumber.

STEP 4
Roll it up. Lift the edge of the mat over the rice, applying a little pressure to keep everything in a tight roll.

STEP 5
Stick down the sides like a stamp. When you get to the edge without any rice, brush with a little water and continue to roll into a tight roll.

STEP 6
Wrap in cling film. Remove the mat and roll tightly in cling film before a grown-up cuts the sushi into thick slices, then unravel the cling film.

STEP 7
TO MAKE PRESSED SUSHI: Layer over some smoked salmon. Line a loaf tin with cling film, then place a thin layer of smoked salmon inside on top of the cling film.

STEP 8
Cover with rice and press down. Press about 3cm of rice over the fish, fold the cling film over and press down as much as you can, using another tin if you have one.

STEP 9
Tip it out like a sandcastle. Turn block of sushi onto a chopping board. Get a grown-up to cut into fingers, then remove the cling film.

STEP 10
TO MAKE SUSHI BALLS: Choose your topping. Get a small square of cling film and place a topping, like half a prawn or a small piece of smoked salmon, on it. Use damp hands to roll walnut-sized balls of rice and place on the topping.

STEP 11
Make into tight balls. Bring the corners of the cling film together and tighten into balls by twisting it up, then unwrap and serve.'''


multilinestring5='''STEP 1
Generously season the steaks all over with salt, then press them down slightly with the palm of your hand so they’re roughly the same thickness. Heat the butter in a heavy-based frying pan over a medium-high heat until foaming, then add the thyme so it crackles and sizzles. Add the steaks and use tongs to turn them every 1 min over the course of 6 mins (for very rare), 8 mins (rare) or 10 mins (medium). This helps build an even crust on both sides. Remove the steaks to a warm plate and leave to rest while you make the sauce.

STEP 2
Scatter the pepper over the butter and thyme already in the pan. Toast for 1 min, then stir in the shallots and cook for another minute until they start to soften. Turn the heat up to high and tilt the pan so the side is against the flame (if using a gas hob). Carefully splash in the brandy. Flambé the shallots until the flames have died down.

STEP 3
Reduce the heat to medium and stir in the mustard and Worcestershire sauce. Bubble for a minute, then pour in the stock. Bring to the boil and cook for 2 mins until reduced by half. Stir in the crème fraîche and simmer until rich and creamy. Taste and add more salt if needed. Scoop out the thyme sprig, then return the steaks and any juices to the pan, spooning the sauce over the steaks. Sprinkle over the tarragon, if using. Bring the steaks to the table in the pan and serve drizzled with more sauce.'''

def RequestId(MessageNumber: int,MessageType,NumberOfParts,ProgressOfMessage,Checksum,Data):
    
    requestid = bytearray(MessageNumber.to_bytes(1, 'big')
    +MessageType.to_bytes(2,'big')
    +NumberOfParts.to_bytes(1,'big')  # the 1 is the number of bytes
    +ProgressOfMessage.to_bytes(1,'big')
    +Checksum.to_bytes(1,'big')
    +(0).to_bytes(3, 'big')
    + Data)
     
    return bytes(requestid)
   









# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('10.77.36.208', 42069))








while True:
	
    
 
    #welcomeMessage= str.encode("Hello my dudes, this is the Recipe sharing protocol")
    
    

    
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024) # recvfrom is buffersize
    # Capitalize the message from the client
    
    decodedmessage = decode(message)

    bf = int.from_bytes(decodedmessage[5][0:4], 'big')
    buffersize = bf - 50

    messagenumber = 0
    len(multilinestring1)
    len(multilinestring1)/buffersize
    messageparts = int(len(multilinestring1)/buffersize)


    serverSocket.sendto((Header(1,1,1,1,0,HelloHeader(1024))),address)

    
    myintx = 0
    myintx+=1
    decodedmessage = decode(message)
    #decodedmessage1,decodedmessage2,decodedmessage3,decodedmessage4,decodedmessage5,decodedmessage6 = decodedmessage

    def calculateChecksum(buffer:bytes):
        lrc = 0
        for b in buffer:
            lrc = (lrc + b) & 0xFF
        lrc = (((lrc ^ 0xFF) + 1) & 0xFF)
        return lrc
    check = calculateChecksum
    while (True):  #recipes1=decode(recipes)
    #print('234')
        message, _ = serverSocket.recvfrom(1024)#
        decodedmessage = decode(message)
        #print('3423')
        #print(decodedmessage)
        if decodedmessage[1] == MessageRequestList:
            t = ""
            for a in recipes.keys():
                t += f"{a}:{recipes[a]}\n"
                
        
            serverSocket.sendto(Header(1,4,1,1,0,t.encode()),address)
        
        if decodedmessage[1] == MessageRequestId:
            decodedmessage = decode(message)
            print ('er')
            print(decodedmessage[5].decode())
            if decodedmessage[5].decode() == '1' or  decodedmessage[5].decode() == 'Roast Chicken':
                if decodedmessage[2] < messageparts:
                    multilinestring1
                    print(messageparts)
                    serverSocket.sendto(Header(decodedmessage[0],5,messageparts,1,0,multilinestring1[0:buffersize].encode()),address)
                    print('test')
                    #message, _ = serverSocket.recvfrom(1024)
                    #decodedmessage = decode(message)
                    print('test2')
                    print(decodedmessage)
                    myint = 0
                    myint2 = 1
                    while (True) :
                        myint2+= 1
                        myintx+= 1
                        message, _ = serverSocket.recvfrom(1024)
                        decodedmessage = decode(message)
                        print(decodedmessage)
                        print('test meme',myint, messageparts,myint2,myintx, myint2 >= messageparts)
                        if decodedmessage[0] == 0:
                            myint+= 1

                        
                        if myint2 > messageparts:
                            print('meme2')
                            break
                        serverSocket.sendto(Header(decodedmessage[0],5, messageparts,myint2,0,multilinestring1[buffersize*myintx:(myintx+1)*buffersize].encode()),address)
                    print(decodedmessage)
            else:
                if decodedmessage[1] != '1' or decodedmessage[1] != '2' or decodedmessage[1] != '3' or decodedmessage[1] !='4' or decodedmessage[1]!= '5' or decodedmessage[1]!= 'Roast Chicken' or decodedmessage[1]!= 'Burger' or decodedmessage[1]!= 'Paella' or decodedmessage[1]!= 'Sushi' or decodedmessage[1]!= 'Steak':
                    serverSocket.sendto(Header(messagenumber,8,1,1,0,bytes()),address)
            
        


                ''' if decodedmessage[5].decode() == '2' or  decodedmessage[5].decode() == 'Burger':
                            if decodedmessage[2] < messageparts:
                                multilinestring1
                                print(multilinestring1[0:1024])
                                print(messageparts)
                                serverSocket.sendto(Header(decodedmessage[0],5,messageparts,1,0,multilinestring2[0:buffersize].encode()),address)
                                print('test')
                                message, _ = serverSocket.recvfrom(1024)
                                decodedmessage = decode(message)
                                print('test2')
                                print(decodedmessage)
                                if decodedmessage[1] == 0:
                                    myint = 0
                                    myint2 = 1
                                    while (True) :
                                        myint2+= 1
                                        myintx+= 1
                                        message, _ = serverSocket.recvfrom(1024)
                                        decodedmessage = decode(message)
                                        print(decodedmessage)
                                        print('test meme')
                                        if decodedmessage[0] == 0:
                                            myint+= 1
                                        if myint == messageparts:
                                            print('meme2')
                                            break
                                        serverSocket.sendto(Header(decodedmessage[0],5, messageparts,myint2,0,multilinestring2[buffersize*myintx:(myintx+1)*buffersize].encode()),address)
                                print(decodedmessage)
            
            if decodedmessage[5].decode() == '3' or  decodedmessage[5].decode() == 'Paella':
                if decodedmessage[2] < messageparts:
                    multilinestring1
                    print(multilinestring1[0:1024])
                    print(messageparts)
                    serverSocket.sendto(Header(decodedmessage[0],5,messageparts,1,0,multilinestring3[0:buffersize].encode()),address)
                    print('test')
                    message, _ = serverSocket.recvfrom(1024)
                    decodedmessage = decode(message)
                    print('test2')
                    print(decodedmessage)
                    if decodedmessage[1] == 0:
                        myint = 0
                        myint2 = 1
                        while (True) :
                            myint2+= 1
                            myintx+= 1
                            message, _ = serverSocket.recvfrom(1024)
                            decodedmessage = decode(message)
                            print(decodedmessage)
                            print('test meme')
                            if decodedmessage[0] == 0:
                             myint+= 1
                            if myint == messageparts:
                                print('meme2')
                                break
                            serverSocket.sendto(Header(decodedmessage[0],5, messageparts,myint2,0,multilinestring3[buffersize*myintx:(myintx+1)*buffersize].encode()),address)
                    print(decodedmessage)

            if decodedmessage[5].decode() == '4' or  decodedmessage[5].decode() == 'Sushi':
                if decodedmessage[2] < messageparts:
                    multilinestring1
                    print(multilinestring1[0:1024])
                    print(messageparts)
                    serverSocket.sendto(Header(decodedmessage[0],5,messageparts,1,0,multilinestring4[0:buffersize].encode()),address)
                    print('test')
                    message, _ = serverSocket.recvfrom(1024)
                    decodedmessage = decode(message)
                    print('test2')
                    print(decodedmessage)
                    if decodedmessage[1] == 0:
                        myint = 0
                        myint2 = 1
                        while (True) :
                            myint2+= 1
                            myintx+= 1
                            message, _ = serverSocket.recvfrom(1024)
                            decodedmessage = decode(message)
                            print(decodedmessage)
                            print('test meme')
                            if decodedmessage[0] == 0:
                             myint+= 1
                            if myint == messageparts:
                                print('meme2')
                                break
                            serverSocket.sendto(Header(decodedmessage[0],5, messageparts,myint2,0,multilinestring4[buffersize*myintx:(myintx+1)*buffersize].encode()),address)
                    print(decodedmessage)

            if decodedmessage[5].decode() == '5' or  decodedmessage[5].decode() == 'Steak':
                if decodedmessage[2] < messageparts:
                    multilinestring1
                    print(multilinestring1[0:1024])
                    print(messageparts)
                    serverSocket.sendto(Header(decodedmessage[0],5,messageparts,1,0,multilinestring5[0:buffersize].encode()),address)
                    print('test')
                    message, _ = serverSocket.recvfrom(1024)
                    decodedmessage = decode(message)
                    print('test2')
                    print(decodedmessage)
                    if decodedmessage[1] == 0:
                        myint = 0
                        myint2 = 1
                        while (True) :
                            myint2+= 1
                            myintx+= 1
                            message, _ = serverSocket.recvfrom(1024)
                            decodedmessage = decode(message)
                            print(decodedmessage)
                            print('test meme')
                            if decodedmessage[0] == 0:
                             myint+= 1
                            if myint == messageparts:
                                print('meme2')
                                break
                            serverSocket.sendto(Header(decodedmessage[0],5, messageparts,myint2,0,multilinestring5[buffersize*myintx:(myintx+1)*buffersize].encode()),address)
                    print(decodedmessage)
        '''
        
        if decodedmessage[1] == MessageGoodbye:
            serverSocket.sendto(Header(0,6,1,1,0,bytes()),address)
            quit()
        


        #if decodedmessage[1] != '1' or decodedmessage[1] != '2' or decodedmessage[1] != '3' or decodedmessage[1] !='4' or decodedmessage[1]!= '5' or decodedmessage[1]!= 'Roast Chicken' or decodedmessage[1]!= 'Burger' or decodedmessage[1]!= 'Paella' or decodedmessage[1]!= 'Sushi' or decodedmessage[1]!= 'Steak':
         #   serverSocket.sendto(Header(0,8,1,1,0,bytes()),address)
        # print('recipes1')'''
    
    
        
       # message, _ = serverSocket.recvfrom(1024)
       # decodedmessage = decode(message)
        #if decodedmessage == '1':
        #print('Roast Chicken')
        #serverSocket.sendto(multilinestring1.encode('UTF-8'),address)


    #print((decodedmessage6.decode('ascii')))
 #   if decodedmessage[1] == MessageTypeHello:
  #      serverSocket.sendto(Header(decodedmessage[0],1,1,1,0,HelloHeader(1024)), address)#
   #     decodedmessage[8:]


    #if decodedmessage[1] == MessageRequestId:
     #   serverSocket.sendto(Header(decodedmessage[0],2,1,1,0,bytes()))
      #  message,address = serverSocket.recvfrom(1024)
        
    
   
    #choice,address = serverSocket.recvfrom(1024)
   # choice,address = serverSocket.recvfrom(1024)
    #serverSocket.sendto(recipestring.encode('UTF-8'), address)
    
   # choice,address = serverSocket.recvfrom(1024)
    #decodedmessage = decode(choice)
    #print(decodedmessage[5])
    
    
    
    
    '''
    choice = choice.decode('UTF-8')
    if choice == '1':
       # print('Roast Chicken')
        serverSocket.sendto(multilinestring1.encode('UTF-8'),address)
    
    if choice == '2':
        #print burger
        serverSocket.sendto(multilinestring2.encode('UTF-8'),address)
   
    if choice == '3':
        #print paella
        serverSocket.sendto(multilinestring3.encode('UTF-8'),address)

    if choice == '4':
        #print sushi
        serverSocket.sendto(multilinestring4.encode('UTF-8'),address)

    if choice == '5':
        #print paella
        serverSocket.sendto(multilinestring5.encode('UTF-8'),address)


    if choice == 'No':
        serverSocket.sendto(MessageGoodbye)
   
    decodedmessage = decode(message) 
    print(str(decodedmessage))
    if decodedmessage[2] == MessageRequestId: 
       
       
        serverSocket.sendto(MessageListResponse('sdf'), address)#
        decodedmessage[8:]


    


''''''# If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
        print(str(message)+" timing out")
        continue
    # Otherwise, the server responds
    print("Sending message: "+str(message))
    serverSocket.sendto(message, address)

'''
    #put if statement after recieve something

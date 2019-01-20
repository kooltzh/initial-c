# initial-BC
Initial-BC is a web chat app with integrated blockchain. 
The purposes of this project is to help user to record messeges' originality. It also helps us to trace and identify rumors. 
It will create a blockchain for a "potential" rumors according to the message size. After that, it will compare the rumor message with your sent message, another chain will be created if your sent message has a similarity of higher than 90% with the rumor message

## Motivation


## Notiable functionality
To prove that this Application can be integrated into all types of chat system. We create a "XMPP-like" chat system which is end to end encrypted. The comparison between received and sent message is all computed at the client side.

### Track chat message source using blockchain
1. The message will be encrypted with the sender's public key to create a hashed message
2. The recipent will received the message(along with its own block chain access)
3. Every following sent message by the recipent will be used to compared with the chained message
4. Another chain will be created if the sent message is similar to the chained message
5. Step 1 and 4 will keep on repeating every other senders and recipents

### Forwarded msg detection with similarity


## Component made

### Secure chat apps with asymmetry cryptography


### Central server

### Blockchain server 

# python-simplekvs
Simple KVS server built with python, for studying purpose

## What is this?
I wanted to try and write a simple memory-based KVS, to study socket connections on Python. 

## How to Use

### Starting the Server

Just run the python script.  
The second argument is the port number.  

```
python SimpleKVS.py 8888
```

### Connecting 

Any TCP connection on the socket will do. 

```
telnet localhost 8888
```

### Storing/getting data

SET {key} {value}\n
 * returns 0 if successfully set.  
 * returns 1 if error.  

GET {key}\n
 * returns {value} if data is found.  
 * returns null byte (\0) if there is no data in the key.  






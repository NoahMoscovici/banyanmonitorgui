## Documentation on banyan_monitor_gui.py

#### How banyan_monitor_gui.py works
This is a Tkinter GUI that allows a way to easily view messages going through the banyanrouter while being able to switch through topics in real-time. The GUI works by listening to every message on a certain banyanrouter.


#### How to run banyan_monitor_gui.py
While running banyan_monitor_gui.py, you are able to pass through two arguments: the topic(s) you want to listen to (-t) and the banyanrouter you are listening on (-b). The argument -b is required, while leaving -t blank or not setting it will default to listening to all messages through that banyanrouter. The only reason you would need to pass in specific topics while running the script is because of the large amount of messages the scirpt would be trying to display. Since Tkinter has a fixed loop time, it cannot pick up every message and will drop some if many messages are being passed through. However, this won't be a problem unless you would be expecting over 10,000 messages a minute. For banyanrouters recieving less than 10,000 messages a minute, not using the argument -t is best. 

An example of how to run the script would be:
```
python3 /banyan_monitor_gui.py -b 172.16.70.1 -t topic1,topic2,topic3
```
or 
```
python3 /banyan_monitor_gui.py -b 172.16.70.1
```

#### What do the buttons on the GUI do?

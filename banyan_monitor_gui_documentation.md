## Documentation on banyan_monitor_gui.py

#### How banyan_monitor_gui.py works
This is a Tkinter GUI that allows a way to easily view messages going through the banyanrouter while being able to switch through topics in real-time. 


#### How to use banyan_monitor_gui.py
While running banyan_monitor_gui.py, you are able to pass through two arguments: the topic(s) you want to listen to (-t) and the banyanrouter you are listening on (-b). The argument -b is required, while leaving -t blank or not setting it will default to listening to all messages through that banyanrouter. An example of how to run it would be ```./banyan_monitor_gui.py -b 172.16.70.1 -t topic1,topic2,topic3```

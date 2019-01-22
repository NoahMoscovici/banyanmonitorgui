## Documentation on banyan_monitor_gui.py

#### How banyan_monitor_gui.py works
This is a Tkinter GUI that allows a way to easily view messages going through the banyanrouter while being able to switch through topics in real-time. The GUI works by listening to every message (or the messages for the topic(s) passed through) on a certain banyanrouter. The script then builds a dynamic topic list dropdown interface in the GUI that updates as messages with various topics come through. You are then able to narrow down the flood of messages being displayed by choosing a specific topic to listen to. Another way you can narrow down your search is by seraching for specific terms in the filter box. 


#### How to run banyan_monitor_gui.py
While running banyan_monitor_gui.py, you are able to pass two arguments: the comma seperated list of topic(s) you want to listen to (-t) and the banyanrouter you are listening on (-b). The argument -b is required, while not setting -t will default to listening to all messages. The only reason you would need to pass in specific topics while running the script is because of the large volume of messages the scirpt would be trying to display. Since Tkinter has a fixed loop time, it cannot pick up every message and will drop some if too many messages are being passed through. However, this won't be a problem unless you are expecting over 10,000 messages a minute. For banyanrouters recieving less than 10,000 messages a minute, not using the argument -t is best. 

An example of how to run the script would be:
```
python3 /banyan_monitor_gui.py -b 172.16.70.1 -t topic1,topic2,topic3
```
or 
```
python3 /banyan_monitor_gui.py -b 172.16.70.1
```

#### What do the buttons on the GUI do/mean?
![Image of GUI](https://github.com/NoahMoscovici/banyanmonitorgui/blob/master/banyan_monitor_gui_screenshot.png)

**Filtered Messages Per Minute:**
This displays the filtered messages (the ones showing up on the big message box) per minute by taking the number received in 3 second intervals and multiplying it by 20. (If you recieve less than one message every 3 seconds, the display will sometimes say 0)

**Enter Keyword to Filter:**
This box allows you to futher your message filter by seraching for specific keywords in the payload of the messages. In the image, the keyword WGAM is being searched along with the topic.

**Topic:**
This is a dropdown box that allows you to filter your messages by their topic. The message box gets dynamically updated as messages with a new topic come through. Selecting *ALL* in the dropdown will give you all of the messages, regardless of their topic. Selecting a topic will automatically clear the messages in the big message box. Remeber that your topic list is limited by what is passed through when calling the script (-t).

**Pause/Play**
This button is used to pause/play the messages being displayed on the big message box. However, the pausing will not affect the *Filtered Messages Per Minute box.* (Once pressing pause, the button will be replaced with the play button and vise versa) *Note that the pause does not buffer any messages. It simply stops displaying the messages*

**Clear Messages**
This button will clear the messages being displayed in the big message box.

*If you attempt to process more messages than Tkinter can handle in its update loop (about 10,000 messages per minute), the GUI can delay displaying messages and in some situations messages can be dropped.*

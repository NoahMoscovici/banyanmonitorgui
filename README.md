## Documentation on banyan_monitor_gui.py
banyan_monitor_gui.py is a Tkinter GUI that allows a way to easily view messages going through the banyanrouter while being able to switch through topics in real-time. banyan_monitor_gui.py listens to, parses, and organizes messages being sent through a Python Banyan Backplane to present information in a clean and intuitive manner. The project is built off the Python Banyan framework, by Alan Yorinks. *See [here](https://mryslab.github.io/python_banyan/) for in-depth documentation and setup of Python Banyan.*

#### How to run banyan_monitor_gui.py
While running banyan_monitor_gui.py, you must pass the IP address of the python-banyan backplane you wish to listen to. However, Tkinter's fixed loop time may mean that this GUI cannot pick up every message in the event too many messages are being sent (around 10,000 messages a minute). You can fix such an issue by limiting the topics the GUI will listen to through passing a list of topics as an argument. This argument is optional, and if not set will listen to all topics on the backplane (this is recommended to backplanes handling less than 10,000 messages a minute).

For example, the following might be run if the python-banyan backplane were to be running on the 172.16.70.1 IP Address:
```
python3 banyan_monitor_gui.py -b 172.16.70.1 -t topic1,topic2,topic3
```

#### Utilities provided through the banyan_monitor_gui.py interface
![Image of GUI](https://github.com/NoahMoscovici/banyanmonitorgui/blob/master/banyanmonitorgui.png)

**Filtered Messages Per Minute:**
This displays the filtered messages (the ones showing up on the big message box) per minute by taking the number received in 3 second intervals and multiplying it by 20. (If you receive less than one message every 3 seconds, the display will sometimes say 0)

**Enter Keyword to Filter:**
This box allows you to further your message filter by searching for specific keywords in the payload of the messages. In the image, the keyword WGAM is being searched along with the topic.

**Topic:**
This is a dropdown box that allows you to filter your messages by their topic. The message box gets dynamically updated as messages with a new topic come through. Selecting *ALL* in the dropdown will give you all of the messages, regardless of their topic. Selecting a topic will automatically clear the messages in the big message box. Remember that your topic list is limited by what is passed through when calling the script (-t).

**Pause/Play**
This button is used to pause/play the incoming flow of messages displayed. This will not disrupt or alter the *actual* flow of messages on the banyan framework, just halt the displaying of such picked up messages.

**Clear Messages**
This button will clear the messages being displayed on the large display.

---
*For further help on installation or other inquiries, feel free to contact me at noah.moscovici@gmail.com*

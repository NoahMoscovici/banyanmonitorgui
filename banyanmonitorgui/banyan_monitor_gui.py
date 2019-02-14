#!/usr/bin/env python3
"""


 Copyright (c) 2019 Noah Moscovici, Palace Games. All right reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import argparse
import signal
import time
import tkinter as tk
import tkinter.scrolledtext as tkst
import traceback
from datetime import datetime
from tkinter import *
from tkinter import ttk

import msgpack
import msgpack_numpy as m
import zmq
from python_banyan.banyan_base import BanyanBase

YELLOW_COLOR = "LightGoldenrod1"
GREEN_COLOR = "palegreen1"
GRAY_COLOR = "snow3"
BLUE_COLOR = "deep sky blue"
FONT = ("droidsans", 8)
LARGE_FONT = ("droidsans", 13)


class MonitorGui(BanyanBase):
    def __init__(self, back_plane_ip_address,
                 subscriber_port='43125',
                 publisher_port='43124',
                 process_name=None, numpy=True,
                 loop_time=0.01, topic_names=''):
        """
        :param back_plane_ip_address:
        :param subscriber_port:
        :param publisher_port:
        :param process_name:
        :param numpy:
        :param loop_time:
        :param topic_names:
        """

        # initialize the base class
        super().__init__(back_plane_ip_address,
                         subscriber_port=subscriber_port,
                         publisher_port=publisher_port,
                         process_name=process_name,
                         numpy=numpy)

        self.loop_time = loop_time

        # allow time for connection
        time.sleep(.03)
        m.patch()

        self.topic_array = ['ALL']


        # make an array of topics based of the list passed by spliting it by commas
        topic_array = topic_names[0:420].split(',')

        for t in topic_array:
            print('        Subscribed to topic: ' + t)
            # set the topic subscribing to for each item in array
            self.set_subscriber_topic(t)
            self.topic_array.append(t)

        self.master = Tk()

        # set the title of the window
        self.master.wm_title("Banyan Monitor on the " + self.back_plane_ip_address + "-banyanrouter")

        # set up the frames for the buttons and message display
        self.button_frame = Frame(self.master)
        self.button_frame.pack(side=LEFT)
        self.message_frame = Frame(self.master)
        self.message_frame.pack(side=RIGHT)

        # message display
        self.message_box = tkst.ScrolledText(self.message_frame, height=60, width=175, bg=GRAY_COLOR)
        self.message_box.grid(row=0, column=0, padx=5, sticky="e")

        # message count label and display
        self.total_count = StringVar()
        self.total_count.set(" ")
        self.message_count_label = Label(self.button_frame, text="Filtered Messages per Minute:", font=LARGE_FONT)
        self.message_count_label.grid(row=2, column=0, padx=5, pady=0, sticky="nw")
        self.count = StringVar()
        self.message_count = Entry(self.button_frame, text=self.count, background=GRAY_COLOR, font=LARGE_FONT, width=10,
                                   state="disabled")
        self.message_count.grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.count.set(" ")

        # message filter label and display
        self.message_filter_label = Label(self.button_frame, text="Enter Keyword to Filter:", font=LARGE_FONT)
        self.message_filter_label.grid(row=4, column=0, padx=5, sticky="nw")
        self.message_filter_box = Entry(self.button_frame, text="Topic", width=25, background=GRAY_COLOR,
                                        font=LARGE_FONT)
        self.message_filter_box.grid(row=5, column=0, padx=5, sticky="nw")

        # topic dropdown
        self.topic_name = "ALL"
        self.topic_val = StringVar()
        self.topic_drop = ttk.Labelframe(self.button_frame, text='Topic')
        self.topic_drop.grid(in_=self.button_frame, pady=5, padx=5, row=6, column=0, sticky="sw")
        self.topic_combobox = ttk.Combobox(self.topic_drop, textvariable=self.topic_val, width="30")
        self.topic_combobox['values'] = self.topic_array
        self.topic_combobox.bind('<<ComboboxSelected>>', self.topicselect)
        self.topic_combobox.current(0)
        self.topic_combobox.grid(pady=5, padx=5)

        # pause/play button
        self.paused = False
        self.pp_button = Button(self.button_frame, text="Pause", height=1, background=YELLOW_COLOR, font=LARGE_FONT,
                                command=lambda: (self.pp_chat()))
        self.pp_button.grid(row=7, column=0, padx=5, pady=10, sticky="nw")

        # clear button
        self.clear_button = Button(self.button_frame, text="Clear Messages", height=1, background=BLUE_COLOR,
                                   font=LARGE_FONT, command=lambda: (self.clear_messages()))
        self.clear_button.grid(row=8, column=0, padx=5, pady=10, sticky="nw")

        # clear the message display
        display_messages = ""
        self.update_message_box(display_messages)

        # set variables for later message count calculations
        self.message_count_int = 0
        self.message_count_min = 0
        self.last_time = datetime.now()
        self.current_time = datetime.now()
        self.elapsed_time = None

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.after(1, self.get_message)
        self.master.mainloop()

    def topicselect(self, event=None):
        # change the var topic_name to the selected topic
        self.topic_name = event.widget.get()
        self.clear_messages()

    def pp_chat(self):
        # check whether the chat is paused or playing and change it
        if self.paused:
            self.paused = False
            self.pp_button.configure(text="Pause", background=YELLOW_COLOR)
        else:
            self.paused = True
            self.pp_button.configure(text="Play", background=GREEN_COLOR)

    def clear_messages(self):
        # clear the messages in the display
        self.message_box.configure(state='normal')
        self.message_box.delete('1.0', tk.END)
        self.message_box.configure(state='disabled')

    def update_message_box(self, message):
        # update the display with incoming messages
        if not self.paused:
            self.message_box.configure(state='normal')
            self.message_box.insert(tk.END, message + '\n')
            self.message_box.yview(tk.END)
            self.message_box.configure(state='disabled')
        else:
            pass

    def get_message(self):
        """
        This method is called from the tkevent loop "after" call. It will poll for new zeromq messages
        :return:
        """

        try:
            data = self.subscriber.recv_multipart(zmq.NOBLOCK)
            try:
                if self.numpy:
                    payload = msgpack.unpackb(data[1], object_hook=m.decode)
                    self.incoming_message_processing(data[0].decode(), payload)
                    self.master.after(1, self.get_message)
                else:
                    self.incoming_message_processing(data[0].decode(), msgpack.unpackb(data[1]))
                    self.master.after(1, self.get_message)

            except Exception:
                self.error_reporting()

        except zmq.error.Again:
            try:
                self.master.after(1, self.get_message)
            except KeyboardInterrupt:
                self.clean_up()
            except Exception:
                self.error_reporting()

    def error_reporting(self):
        """used to send a stack trace when there is an error"""
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

    def incoming_message_processing(self, topic, payload):
        """
        :param topic: Message Topic string
        :param payload: Message Data
        :return:
        """

        if topic not in self.topic_array:
            # the topic array get built dynamically based on incoming messages
            self.topic_array.append(topic)
            self.topic_combobox['values'] = sorted(self.topic_array)

            # increment the message count
            self.message_count_int = self.message_count_int + 1

        self.current_time = datetime.now()
        self.elapsed_time = self.current_time - self.last_time

        if int(self.elapsed_time.total_seconds()) > 3:
            # every 3 seconds take the number of messages received and
            # times it by 20 to find the estimated number of messages per minute
            self.message_count_min = self.message_count_int * 20

            self.count.set(self.message_count_min)

            self.message_count_int = 0
            self.last_time = datetime.now()

        if topic == self.topic_name or self.topic_name == "ALL":

            if self.message_filter_box.get() in str(payload):
                # only display the messages if it is under the topic set in dropdown
                if self.topic_name == "ALL":
                    display_messages = "Topic: " + str(topic) + "\n" + "Payload: " + str(payload)
                else:
                    display_messages = str(payload)

                self.message_count_int = self.message_count_int + 1
                self.update_message_box(display_messages)

    def on_closing(self):
        """
        Destroy the window
        :return:
        """
        self.master.destroy()

    def clean_up(self):
        """
        Clean up before exiting - override if additional cleanup is necessary

        :return:
        """
        self.master.destroy()
        self.publisher.close()
        self.subscriber.close()
        self.context.term()
        sys.exit(0)


def start_gui():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="back_plane_ip_address", default="None",
                        help="None or IP address used by Back Plane",
                        )
    parser.add_argument("-m", dest="numpy", default="True",
                        help="Set to False If Not Using Numpy")
    parser.add_argument("-n", dest="process_name", default="MasterGui",
                        help="Process Name on Banner")
    parser.add_argument("-p", dest="publisher_port", default='43124',
                        help="Publisher IP port")
    parser.add_argument("-s", dest="subscriber_port", default='43125',
                        help="Subscriber IP port")
    parser.add_argument("-t", dest="topic_names", default="",
                        help="Separate topic names with commas")

    args = parser.parse_args()
    kw_options = {}

    if args.back_plane_ip_address == 'None':
        args.back_plane_ip_address = None

    kw_options['back_plane_ip_address'] = args.back_plane_ip_address

    kw_options['process_name'] = args.process_name

    kw_options['topic_names'] = args.topic_names

    kw_options['publisher_port'] = args.publisher_port

    kw_options['subscriber_port'] = args.subscriber_port

    if args.numpy == "True":
        kw_options['numpy'] = True
    else:
        kw_options['numpy'] = False

    my_monitor_gui = MonitorGui(**kw_options)

    # signal handler function called when Control-C occurs
    # noinspection PyShadowingNames,PyUnusedLocal,PyUnusedLocal
    def signal_handler(signal, frame):
        print('Control-C detected. See you soon.')
        my_monitor_gui.master.destroy()
        sys.exit(0)

    # listen for SIGINT
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


if __name__ == '__main__':
    try:
        start_gui()
    except KeyboardInterrupt:
        sys.exit(0)

import tkinter as tk
import random
from random import randint
from win32api import GetMonitorInfo, MonitorFromPoint
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
import json
import threading
import time

use_cloud_resource = False

subscription_id = "eeeee5b2-666a-4f32-bb9f-4d548cd027db"
resource_group_name = "AZURESTORAGE"

subscription_id_2 = "18bed606-20b7-4119-ba9d-679a31d8f57e"
resource_group_name_2 = "rg-BlogCypoint-01"

subscription_id_3 = "18bed606-20b7-4119-ba9d-679a31d8f57e"
resource_group_name_3 = "rg-skidev"

def get_vm_status(compute_client, resource_group, vm_name):
    # Getting the status of a virtual machine
    vm_instance_view = compute_client.virtual_machines.instance_view(resource_group, vm_name)
    statuses = vm_instance_view.statuses
    for status in statuses:
        if status.code.startswith('PowerState/'):
            return status.code
    return 'Unknown'

def list_resources(subscription_id, resource_group_name):
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)
    compute_client = ComputeManagementClient(credential, subscription_id)

    resource_list = []
    for resource in resource_client.resources.list_by_resource_group(resource_group_name):
        if resource.type == 'Microsoft.Compute/virtualMachines':
            resource_info = {
                'name': resource.name,
                'type': resource.type.replace('Microsoft.Compute/', ''),
            }
        # Check if the resource is a VM to get its status
        if resource.type == 'Microsoft.Compute/virtualMachines':
            resource_info['status'] = get_vm_status(compute_client, resource_group_name, resource.name).replace('PowerState/', '')
            resource_list.append(resource_info)

    return json.dumps(resource_list, indent=2)


monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get('Work')
screen_width = work_area[2]
work_height = work_area[3]

idle_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # 12
sleep_num = [19, 20, 21, 22, 23, 24]  # 26
walk_left = [13, 14, 15]
walk_right = [16, 17, 18]
angry = [25]

class Sprite():
    def __init__(self, master, sprit_type, horizontal_position, name, status):
        self.name = name
        self.status = status
        self.window = tk.Toplevel(master)
        self.master = master
        self.spirt_type = sprit_type
        self.name_window = tk.Toplevel(master)
        self.name_window.overrideredirect(True)
        self.name_window.attributes('-topmost', True)
        self.name_window.config(bg='black')
        self.name_window.wm_attributes('-transparentcolor', 'black')

        self.name_label = tk.Label(self.name_window, text=name, bg="black", font=("Arial", 20), fg="white")
        self.name_label.pack()

        if sprit_type == "loadbalancer":
            self.idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 41)]
            self.idle_to_sleeping =[tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 41)]
            self.sleeping = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 41)]
            self.sleeping_to_idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 41)]
            self.walking_left = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 41)]
            self.walking_right = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 41)]
            self.x = horizontal_position
            self.y = work_height - 135

            self.i_frame = 0
            self.state = 1
            self.event_number = randint(1, 4)

            self.frame = self.idle[0]
            
            self.window.config(highlightbackground='black')
            self.label = tk.Label(self.window, bd=0, bg='black')
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)
            self.window.wm_attributes('-transparentcolor', 'black')
            self.animation_speed = 5  # Faster speed for 'vpc' with many frames

            self.label.pack()
            self.label.bind('<Double-Button-1>', self.close_script)

        elif sprit_type == "iam":
            self.idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 60)]
            self.idle_to_sleeping =[tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 20)]
            self.sleeping = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 60)]
            self.sleeping_to_idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 20)]
            self.walking_left = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 20)]
            self.walking_right = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 20)]
            self.x = horizontal_position
            self.y = work_height - 135

            self.i_frame = 0
            self.state = 1
            self.event_number = randint(1, 4)

            self.frame = self.idle[0]
            
            self.window.config(highlightbackground='black')
            self.label = tk.Label(self.window, bd=0, bg='black')
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)
            self.window.wm_attributes('-transparentcolor', 'black')
            self.animation_speed = 5  # Faster speed for 'vpc' with many frames

            self.label.pack()
            self.label.bind('<Double-Button-1>', self.close_script)

        elif sprit_type == "cdn":
            self.idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 300)]
            self.idle_to_sleeping =[tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.sleeping = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 300)]
            self.sleeping_to_idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.walking_left = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.walking_right = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.x = horizontal_position
            self.y = work_height - 130

            self.i_frame = 0
            self.state = 1
            self.event_number = randint(1, 4)

            self.frame = self.idle[0]
            
            self.window.config(highlightbackground='black')
            self.label = tk.Label(self.window, bd=0, bg='black')
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)
            self.window.wm_attributes('-transparentcolor', 'black')
            self.animation_speed = 1  # Faster speed for 'vpc' with many frames

            self.label.pack()
            self.label.bind('<Double-Button-1>', self.close_script)

        elif sprit_type == "faas":
            self.idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 150)]
            self.idle_to_sleeping =[tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.sleeping = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 150)]
            self.sleeping_to_idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.walking_left = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.walking_right = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.x = horizontal_position
            self.y = work_height - 130

            self.i_frame = 0
            self.state = 1
            self.event_number = randint(1, 4)

            self.frame = self.idle[0]
            
            self.window.config(highlightbackground='black')
            self.label = tk.Label(self.window, bd=0, bg='black')
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)
            self.window.wm_attributes('-transparentcolor', 'black')
            self.animation_speed = 5  # Faster speed for 'vpc' with many frames

            self.label.pack()
            self.label.bind('<Double-Button-1>', self.close_script)

        elif sprit_type == "nosql":
            self.idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.idle_to_sleeping =[tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.sleeping = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.sleeping_to_idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.walking_left = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.walking_right = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 40)]
            self.x = horizontal_position
            self.y = work_height - 130

            self.i_frame = 0
            self.state = 1
            self.event_number = randint(1, 4)

            self.frame = self.idle[0]
            
            self.window.config(highlightbackground='black')
            self.label = tk.Label(self.window, bd=0, bg='black')
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)
            self.window.wm_attributes('-transparentcolor', 'black')
            self.animation_speed = 5  # Faster speed for 'vpc' with many frames

            self.label.pack()
            self.label.bind('<Double-Button-1>', self.close_script)

        elif sprit_type == "sql":
            self.idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 150)]
            self.idle_to_sleeping =[tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 35)]
            self.sleeping = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 150)]
            self.sleeping_to_idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 35)]
            self.walking_left = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 35)]
            self.walking_right = [tk.PhotoImage(file=f'assets/{sprit_type}/idle ({i}).gif') for i in range(1, 35)]
            self.x = horizontal_position
            self.y = work_height - 130

            self.i_frame = 0
            self.state = 1
            self.event_number = randint(1, 4)

            self.frame = self.idle[0]
            
            self.window.config(highlightbackground='black')
            self.label = tk.Label(self.window, bd=0, bg='black')
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)
            self.window.wm_attributes('-transparentcolor', 'black')
            self.animation_speed = 5  # Faster speed for 'vpc' with many frames

            self.label.pack()
            self.label.bind('<Double-Button-1>', self.close_script)

        elif sprit_type == "storage":
            self.idle = [tk.PhotoImage(file=f'assets/{sprit_type}/base/idle ({i}).gif') for i in range(1, 136)]
            self.idle_to_sleeping =[tk.PhotoImage(file=f'assets/{sprit_type}/base/idle ({i}).gif') for i in range(1, 35)]
            self.sleeping = [tk.PhotoImage(file=f'assets/{sprit_type}/base/idle ({i}).gif') for i in range(1, 136)]
            self.sleeping_to_idle = [tk.PhotoImage(file=f'assets/{sprit_type}/base/idle ({i}).gif') for i in range(1, 35)]
            self.walking_left = [tk.PhotoImage(file=f'assets/{sprit_type}/base/idle ({i}).gif') for i in range(1, 35)]
            self.walking_right = [tk.PhotoImage(file=f'assets/{sprit_type}/base/idle ({i}).gif') for i in range(1, 35)]
            self.x = horizontal_position
            self.y = work_height - 64

            self.i_frame = 0
            self.state = 1
            self.event_number = randint(1, 4)

            self.frame = self.idle[0]
            
            self.window.config(highlightbackground='black')
            self.label = tk.Label(self.window, bd=0, bg='black')
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)
            self.window.wm_attributes('-transparentcolor', 'black')
            self.animation_speed = 5  # Faster speed for 'vpc' with many frames

            self.label.pack()
            self.label.bind('<Double-Button-1>', self.close_script)

        elif sprit_type == "MKS":
            self.idle = [tk.PhotoImage(file=f'assets/{sprit_type}/base/idle ({i}).gif') for i in range(1, 150)]
            self.idle_to_sleeping =[tk.PhotoImage(file=f'assets/{sprit_type}/base/idle ({i}).gif') for i in range(1, 35)]
            self.sleeping = [tk.PhotoImage(file=f'assets/{sprit_type}/base/idle ({i}).gif') for i in range(1, 150)]
            self.sleeping_to_idle = [tk.PhotoImage(file=f'assets/{sprit_type}/base/idle ({i}).gif') for i in range(1, 35)]
            self.walking_left = [tk.PhotoImage(file=f'assets/{sprit_type}/base/idle ({i}).gif') for i in range(1, 35)]
            self.walking_right = [tk.PhotoImage(file=f'assets/{sprit_type}/base/idle ({i}).gif') for i in range(1, 35)]
            self.x = horizontal_position
            self.y = work_height - 64

            self.i_frame = 0
            self.state = 1
            self.event_number = randint(1, 4)

            self.frame = self.idle[0]
            
            self.window.config(highlightbackground='black')
            self.label = tk.Label(self.window, bd=0, bg='black')
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)
            self.window.wm_attributes('-transparentcolor', 'black')
            self.animation_speed = 5  # Faster speed for 'vpc' with many frames

            self.label.pack()
            self.label.bind('<Double-Button-1>', self.close_script)

        elif sprit_type == "robot":
            self.idle = [tk.PhotoImage(file=f'assets/{sprit_type}/robot ({i}).gif') for i in range(1, 87)]
            self.idle_to_sleeping = [tk.PhotoImage(file=f'assets/{sprit_type}/robot ({i}).gif') for i in range(1, 87)]
            self.sleeping = [tk.PhotoImage(file=f'assets/{sprit_type}/robot ({i}).gif') for i in range(1, 87)]
            self.sleeping_to_idle = [tk.PhotoImage(file=f'assets/{sprit_type}/robot ({i}).gif') for i in range(1, 87)]
            self.walking_left = [tk.PhotoImage(file=f'assets/{sprit_type}/robot ({i}).gif') for i in range(7, 19)]
            self.walking_right = [tk.PhotoImage(file=f'assets/{sprit_type}/robot ({i}).gif') for i in range(7, 19)]

            self.x = horizontal_position
            self.y = work_height - 102

            self.i_frame = 0
            self.state = 1
            self.event_number = randint(1, 3)

            self.frame = self.idle[0]

            self.window.config(highlightbackground='black')
            self.label = tk.Label(self.window, bd=0, bg='black')
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)
            self.window.wm_attributes('-transparentcolor', 'black')
            self.animation_speed = 5  # Faster speed for 'robot' with many frames

            self.label.pack()
            self.label.bind('<Double-Button-1>', self.close_script)

        elif sprit_type == "gpt_robot":
            self.idle=[tk.PhotoImage(file=f'assets/{sprit_type}/idle1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle4.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle1.png')]
            self.idle_to_sleeping=[tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping4.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping5.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping6.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping7.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping8.png')]
            self.sleeping=[tk.PhotoImage(file=f'assets/{sprit_type}/sleeping1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping4.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping5.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping6.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping7.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping8.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping9.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping10.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping11.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping12.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping13.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping14.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping15.png')]
            self.sleeping_to_idle=[tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping8.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping7.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping6.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping5.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping4.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle_to_sleeping1.png')]
            self.walking_left=[tk.PhotoImage(file=f'assets/{sprit_type}/walking_left1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walking_left2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walking_left3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walking_left4.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walking_left5.png')]
            self.walking_right=[tk.PhotoImage(file=f'assets/{sprit_type}/walking_right1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walking_right2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walking_right3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walking_right4.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walking_right5.png') ]
            self.angry=[tk.PhotoImage(file=f'assets/{sprit_type}/notice.png'), tk.PhotoImage(file=f'assets/{sprit_type}/notice.png'), tk.PhotoImage(file=f'assets/{sprit_type}/notice.png'), tk.PhotoImage(file=f'assets/{sprit_type}/notice.png') ]


            self.x = horizontal_position
            self.y = work_height - 200

            self.i_frame = 0
            self.state = 1
            self.event_number = randint(1, 3)

            self.frame = self.idle[0]

            self.window.config(highlightbackground='black')
            self.label = tk.Label(self.window, bd=0, bg='black')
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)
            self.window.wm_attributes('-transparentcolor', 'black')
            self.animation_speed = 10  # Faster speed for 'robot' with many frames

            self.label.pack()
            self.label.bind('<Double-Button-1>', self.close_script)

        elif sprit_type == "cat":
            self.idle=[tk.PhotoImage(file=f'assets/{sprit_type}/idle1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/idle4.png')]
            self.idle_to_sleeping=[tk.PhotoImage(file=f'assets/{sprit_type}/sleeping1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping4.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping5.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping6.png')]
            self.sleeping=[tk.PhotoImage(file=f'assets/{sprit_type}/zzz1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/zzz2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/zzz3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/zzz4.png')]
            self.sleeping_to_idle=[tk.PhotoImage(file=f'assets/{sprit_type}/sleeping6.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping5.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping4.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/sleeping1.png')]
            self.walking_left=[tk.PhotoImage(file=f'assets/{sprit_type}/walkingleft1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walkingleft2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walkingleft3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walkingleft4.png')]
            self.walking_right=[tk.PhotoImage(file=f'assets/{sprit_type}/walkingright1.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walkingright2.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walkingright3.png'), tk.PhotoImage(file=f'assets/{sprit_type}/walkingright4.png') ]
            self.angry=[tk.PhotoImage(file=f'assets/{sprit_type}/angry.png'), tk.PhotoImage(file=f'assets/{sprit_type}/angry.png'), tk.PhotoImage(file=f'assets/{sprit_type}/angry.png'), tk.PhotoImage(file=f'assets/{sprit_type}/angry.png') ]

            self.x = horizontal_position
            self.y = work_height - 64

            self.i_frame = 0
            self.state = 1
            self.event_number = randint(1, 4)

            self.frame = self.idle[0]
            
            self.window.config(highlightbackground='black')
            self.label = tk.Label(self.window, bd=0, bg='black')
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)
            self.window.wm_attributes('-transparentcolor', 'black')
            self.animation_speed = 100  # Faster speed for 'vpc' with many frames

            self.label.pack()
            self.label.bind('<Double-Button-1>', self.close_script)

            self.label.bind('<Button-1>', self.handle_click)  # Bind left click

        else:
            # Load images with dynamic paths for other sprite types
            self.idle = [tk.PhotoImage(file=f'assets/{sprit_type}/idle{i}.png') for i in range(1, 4)]
            self.idle_to_sleeping = [tk.PhotoImage(file=f'assets/{sprit_type}/sleeping{i}.png') for i in range(1, 4)]
            self.sleeping = [tk.PhotoImage(file=f'assets/{sprit_type}/sleeping{i}.png') for i in range(1, 4)]
            self.sleeping_to_idle = [tk.PhotoImage(file=f'assets/{sprit_type}/sleeping{i}.png') for i in range(1, 4)]
            self.walking_left = [tk.PhotoImage(file=f'assets/{sprit_type}/walkingleft{i}.png') for i in range(1, 4)]
            self.walking_right = [tk.PhotoImage(file=f'assets/{sprit_type}/walkingright{i}.png') for i in range(1, 4)]

            self.x = horizontal_position
            self.y = work_height - 64

            self.i_frame = 0
            self.state = 1
            self.event_number = randint(1, 4)

            self.frame = self.idle[0]
            
            self.window.config(highlightbackground='black')
            self.label = tk.Label(self.window, bd=0, bg='black')
            self.window.overrideredirect(True)
            self.window.attributes('-topmost', True)
            self.window.wm_attributes('-transparentcolor', 'black')
            self.animation_speed = 100  # Faster speed for 'vpc' with many frames

            self.label.pack()
            self.label.bind('<Double-Button-1>', self.close_script)
        
        self.update_label_position()  # Add this line to update the label position
        self.label.configure(   )
        self.window.after(self.animation_speed, self.event, self.i_frame, self.state, self.event_number, self.x)

        self.label.bind('<Button-1>', self.start_drag)
        self.label.bind('<B1-Motion>', self.on_drag)
        self.label.bind('<ButtonRelease-1>', self.stop_drag)
        self.dragging = False

    def start_drag(self, event):
        self.dragging = True
        self.mouse_x = event.x
        self.mouse_y = event.y

    def on_drag(self, event):
        if self.dragging:
            delta_x = event.x - self.mouse_x
            delta_y = event.y - self.mouse_y
            self.x += delta_x
            self.y += delta_y
            self.update_position()

    def stop_drag(self, event):
        self.dragging = False

    def update_position(self):
        self.window.geometry(f"+{self.x}+{self.y}")
        self.update_label_position()

    def update_label_position(self):
        if self.status == 'running':
            self.name_label.configure(fg="green")
        else:
            self.name_label.configure(fg="red")
        label_x = self.x + (self.frame.width() // 2) - (self.name_label.winfo_width() // 2)
        label_y = self.y - self.name_label.winfo_height() - 10
        self.name_window.geometry(f"+{label_x}+{label_y}")
        self.name_window.wm_attributes('-transparentcolor', 'black')

    def close_script(self, event):
        self.master.quit()

    def event(self, i_frame, state, event_number, x):
        if self.event_number in idle_num:
            self.state = 0
            self.window.after(self.animation_speed*4, self.update, self.i_frame, self.state, self.event_number, self.x)
        elif self.event_number == 12:
            self.state = 1
            self.window.after(self.animation_speed, self.update, self.i_frame, self.state, self.event_number, self.x)
        elif self.event_number in walk_left:
            self.state = 4
            self.window.after(self.animation_speed, self.update, self.i_frame, self.state, self.event_number, self.x)
        elif self.event_number in walk_right:
            self.state = 5
            self.window.after(self.animation_speed, self.update, self.i_frame, self.state, self.event_number, self.x)
        elif self.event_number in sleep_num:
            self.state = 2
            self.window.after(self.animation_speed*4, self.update, self.i_frame, self.state, self.event_number, self.x)
        elif self.event_number == 26:
            self.state = 3
            self.window.after(self.animation_speed, self.update, self.i_frame, self.state, self.event_number, self.x)
        elif self.event_number in angry:
            if self.spirt_type == "cat":
                self.state = 6
                self.window.after(self.animation_speed, self.update, self.i_frame, self.state, self.event_number, self.x)
            elif self.spirt_type == "gpt_robot":
                self.state = 6
                self.window.after(self.animation_speed, self.update, self.i_frame, self.state, self.event_number, self.x)

    def animate(self, i_frame, array, event_number, a, b):
        if self.i_frame < len(array) - 1:
            self.i_frame += 1
        else:
            self.i_frame = 0
            self.event_number = randint(a, b)
        return self.i_frame, self.event_number

    def update(self, i_frame, state, event_number, x):

        offset = 10  # This is the offset value. Adjust it as needed.

        # Wrap around logic with offset
        if self.x < -offset:
            self.x = screen_width - offset
        elif self.x > screen_width - offset:
            self.x = -offset

        if self.state == 0:
            self.frame = self.idle[self.i_frame]
            self.i_frame, self.event_number = self.animate(self.i_frame, self.idle, self.event_number, 1, 18)
        elif state == 1:
            self.frame = self.idle_to_sleeping[self.i_frame]
            self.i_frame, self.event_number = self.animate(self.i_frame, self.idle_to_sleeping, self.event_number, 19,
                                                           19)
        elif self.state == 2:
            self.frame = self.sleeping[self.i_frame]
            self.i_frame, self.event_number = self.animate(self.i_frame, self.sleeping, self.event_number, 18, 24)
        elif self.state == 3:
            self.frame = self.sleeping_to_idle[self.i_frame]
            self.i_frame, self.event_number = self.animate(self.i_frame, self.sleeping_to_idle, self.event_number, 1, 1)
        elif self.state == 4:
            self.frame = self.walking_left[self.i_frame]
            self.i_frame, self.event_number = self.animate(self.i_frame, self.walking_left, self.event_number, 1, 18)
            self.x -= 3  # Move left
        elif self.state == 5:
            self.frame = self.walking_right[self.i_frame]
            self.i_frame, self.event_number = self.animate(self.i_frame, self.walking_right, self.event_number, 1, 18)
            self.x += 3  # Move right
        elif self.state == 6:
            self.frame = self.angry[self.i_frame]
            self.i_frame, self.event_number = self.animate(self.i_frame, self.angry, self.event_number, 23, 25)

        if self.spirt_type == 'loadbalancer':
            self.window.geometry('150x150+' + str(self.x) + '+' + str(self.y))
        elif self.spirt_type == 'iam':
            self.window.geometry('150x150+' + str(self.x) + '+' + str(self.y))
        elif self.spirt_type == 'cdn':
            self.window.geometry('150x150+' + str(self.x) + '+' + str(self.y))
        elif self.spirt_type == 'faas':
            self.window.geometry('150x150+' + str(self.x) + '+' + str(self.y))
        elif self.spirt_type == 'nosql':
            self.window.geometry('150x150+' + str(self.x) + '+' + str(self.y))
        elif self.spirt_type == 'sql':
            self.window.geometry('150x150+' + str(self.x) + '+' + str(self.y))
        elif self.spirt_type == 'robot':
            self.window.geometry('150x124+' + str(self.x) + '+' + str(self.y))
        elif self.spirt_type == 'gpt_robot':
            self.window.geometry('120x203+' + str(self.x) + '+' + str(self.y))
        else:
            self.window.geometry('72x64+' + str(self.x) + '+' + str(self.y))

        if self.name == 'vm-skidev':
            self.status = vm_status_skiidev
            #print('vm-skidev - status: ' + str(self.status))
        elif self.name == 'CyclopseDev':
            self.status = vm_status_cypoint
            #print('CyclopseDev - status: ' + str(self.status))
        elif self.name == 'vm-BlogCypoint-01':
            self.status = vm_status_blog
        else:
            self.status = 'running'
            #print('vm-CyclopseDev - status: ' + str(self.status))
        self.update_label_position()  # Add this line to update the label position
        self.label.configure(image=self.frame)
        self.window.after(self.animation_speed, self.event, self.i_frame, self.state, self.event_number, self.x)

        
    def handle_click(self, event):
        if self.spirt_type == "cat":
            print(self.state)
            # Assuming 'angry' is a state you can check for
            if self.state == 6:  
                self.show_popup("The cat is angry! Something is wrong!")
        elif self.spirt_type == "gpt_robot":
            print(self.state)
            if self.state == 6:
                self.show_popup("The GPT robot is angry! Something is wrong!")

    def show_popup(self, message):
        popup = tk.Toplevel(self.window)
        popup.title("Status Message")
        popup.geometry(f"200x100+{self.x}+{self.y - 110}")  # Positioning above the cat
        popup.transient(self.window)  # Set to be on top of the main window

        tk.Label(popup, text=message, wraplength=180).pack(expand=True, pady=10)
        tk.Button(popup, text="Close", command=popup.destroy).pack(pady=5)

def get_resource_status(id1, name1):
    resources_json = list_resources(id1, name1)
    resources = json.loads(resources_json)
    vm_status = resources[0]['status']
    return vm_status

# background task that updates global vm_status_2 variable every 1 min:
def update_vm_status():
    if use_cloud_resource:
        while True:
            global vm_status_cypoint
            global vm_status_blog
            global vm_status_skiidev
            vm_status_skiidev = get_resource_status(subscription_id_3, resource_group_name_3)
            vm_status_cypoint = get_resource_status(subscription_id, resource_group_name)
            vm_status_blog = get_resource_status(subscription_id_2, resource_group_name_2)
            time.sleep(300)

def create_sprites():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tk window

    horizontal_distance = 100  # Distance between each sprite

    # Start the background task to get the vm status
    threading.Thread(target=update_vm_status).start()

    if use_cloud_resource:
        # Load resource information
        resources_json = list_resources(subscription_id, resource_group_name)
        resources_json_2 = list_resources(subscription_id_2, resource_group_name_2)
        resources_json_3 = list_resources(subscription_id_3, resource_group_name_3)
        resources = json.loads(resources_json)
        resources_2 = json.loads(resources_json_2)
        resources_3 = json.loads(resources_json_3)
        
        resource_names = [resources_3[0]['name'], resources[0]['name'], resources_2[0]['name']]
        resource_statuses = [resources_3[0]['status'], resources[0]['status'], resources_2[0]['status']]
    
    else:
        resource_names = ["vm-Dev01", "kubernetes-Uat-Pod01", "blobStoage-Prod01", "DB-Psql-Test01", "DB-MongoDB-Dev01", "AzureFunction-Uat01", "CDN-Internal01", "IAM-Company", "NLB-Dev01"]
        resource_statuses = ["running", "running", "running", "running", "running", "running", "running", "running", "running"]
        sprite_types = ["cloud_server", "MKS", "storage", "sql", "nosql", "cdn", "faas", "iam", "loadbalancer"]

    #sprite_types = ["cloud_server"]
    #sprite_types = ["gpt_robot"]
    #sprite_types = ["cat"]
    #sprite_types = ["MKS"]
    #sprite_types = ["storage"]
    #sprite_types = ["sql"]
    #sprite_types = ["nosql"]
    #sprite_types = ["faas"]
    #sprite_types = ["cdn"]
    #sprite_types = ["iam"]
    #sprite_types = ["loadbalancer"]
    sprites = []

    # Determine the starting horizontal position
    start_x = screen_width // (len(resource_names))
    for i, sprit_type in enumerate(sprite_types):
        horizontal_position = start_x + i * horizontal_distance
        # make sure horizontal_position is inside the screen width:
        horizontal_position = horizontal_position - 400
        if horizontal_position > screen_width:
            horizontal_position = horizontal_position - 300
        sprite = Sprite(root, sprit_type, horizontal_position, name=resource_names[i], status=resource_statuses[i])
        sprites.append(sprite)
    # Update the start position for the next VM
    start_x += screen_width // len(resource_names) + horizontal_distance

    root.mainloop()
    return sprites

create_sprites()

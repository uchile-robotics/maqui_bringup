#!/usr/bin/env python3.9
import rospy
import openai
import json
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class chat_test():
    def __init__(self):
        self.subscriber = rospy.Subscriber('/chatbot/input', String, self._callback)
        self.publisher = rospy.Publisher('/chatbot/output', String , queue_size=10)
        self.api_key = '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'
        
    def _callback(self, msg):
        with open('./memory.json', 'r+') as memory_file:

            data = json.load(memory_file)

            openai.api_key = self.api_key
            model="gpt-3.5-turbo"
            
            chat = {"role": "user", "content": msg.data}

            messages = [data["prompt"]] + data["memory"] + [chat]
                    
            reply = openai.ChatCompletion.create(model=model, messages=messages)
            print(reply["choices"][0]["message"]["content"])
            output = String()
            output.data = reply["choices"][0]["message"]["content"]
            self.publisher.publish(output)
            
            response = {"role": "assistant", "content": output.data}

            if len(data["memory"]) > 100:
                data["memory"] = data["memory"][2::]
                data["memory"].append(chat)
                data["memory"].append(response)
            else:
                data["memory"].append(chat)
                data["memory"].append(response)
            memory_file.seek(0)
            memory_file.truncate()
            json.dump(data,memory_file, indent = 4, sort_keys=True)
            memory_file.close()

def main():

    rospy.init_node('chat_test')
    chat_test()
    rospy.spin()

if __name__ == '__main__':
    main()
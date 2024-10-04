import asyncio
from kasa import SmartPlug
from datetime import datetime, time
import paho.mqtt.client as mqtt


mqtt_broker = "192.168.2.13"
mqtt_topic = "balcony/plug/status"

def publish_status(client, status):
    client.publish(mqtt_topic, status)

async def plug_control(plug):
    while True:
        client = mqtt.Client()
        client.connect(mqtt_broker)
        now = datetime.now().time() # get the current time
        turn_on_time =  time(19, 0) # 7:00 pm
        breaking_time = time(23, 59)
        mid_night_time = time (0, 0)
        turn_off_time = time(7, 30) # 7:30 am

        if now >= turn_on_time and now <= breaking_time :
            await plug.turn_on()  # turn on the light
            #print( plug.alias + " is on")
            publish_status(client, "on") # send mqtt message to node-red


        elif now >= mid_night_time and now < turn_off_time:
            await plug.turn_on() # turn on the light
            #print( plug.alias + " is on")
            publish_status(client, "on") # send mqtt message to node-red


        elif now >= turn_off_time and now < turn_on_time:
            await plug.turn_off() # turn off the light
            #print(plug.alias + " is off")
            publish_status(client, "off") # send mqtt message to node-red

        await asyncio.sleep(600) # check evey 10 mins

async def main():
    plug = SmartPlug("192.168.2.28") # plug IP address
    await plug.update() #connect to the plug
    #client = mqtt.Client()
    #client.connect(mqtt_broker)
    await plug_control(plug)



if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from kasa import SmartPlug
from datetime import datetime, time



async def plug_control(plug):
    while True:
        now = datetime.now().time() # get the current time
        turn_on_time =  time(19, 0) # 7pm
        breaking_time = time(23, 59)
        mid_night_time = time (0, 0)
        turn_off_time = time(7, 30) # 7am
        print(now)

        if now >= turn_on_time and now <= breaking_time :
            await plug.turn_on()
            print( plug.alias + " is on")

        elif now >= mid_night_time and now < turn_off_time:
            await plug.turn_on()
            print( plug.alias + " is on")

        elif now >= turn_off_time and now < turn_on_time:
            await plug.turn_off()
            print(plug.alias + " is off")

        await asyncio.sleep(600) # check evey 10 mins

async def main():
    plug = SmartPlug("192.168.2.28") # plug IP address
    await plug.update() #connect to the plug
    await plug_control(plug)



if __name__ == "__main__":
    asyncio.run(main())

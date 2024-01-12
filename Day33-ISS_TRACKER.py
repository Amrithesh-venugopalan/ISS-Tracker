import requests
from datetime import datetime
import smtplib

MY_LAT=''
MY_LONG=''
My_CITY=""
RANGE=100

my_email=""
my_pass=""
send_to=""
iss_near_you=False

#TODO get iss postiion
response1=requests.get("http://api.open-notify.org/iss-now.json")
response1.raise_for_status()

data=response1.json()
longitude=float(data["iss_position"]["longitude"])
latitude=float(data["iss_position"]["latitude"])
iss_position=(longitude,latitude)
print("iss_position-",iss_position)
print(f"{My_CITY} position-{(MY_LONG,MY_LAT)}")


#TODO find if iss is near your place


if latitude-RANGE<MY_LAT<latitude+RANGE and longitude-RANGE<MY_LONG<longitude+RANGE:
    iss_near_you=True

#TODO get sunrise and sunset time at your place
parameters={
    "lat":MY_LAT,
    "lng":MY_LONG,
    "formatted":0
}
response2=requests.get("https://api.sunrise-sunset.org/json",params=parameters)
               #or.get("https://api.sunrise-sunset.org/json?lat=9&lng=7")
response2.raise_for_status()
data=response2.json()
sunrise=int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset=int(data["results"]["sunset"].split("T")[1].split(":")[0])
print("sunrise=",sunrise,"sunset=",sunset)
time_now=datetime.now().hour
print("time_now",time_now)


#TODO find if its night time or not
if time_now>sunset:
    #TODO send email
    if iss_near_you==True:
        print(f"iss is near {My_CITY}")
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email,password=my_pass)
            connection.sendmail(from_addr=my_email,to_addrs=send_to,msg=f"Subject:Iss is nearby\n\nLook up  iss is near {My_CITY}")
            print("sending mail.....")
    else:
        print(f"sorry,iss can't be spotted now")

else:
    print("sorry,try again at night time")

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.


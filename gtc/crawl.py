
import urllib
import urllib.parse
import urllib.request
# import urllib2
import gzip
import time
from datetime import datetime, timezone, timedelta
import os


def saveFile(file_data, file_day, file_name):
    save_path = '/data/gtc/here/speed/speed_' + file_day + '/' + file_name
    # save_path = 'speed/speed_' + file_day + '/' + file_name
    file = open(save_path, 'wb')
    file.write(file_data)
    file.close()

#three corridor: (52.402679, 4.844786), (52.372413, 4.899302), (52.337565, 4.941011)
#data_url = "https://traffic.cit.api.here.com/traffic/6.1/flow.xml?bbox=60.222306%2C24.858754%3B60.142211%2C24.993980&app_id=khoT1bczS9lrR0oUURXo&app_code=Qrl9-c5-V-yWEWjoZeoK5g&responseattributes=sh%2Cfc"
#data_url = "https://traffic.cit.api.here.com/traffic/6.1/flow.json?bbox=60.222306%2C24.858754%3B60.142211%2C24.993980&units=metric&app_id=khoT1bczS9lrR0oUURXo&app_code=Qrl9-c5-V-yWEWjoZeoK5g&responseattributes=sh%2Cfc"
data_url = 'https://traffic.api.here.com/traffic/6.1/flow.json?corridor=52.402679%2C4.844786%3B52.372413%2C4.899302%3B52.337565%2C4.941011%3B1000&units=metric&app_id=XSzY753zm2sCtwrbMv5s&app_code=qpLpNMNK-x3t_BYe-S8wwQ&responseattributes=sh%2Cfc'
#nsw_data_url = "https://api.transport.nsw.gov.au/v1/roads/spatial?format=csv&q=select%20*%20from%20road_traffic_counts_station_reference%20limit%205%20"
values = {
        'Host': 'traffic.cit.api.here.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
}

data = urllib.parse.urlencode(values)
req = urllib.request.Request(
        url=data_url,
        headers=values
)


start_time = 1541631600 #the timestamp of 2018.11:8 0:00:00 for Ams
end_time = 1543618799 #the timestamp of 2018.11.30 23:59:59 for Ams
current_time = int(time.time())

print(current_time)

while (current_time < start_time):
    time.sleep(60)
    current_time = int(time.time())

print("start")

while(current_time < end_time):
    time.sleep(60)
    try:
            current_time = int(time.time())
            dt = datetime.utcnow()
            dt = dt.replace(tzinfo=timezone.utc)
            tzutc_1 = timezone(timedelta(hours=1))
            local_dt = dt.astimezone(tzutc_1)

            time_string = str(local_dt)[0:19]
            print(time_string)
            timeArray = time.strptime(time_string, '%Y-%m-%d %H:%M:%S')

            day = str(time.strftime("%d", timeArray))
            file_name = str(current_time) + ".json"
            print(file_name)

            response = urllib.request.urlopen(req, timeout=60)
            receive_data = response.read()
            print(day)

            dirt = '/data/gtc/here/speed/speed_' + day
            # dirt = 'speed/speed_' + day

            if not os.path.exists(dirt):
                os.mkdir(dirt)
            saveFile(receive_data, day, file_name)

    except Exception as e:
            print(str(e))
    






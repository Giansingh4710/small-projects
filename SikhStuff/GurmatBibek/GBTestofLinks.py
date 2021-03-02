import requests


url="http://www.gurmatbibek.com/contents.php?id="

#47-529
for i in range(530):
    res=requests.get(url+str(i))
    print(res.raise_for_status)

import urllib.request as res
import re
from collections import OrderedDict

data = res.urlopen("https://www.youtube.com/results?search_query=tbi+nr")

data = data.read().decode()


videoid = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', data)  # Added _ and - just in case



videoid = list(OrderedDict.fromkeys(videoid))
print(videoid)

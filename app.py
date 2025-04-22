import yt_dlp
from flask import Flask,render_template,request,jsonify
import json
import urllib.request
import re
from collections import OrderedDict

app = Flask(__name__)

database = ['user1','user2']
# songdetails = {'xtmNpR_xQd8E.webm':'Xcho - Ты и Я | Tik Tok Remi', 'ggG9ySCChYw.webm':'The Neighbourhood - Softcore (Official Audio'}
# playlist = {
# 'user1':['xtmNpR_xQd8E.webm','ggG9ySCChYw.webm'],
# 'user2':['ggG9ySCChYw.webm','xtmNpR_xQd8E.webm']

# }

songdetails = {}
playlist = {
}


            

ytlopts={
    'format':'bestaudio/best',
    'outtmpl':'src\\static\\audios\\%(id)s.%(ext)s',
}

@app.route('/')
def details():
    print(songdetails)
    print(playlist)
    return "Shown"


#WEBPAAGES
@app.route('/downloaderpage')
def downloaderpage():
    return render_template('downloader.html')

@app.route('/playlisterpage')
def playlisterpage():
    return render_template('playlister.html')

@app.route('/searcherpage')
def searchpage():
    return render_template('searcher.html')

#PLAYLIST ADDER
@app.route('/playlistadder',methods=['GET','POST'])
def playlistadder():
    data = request.get_json()
    print(data)
    if data['username'] not in playlist:
        playlist[data['username']]=[]
    
    if data['audiosrc'] not in playlist[data['username']]:
        playlist[data['username']].append(data['audiosrc'])
        
        print(playlist)
        return jsonify({'data':'success'})
    else:
        print(playlist)
        return jsonify({'data':'already'})

@app.route('/playlistgetter',methods=['GET','POST'])
def playlistgetter():
    data = request.get_json()
    if data['username'] not in playlist:
        return jsonify({'data':'no'})
    details = {}
    for i in playlist[data['username']]:
        details[i]=songdetails[i]
    return jsonify(details)




#ROUTERS
@app.route('/downloader',methods=['GET','POST'])
def downloader():
    data = request.get_json()
    if (data['username'] == ""):
        return jsonify({"data":"fail"})
    if(data['username'] in database):
        res = audiodownloader(data['url'])
        if res == "err":
            return jsonify({"data":"Invalid Url"})
        else:
            songdetails[res[2]]=res[0]
            return jsonify({"data":"success",'audiosrc':res[2],'videosrc':res[1],'audiotittle':res[0]})
    else:
        return jsonify({"data":"fail"})
    
def audiodownloader(url):
    with yt_dlp.YoutubeDL(ytlopts) as ydl:
        try:
            info = ydl.extract_info(url,download=True)
            tittle = info["title"]
            thumbnail = info["thumbnail"]
            audiosrc=info["id"]+'.webm'
            return tittle,thumbnail,audiosrc
        except Exception as e:
            return "err"


@app.route('/searcher',methods=['GET','POST'])
def searcher():
    res = request.get_json()
    print(res['searchid'])
    if(res['searchid']!=""):
        searchid = res['searchid']
        searchid = searchid.replace(" ", "+")
        searchid = "https://www.youtube.com/results?search_query="+searchid
        data = urllib.request.urlopen(searchid)
        data = data.read().decode()
        videoid = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', data)  
        videoid = list(OrderedDict.fromkeys(videoid))
        if videoid:
            return jsonify({"data":videoid})
        else:
            return jsonify({"data":'fail'})
    else:
        return jsonify({"data":'fail'}) 



if __name__ == "__main__":
    app.run(debug=True)

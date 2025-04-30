import yt_dlp
from flask import Flask,render_template,request,jsonify
import urllib.request
import re
from collections import OrderedDict
from flask_cors import CORS 

app = Flask(__name__)

database = ['user1','user2']
# songdetails = {'ggG9ySCChYw': ['The Neighbourhood - Softcore (Official Audio)', 'https://rr1---sn-8vq54voxpo-nm8l.googlevideo.com/videoplayback?expire=1745878903&ei=F6sPaPOQHdHGs8IPkeij8AI&ip=2402%3A3a80%3A18%3A1b36%3A8930%3A701a%3Ab2dd%3A3d0e&id=o-AKiWAoQRlq05ifr10BFbvyjvJHmuWMgzYrI9qSqqY8VL&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1745857303%2C&mh=fe&mm=31%2C29&mn=sn-8vq54voxpo-nm8l%2Csn-pqx5jxaa0a5g-h55l&ms=au%2Crdu&mv=m&mvi=1&pl=48&rms=au%2Cau&gcr=in&initcwndbps=310000&bui=AecWEAay3NsVf-0NVAcaQxtFRBe4TQPPm-rH8DoU33voXprMbKBfbpj_Ur5iDf-xb8LP4cZ6v_qNACb2&vprv=1&svpuc=1&mime=audio%2Fwebm&ns=WYMfI-8pJcGYa26aShgW6CYQ&rqh=1&gir=yes&clen=3405466&dur=210.061&lmt=1714781452797631&mt=1745856812&fvip=8&keepalive=yes&lmw=1&c=TVHTML5&sefc=1&txp=4502434&n=gm4MpqtJwUBADA&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cgcr%2Cbui%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=ACuhMU0wRQIgCkPpT6HUPV2LH7IGdksqZnn2Z2B2oMybuhrNHHTLBJACIQCZ7O_a2z9A7f7PeJDtCqPG4QKiZH2MZYkjCGBuWvb3CQ%3D%3D&sig=AJfQdSswRQIgd8EI9ynTolNg6xbVqQwceAUUJekDN8I2OTQZ804LuRYCIQD7CmMtf8svTnKBBj6MVOBaqtOjcJrifsVpM4l4kvzfRw%3D%3D']}
# playlist = {'User1': ['ggG9ySCChYw']}



songdetails = {}
playlist = {
}

CORS(app)
            

ytlopts={
    'format':'bestaudio/best',
    # 'outtmpl':'src\\static\\audios\\%(id)s.%(ext)s',
}

@app.route('/writer')
def writer():
    f = open("songdetails.txt",'w')
    f.write(str(songdetails))
    f = open("playlist.txt",'w')
    f.write(str(playlist))
    f = open("database.txt",'w')
    f.write(str(database))
    print(songdetails)
    print()
    print(playlist)
    print()
    print(database)
    return "Writed"

@app.route('/reader')
def reader():
    f = open("songdetails.txt",'r')
    songdetails = f.read
    print(songdetails)
    f = open("playlist.txt",'r')
    playlist = f.read()
    f = open("database.txt",'r')
    database = f.read()
    print(songdetails)
    print()
    print(playlist)
    print()
    print(database)
    return "Readed"


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

@app.route('/registerpage')
def registerpage():
    return render_template('register.html')


@app.route('/register',methods=['POST','GET'])
def register():
    data = request.get_json()
    if (data['username'] == ""):
        return jsonify({"data":"fail"})
    if(data['username'] in database):
        return jsonify({"data":"already"})
    else:
        database.append(data['username'])
        return jsonify({"data":"success"})


#PLAYLIST ADDER
@app.route('/playlistadder',methods=['GET','POST'])
def playlistadder():
    data = request.get_json()
    print(data['audioid'])
    if data['username'] not in playlist:
        playlist[data['username']]=[]
    if data['audioid'] not in playlist[data['username']]:
        playlist[data['username']].append(data['audioid'])
        return jsonify({'data':'success'})
    else:
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
    match = re.search(r'(?<=watch\?v=)[\w-]{11}', data['url'])
    if match == "":
        return jsonify({"data":"fail"})
    
    if match[0] in songdetails:
        temp = match[0]
        return jsonify({"data":"success",'audiosrc':songdetails[temp][1],'videosrc':'temp','audiotittle':songdetails[temp][0],'audioid':match[0]})
    if(data['username'] in database):
        res = audiodownloader(data['url'])
        if res == "err":
            return jsonify({"data":"Invalid Url"})
        else:
            songdetails[res[3]]=[res[0],res[2]]
            return jsonify({"data":"success",'audiosrc':res[2],'videosrc':res[1],'audiotittle':res[0],'audioid':res[3]})
    else:
        return jsonify({"data":"fail"})
    
def audiodownloader(url):
    with yt_dlp.YoutubeDL(ytlopts) as ydl:
        try:
            audiosrc=""
            info = ydl.extract_info(url,download=False)
            tittle = info["title"]
            thumbnail = info["thumbnail"]
            temp = info['formats']
            audioid=info["id"]
            for i in range(len(temp)):
                if(temp[i]['audio_ext']!="none" and temp[i]['audio_ext']=="webm"):
                    audiosrc=temp[i]['url']
            return tittle,thumbnail,audiosrc,audioid
        except Exception as e:
            return "err"


@app.route('/searcher',methods=['GET','POST'])
def searcher():
    res = request.get_json()
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

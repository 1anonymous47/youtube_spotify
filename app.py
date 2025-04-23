import yt_dlp
from flask import Flask,render_template,request,jsonify
import json
import urllib.request
import re
from collections import OrderedDict

app = Flask(__name__)

database = ['user1','user2']
songdetails = {'tmNpR_xQd8E': ['Xcho - Ты и Я | Tik Tok Remix', 'https://rr1---sn-8vq54voxpo-nm8e.googlevideo.com/videoplayback?expire=1745411352&ei=uIgIaNOGJcucssUPjsebqA4&ip=2402%3A3a80%3A48%3Abe99%3A4c60%3A1e67%3Aa7bb%3A9c53&id=o-APrjgE-rYrYQsfKrByw__HfhYuj0hSXfH07Hk-B9Nt2p&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1745389752%2C&mh=J-&mm=31%2C29&mn=sn-8vq54voxpo-nm8e%2Csn-pqx5jxaa0a5g-h55l&ms=au%2Crdu&mv=m&mvi=1&pl=48&rms=au%2Cau&initcwndbps=456250&bui=AccgBcOXjvq-ht5Dps_VGMsTIX2sJ8iKYje_xzd2bauyhLGEzUHPhn5NQONaRIiIAY90vddASWCXmcDn&vprv=1&svpuc=1&mime=audio%2Fwebm&ns=uIFeQcW2oAy93H2oi3u6pd8Q&rqh=1&gir=yes&clen=2867386&dur=182.121&lmt=1734846140830605&mt=1745389258&fvip=5&keepalive=yes&lmw=1&c=TVHTML5&sefc=1&txp=5532434&n=MBrlHNVHduEN4A&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cbui%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=ACuhMU0wRAIgS4-VCwBEh9y59CsSr3NRYwKLDiqy9aULIvtnLzcrv4MCIBDs-VBG5hcr5Ri2AmiNLn06corN1R4AlXRtcq0dk0vG&sig=AJfQdSswRAIgPsHFWK8VR150I52ex_43FXR_4cykcAQJCBftcGjvDfQCIGHlx1In0QyDYALKCbRtsYj-78C78OOWUsw_z8Cna7FN'],
               'ggG9ySCChYw': ['The Neighbourhood - Softcore (Official Audio)', 'https://rr1---sn-8vq54voxpo-nm8l.googlevideo.com/videoplayback?expire=1745412393&ei=yYwIaPziGYP0s8IP1tjrsQU&ip=2402%3A3a80%3A48%3Abe99%3A4c60%3A1e67%3Aa7bb%3A9c53&id=o-AA5R1PeX8C0t7hIoAF5NugMF7OdqGrLbiCs9pt41O4QK&itag=251&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1745390793%2C&mh=fe&mm=31%2C29&mn=sn-8vq54voxpo-nm8l%2Csn-pqx5jxaa0a5g-h55l&ms=au%2Crdu&mv=m&mvi=1&pl=48&rms=au%2Cau&gcr=in&initcwndbps=510000&bui=AccgBcP6cwjFhUhul7wZrSi0ijfoI3o39I2rs7iHHJH_nbbEJDMYPe8qXvoxasSZ1aM1NMBMkLgSJGrA&vprv=1&svpuc=1&mime=audio%2Fwebm&ns=plkxxeo9SrDhOepz-i5GVJ8Q&rqh=1&gir=yes&clen=3405466&dur=210.061&lmt=1714781452797631&mt=1745390211&fvip=8&keepalive=yes&lmw=1&c=TVHTML5&sefc=1&txp=4502434&n=h5hUj-36MOMD9A&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cgcr%2Cbui%2Cvprv%2Csvpuc%2Cmime%2Cns%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=ACuhMU0wRQIgEUecRiCQssjgyP1VZzJ48FYzkLyWnR2wv_Nwq6HwIk4CIQCtls34NAn90QdyuymwGqkw3BiZdBNp_QVGSjQbCdAp2Q%3D%3D&sig=AJfQdSswRQIhALYWKHkNFZc6PpmuKQuHRuGN86AL08EMLSyQG31wliIpAiAaZu5sIxQ_V1Ow7ua-Sz9Ix6r_CrK3DvMks3NIAOsOsw%3D%3D']}
# playlist = {
# 'user1':['xtmNpR_xQd8E.webm','ggG9ySCChYw.webm'],
# 'user2':['ggG9ySCChYw.webm','xtmNpR_xQd8E.webm']

# }

# songdetails = {}
playlist = {
}


            

ytlopts={
    'format':'bestaudio/best',
    'outtmpl':'src\\static\\audios\\%(id)s.%(ext)s',
}

@app.route('/')
def details():
    print(songdetails)
    print()
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

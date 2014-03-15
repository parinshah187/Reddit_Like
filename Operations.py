from bottle import get, post, route, put, delete,run,request, response, abort
from pymongo import Connection,database, MongoClient
from locale import str

client=MongoClient()
db = client['test']
reddit = db['test']
count = 0

@route('/topics',method=['POST'])
def create_topic():
#    print "hello in add"
    global count
    count = count+1
    topicid = str(count)
    print 'count : ',topicid
    data={
          'topicid':topicid,
          'topicname':request.json['topicname'],
          'desc':request.json['desc'],
          'author':request.json['author'],
          'comments':[]
          }
    reddit=db.reddit
    reddit.insert(data)
    print data
    #print response
    res=""
    res=data
    return "New Topic has been added !\n" , view_topic(topicid)




@route('/topics/<topicID>', method='DELETE')
def delete_topic(topicID):
    topic= topicID
    post = {"topicid": topicID}
    reddit=db.reddit
    document = db.reddit.remove(post)
    return "Topic-",topicID," is deleted!\n",list_topics()


@route('/topics')
def list_topics():
    # Code for mongodb to retrieve list of topics will come here.
    print "in list_topics()"
    #reddit=db['test']
    document = db.reddit.find()
    count = db.reddit.count()
    res="Topic-ID\tTopic-Name\tAuthor\n"
    print 'count : ',count
    print type(document)
    try:
        for i in range(count):
            record = document.next()
            res=res+"\t"+record["topicid"]+"\t"+record["topicname"]+"\t\t"+record["author"]
            res+="\n"
    except StopIteration:
        print 'Exception Caught !'
    print res
    return res


@route('/topics/<topicID>')
def view_topic(topicID):
  
    topic= topicID
    post = {"topicid": topicID}
    reddit=db.reddit
    document = db.reddit.find(post)
    count = db.reddit.count()
    print count
    res = "Topic-ID : "
    try:
        for i in range(count):
            record = document.next()
            res=res+record["topicid"]+"\nTopic-Name : "+record["topicname"]+"\nTopic-desc: "+record["desc"]+"\nAuthor : "+record["author"]+"\nComments : \n"
            comments = record["comments"]
            if(comments!='\0'):
                for i in range(len(comments)):
                    comment=comments[i]
                    res=res+"\t"+comment["comment"]+"\t(Author : "+comment["author"]+")\n"
    except StopIteration:
        print 'Exception Caught !'
    print res
    return res


@route('/topics/<topicid>/comments',method='POST')
def comment_on_topic(topicid):
    print topicid 
    data={
          'author':request.json['author'],
          'comment':request.json['comment']
          }
    print data["comment"]," ",data["author"]
    document = db.reddit.find({topicid:topicid})
    topic= topicid
    post = {"topicid": topicid}
    document = db.reddit.find(post)
    count = db.reddit.count()
    db.reddit.update( {"topicid": topicid}, {"$push": {"comments": {"author":data["author"],"comment":data["comment"]}}} )
    return "Your comment is posted ! Please check !"+view_topic(topicid)

run(host='0.0.0.0', port=8080, debug=True)
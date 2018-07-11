import redis

r = redis.Redis(host='db.bobdu.cc', decode_responses=True)

print(r.keys())

userList = r.keys()

for user in userList:
    if user != 'id':
        print(r.hgetall(user))
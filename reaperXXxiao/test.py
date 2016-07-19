# from spiders.MongoUtils import *
# db = MongoUtils.getDb()
# coll_whole = MongoUtils.getCol(db,'album_whole')
# list = coll_whole.find({},{"key_words":1})
# index = 0
# keyWords = set()
# for item in list:
#     index = index + 1
#     for x in item['key_words'].encode().split(', '):
#         keyWords.add(x)
# print index,len(keyWords)
# for item in keyWords:
#     print item
#
# import re
# url = 'http://m.xxxiao.com/wp-content/uploads/sites/3/2016/05/m.xxxiao.com_b3516455663fcf4a8e3339d07ce7ff69-1024x683.jpg'
# replace_reg = re.compile(r'-(\d+)x(\d+)')
# for x in replace_reg.findall(url):
#     print x[0],x[1]

# import time
# print time.strftime("%Y%m%d%H%M", time.localtime())

import re
str = "12{b"
rex = re.compile(".*[~`!@#$%^&*()_+{}\[\]\"']+.*")
match = rex.match(str)
print match
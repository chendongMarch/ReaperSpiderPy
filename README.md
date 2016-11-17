# 爬虫

## 数据库设计

## album_recommend
推荐专辑，首页推荐的分类下的专辑
```
album_type : 推荐的类型,分new,xinggan,shaonv,mrxt,wmxz,wallpaper
album_link : 指向专辑详情的链接,通过这个链接作为主键,可以查询,这个专辑的详情
album_cover : 专辑的封面,图片链接
album_desc : 专辑的描述
time_stamp:时间戳
```

## album_whole
全部专辑 数据库集合,抽取的所有爬到的专辑列表
```
album_link : 指向专辑详情的链接,通过这个链接作为主键,可以查询,这个专辑的详情
key_words : 关键字
album_cover : 专辑的封面,图片链接
album_desc : 专辑的描述
time_stamp:时间戳
```

## album_detail
详情 数据库集合,每一条字段存储一张图片
```
width: 宽度
height: 高度
album_link : 属于哪一个专辑
photo_src : 图片链接
album_link: 专辑链接
photo_src: 图片链接
time_stamp:时间戳
```
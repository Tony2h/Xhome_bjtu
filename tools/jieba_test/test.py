import jieba
jieba.load_userdict("user_dict.txt")
seg_list = jieba.cut("我想听宇多田ヒカル",cut_all = False)
print(",".join(seg_list))

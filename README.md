# Xhome_bjtu

*1.训练NLU*
python -m rasa_nlu.train --data ./data/music_nlu_data.json --config ivr_chatbot.yml --path models --fixed_model_name demo --project ivr_nlu

python -m rasa_nlu.train --data ./data/music_nlu_data.json \
    --config ivr_chatbot.yml \
    --path models \
    --fixed_model_name demo \
    --project ivr_nlu
#训练数据在路径data/xxx,配置文件在xxx.yml,训练好的数据在path(models/xxx)/
 /project(ivr_nlu)/fixed_model_name(demo)里

2.服务器检验抽取实体
开启服务器监听:
python -m rasa_nlu.server -c ivr_chatbot.yml --path models
发送请求:
curl -XPOST localhost:5000/parse -d '{"q":"我想听薛之谦的歌", "project": "ivr_nlu", "model": "demo"}' | python -mjson.tool | jq

3.在线训练
python -m rasa_core.train \
  --online -o models/dialogue \
  -d domain.yml -s stories.md \
  --endpoints endpoints.yml

4.训练对话
python -m rasa_core.train -d domain.yml -s data/stories.md -o models/current/dialogue --epochs 200

5.Debug
python -m rasa_core.run -d models/dialogue -u models/ivr_nlu/demo --debug

6.python trainsfer_raw_to_rasa.py 转换

7.关于jieba
import jieba
seg_list = jieba.cut("给我来一首邓紫琪的夜空中最亮的星",cut_all = False)

8.online-train
./data/music_story.md

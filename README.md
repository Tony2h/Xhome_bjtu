# Xhome_bjtu

**1.训练NLU**   
python bot.py train-nlu  
python -m rasa_nlu.train --data ./data/music_nlu_data.json --config ivr_chatbot.yml --path models --fixed_model_name demo --project ivr_nlu

#训练数据在路径data/xxx,配置文件在xxx.yml,训练好的数据在path(models/xxx)/project(ivr_nlu)/fixed_model_name(demo)里

**2.服务器检验抽取实体**   
开启服务器监听:  
python -m rasa_nlu.server -c ivr_chatbot.yml --path models
发送请求:  
curl -XPOST localhost:5000/parse -d '{"q":"我想听薛之谦的歌", "project": "ivr_nlu", "model": "demo"}' | python -mjson.tool | jq

**3.在线训练**  
python bot.py online-train  
python -m rasa_core.train --online -o models/dialogue -d domain.yml -s stories.md --endpoints endpoints.yml

**4.训练对话**  
python bot.py train-dialogue  
python -m rasa_core.train -d domain.yml -s data/stories.md -o models/current/dialogue --epochs 200

**5.Debug**    
python -m rasa_core.run -d models/dialogue -u models/ivr_nlu/demo --debug

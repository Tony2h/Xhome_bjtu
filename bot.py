# -*- coding: UTF-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings
import pymysql
import random  

from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.events import SlotSet
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

def search_sql(item,choice):
    #打开数据库连接
    db = pymysql.connect("localhost","root","123456","songDB")
    #使用cursor方法获取操作游标
    cursor = db.cursor()
    #SQL查询语句
    if choice == 1:
        sql = "select * from song where name = \'{}\' and singer = \'{}\'".format(item[0],item[1])
    elif choice == 2:
        sql = "select * from song where name = \'{}\'".format(item[0])
    elif choice == 3:
        sql = "select * from song where singer = \'{}\' and style = \'{}\'".format(item[1],item[2])
    elif choice == 4:
        sql = "select * from song where singer = \'{}\'".format(item[1])
    elif choice == 5:
        sql = "select * from song where style = \'{}\'".format(item[2])
    try:
        #执行SQL查询语句
        cursor.execute(sql)
        #获取所有记录列表
        results = cursor.fetchall()
        songlist = []
        for row in results:
            songlist.append({'name':row[0],'singer':row[1],'style':row[2]})
        db.close()
        songlen = len(songlist)
        i = random.randint(0,songlen - 1)
        return songlist[i]
    except:
        print("Error: unable to fetch data")
        
class ActionSearchConsume(Action):
    def name(self):
        return 'action_search_consume'

    def run(self, dispatcher, tracker, domain):
        item = []
        item.append(tracker.get_slot("name"))# 歌名
        item.append(tracker.get_slot("singer"))# 歌手
        item.append(tracker.get_slot("style"))# 风格
        if item[0]:
            if item[1]:
                choice = 1
                song = search_sql(item,choice)
                return dispatcher.utter_message("好哒，正在为您播放{}的歌曲{},风格:{}".format(item[1], item[0],song['style']))
            else:
                choice = 2
                song = search_sql(item,choice)
                return dispatcher.utter_message("好哒,为您播放歌曲{}。歌曲名：{},歌手：{}".format(item[0],song['name'],song['singer']))
        elif item[1]:
            if item[2]:
                # 已知歌手和风格，随机选一个歌名
                choice = 3
                song = search_sql(item,choice)
                return dispatcher.utter_message("好哒，为您随机播放{}的一首{}风格的歌曲{}。".format(song['singer'],song['style'],song['name']))
            else:
               #已知歌手，随机选
                choice = 4
                song = search_sql(item,choice)
                return dispatcher.utter_message("好哒，正在为您随机播放{}的一首{}的歌曲。".format(song['singer'],song['name']))
        elif item[2]:
            # 已知风格，随机选
            choice = 5
            song = search_sql(item,choice)
            return dispatcher.utter_message("好哒，正在为您播放一首{}风格的歌曲{}。".format(song['style'],song['name']))
        else:
            return dispatcher.utter_template("utter_default",tracker)
            
class ActionSearchListen(Action):
    def name(self):
        return 'action_search_listen'
    
    def run(self,dispatcher,tracker,domain):
        item1 = tracker.get_slot("name")
        item2 = tracker.get_slot("singer")
        item3 = tracker.get_slot("style")
        if item1 == None:
            return dispatcher.utter_template("utter_ask_name",tracker)
        if item2 == None:
            return dispatcher.utter_template("utter_ask_singer",tracker)
        if item3 == None:
            return dispatcher.utter_template("utter_ask_style",tracker)

def train_dialogue(domain_file="music_domain.yml",
                   model_path="models/dialogue",
                   training_data_file="data/music_story.md"):
    from rasa_core.policies.fallback import FallbackPolicy
    from rasa_core.policies.keras_policy import KerasPolicy
    from rasa_core.agent import Agent

    fallback = FallbackPolicy(fallback_action_name="utter_default",
                          core_threshold=0.3,
                          nlu_threshold=0.3)
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy(),fallback])

    training_data = agent.load_data(training_data_file)
    agent.train(
        training_data,
        epochs=200,
        batch_size=16,
        augmentation_factor=50,
        validation_split=0.2
    )

    agent.persist(model_path)
    return agent

def train_nlu():
    from rasa_nlu.training_data import load_data
    from rasa_nlu import config
    from rasa_nlu.model import Trainer

    training_data = load_data("data/music_nlu_data.json")
    trainer = Trainer(config.load("ivr_chatbot.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist("models/", project_name="ivr_nlu", fixed_model_name="demo")

    return model_directory

def run_ivrbot_online(input_channel=ConsoleInputChannel(),
                      interpreter=RasaNLUInterpreter("models/ivr_nlu/demo"),
                      domain_file="music_domain.yml",
                      training_data_file="data/music_story.md"):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy()],
                  interpreter=interpreter)

    training_data = agent.load_data(training_data_file)
    agent.train_online(training_data,
                       input_channel=input_channel,
                       batch_size=16,
                       epochs=200,
                       max_training_samples=300)

    return agent


def run(serve_forever=True):
    agent = Agent.load("models/dialogue",
                       interpreter=RasaNLUInterpreter("models/ivr_nlu/demo"))

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
    return agent


if __name__ == "__main__":
    logging.basicConfig(level="INFO")

    parser = argparse.ArgumentParser(
        description="starts the bot")

    parser.add_argument(
        "task",
        choices=["train-nlu", "train-dialogue", "run", "online-train"],
        help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
    elif task == "run":
        run()
    elif task == "online-train":
        run_ivrbot_online()
    else:
        warnings.warn("Need to pass either 'train-nlu', 'train-dialogue' or "
                      "'run' to use the script.")
        exit(1)

import urllib
import json
from urllib.request import urlopen
import requests


with open('e8wQHAlz.json', 'rb') as json_file:
    json_data = json.load(json_file)


buckets = pd.DataFrame(json_data['lists']).loc[:, ['id', 'name']].set_index('id')
columns = ['id', 'idList', 'closed', 'desc', 'name', 'labels','dateLastActivity']
cards = pd.DataFrame(json_data['cards']).loc[:, columns]
cards_num = len(cards['name'].values)

cards = pd.merge(cards, buckets, how='left', left_on='idList', right_on='id', 
                 suffixes=('_card', '_list'), right_index=True).drop(['idList'], axis=1)
                 
columns = ['idMemberCreator','data','type','date']
actions = pd.DataFrame(json_data['actions']).loc[:, columns]

members = pd.DataFrame(json_data['members']).loc[:, ['id', 'username']].set_index('id')
actions = pd.merge(actions, members, how='left',
                   left_on='idMemberCreator', right_on='id',
                   suffixes=('_actions', '_members')).drop(['idMemberCreator'], axis=1)
                   
                   
actions['card_id'] = ''
actions['changed'] = ''
actions['old'] = ''
actions['new'] = ''
actions['comment'] = ''
actions['Date'] = ''


for row in range(len(actions)):
    try:
        
        actions.loc[row, 'card_id'] = actions.loc[row, 'data']['card']['id']
        actions.loc[row, 'changed'] = list(actions.loc[row, 'data']['old'].keys())[0]
        actions.loc[row, 'old'] = list(actions.loc[row, 'data']['old'].values())
        # get value of what was changed to use it after
        changed = list(actions.loc[row, 'data']['old'].keys())[0]
        actions.loc[row, 'new'] = actions.loc[row, 'data']['card'][changed]
        actions.loc[row, 'card_id'] = actions.loc[row, 'data']['card']['date']
    except:
        pass
        
actions = pd.merge(actions, cards, how='left',
                   left_on='card_id', right_on='id',
                   suffixes=('_actions', '_cards'))
                   
actions=actions.replace({'old':{65535:'Request', 131071:'To Do', 196607:'On Hold', 262143:'Done', 327679: 'Approve' }
, 'new':{65535:'Request', 131071:'To Do', 196607:'On Hold', 262143:'Done', 327679: 'Approve'} })


actions.to_excel("Trello.xlsx")

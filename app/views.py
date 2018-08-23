from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app import img
from app import idioms
from app import example
from app import meaning
from app import quiz
from app import butter
import json
import emoji
import sqlite3
import random

emo1 = emoji.emojize(':cookie:')
emo2 = emoji.emojize(':heavy_check_mark:')
emo3 = emoji.emojize(':books:')
emo4 = emoji.emojize(':bomb:')
emo5 = emoji.emojize(':tongue:')
emo6 = emoji.emojize(':droplet:')
emo7 = emoji.emojize(':trophy:')

def keyboard(request):

	return JsonResponse(
		{
			'type': 'buttons',
			'buttons': ['오늘의 이디엄 (미국)', '오늘의 이디엄 (영국)', '오늘의 퀴즈', '오늘의 버터']
		}
	)

@csrf_exempt
def message(request):
	button_info = ['오늘의 이디엄 (미국)', '오늘의 이디엄 (영국)', '오늘의 퀴즈', '오늘의 버터']	

	json_str = (request.body).decode('utf-8')
	received_json = json.loads(json_str)
	content_name = received_json['content']
	content_type = received_json['type']
	user_name = received_json['user_key']	

	con = sqlite3.connect("./DB/userquiz.db")
	cur = con.cursor()	

	if content_name == "오늘의 이디엄 (미국)":
		text = idioms.get_usa()
		url = img.get_img(text)
		mean = meaning.get_meaning(text)
		ex = example.get_usa_example(text)

		return JsonResponse(
			{
				'message': {
					'text': emo1 + 'idioms' + emo1 + '\n: ' + text + '\n\n' + emo2  +  'meaning' + emo2 + '\n: ' + mean + '\n\n' + emo3 +'example' + emo3 + '\n: ' + ex,
					'photo':{
						'url': url,
						'width': 300,
						'height': 200
					},
				},
				'keyboard': {
					'type': 'buttons',
					'buttons': button_info
				}
			}

		)

	elif content_name == "오늘의 이디엄 (영국)":
		text = idioms.get_uk()
		url = img.get_img(text)
		mean = meaning.get_meaning(text)
		ex = example.get_uk_example(text)

		return JsonResponse(
			{
				'message': {
					'text': emo1 + 'idioms' + emo1 + '\n: ' + text + '\n\n' + emo2  +  'meaning' + emo2 + '\n: ' + mean + '\n\n' + emo3 +'example' + emo3 + '\n: ' + ex,
					'photo':{
						'url': url,
						'width': 300,
						'height': 200
					},
				},
				'keyboard': {
					'type': 'buttons',
					'buttons': button_info
				}
			}

		)


	elif content_name == "오늘의 버터":
		url = butter.get_butter()

		return JsonResponse(
			{
				'message': {
					'text': '오늘의 버터는 뭘까요 ?',
					'photo':{
						'url': url,
						'width': 300,
						'height': 200
					},
				},
				'keyboard': {
					'type': 'buttons',
					'buttons' : button_info
				}
			}

		)
	
	elif content_type != 'text':
		return JsonResponse(
			{
				'message':{
					'text': '텍스트만 입력 가능합니다.\n텍스트로 답해주세요!'
				},
				'keyboard':{
					'type': 'buttons',
					'buttons': button_info
				}
			}
		)
	
	elif content_name == "오늘의 퀴즈":
		text = quiz.get_line()
		answer = quiz.modify_line(text)
		quizlet = quiz.quiz(answer)
		mean = meaning.get_meaning(text)
		
		cur.execute("DELETE FROM user_quiz WHERE Name = (:name)", {"name": user_name})
		cur.execute("INSERT into user_quiz(Name, Quiz, Hint) VALUES (?,?,?)", (user_name, answer, quizlet))
		
		con.commit()
		con.close()

		return JsonResponse(
			{
				'message': {
					'text': emo5+ 'Quiz'+emo5+ '\n' + quizlet + '\n\n\n' + emo4 + 'Hint' +emo4 + '\n' + mean
				},
				'keyboard': {
					'type': 'text'
				}
			}

		)
#	cur.execute("SELECT Quiz from user_quiz WHERE Name = (:name)", {"name": user_name})
#	confirm = cur.fetchall()

	
	elif content_name not in button_info:
		cur.execute("SELECT Quiz from user_quiz WHERE Name = (:name)", {"name": user_name})		
		answer = cur.fetchone()[0]
	
		cur.execute("SELECT Hint from user_quiz WHERE Name = (:name)", {"name": user_name})
		hint = cur.fetchone()[0]

		count = 0

		for c in hint:
			if c == '_':
				count += 1		
		if content_name.lower() == answer:
			return JsonResponse(
				{
					'message': {
						'text': emo7 +  '정답입니다!' + emo7+ '\n\n다른 퀴즈도 풀어보는건 어떠세요?'
					},
					'keyboard': {
						'type' : 'buttons',
						'buttons': button_info
					}
				}
			)
		if count > 1:
			idx = hint.index('_')		
			hint = answer[:idx+1] + hint[idx+1:]		
	
			cur.execute("DELETE FROM user_quiz WHERE Name = (:name)", {"name": user_name})
			cur.execute("INSERT into user_quiz(Name, Quiz, Hint) VALUES (?,?,?)", (user_name, answer, hint))
			con.commit()
			con.close()

		else:
			return JsonResponse(
				{
					'message':{
						'text': 'Hint 기회가 모두 소진되었습니다.\n\n정답은 "' + answer + '" 이었습니다!\n\n버터와 함께 더 공부해보아요!'
					},
					'keyboard':{
						'type': 'buttons',
						'buttons': button_info
					}
				}
			)		

			
		if content_name != answer:
			return JsonResponse(
				{
					'message':{
						'text': '오답입니다'+ emo6  + '\n\n' + emo4  + 'Hint' + emo4 + '\n' + str(hint) + '\n\n다른 퀴즈를 풀고 싶으시면\n"오늘의 퀴즈"를 입력해주세요!'
					},
					'keyboard': {
						'type': 'text'
					}
				}
			)

	

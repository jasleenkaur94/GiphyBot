from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import requests
import json

from giphy import get_gif

# Create your views here.

def testing(request):
	return HttpResponse("Testing successful...")


class CommonUrl(generic.View):

	def get(self, request, *args, **kwargs):
		return HttpResponse("Hello")


class ChatBot(generic.View):

	def get(self, request, *args, **kwargs):
		print self.request.GET
		if self.request.GET.get('hub.verify_token') == '123456789':
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		message = json.loads(self.request.body.encode('utf-8'))

		for entry in message['entry']:
			for msg in entry.get('messaging'):
				print msg.get('message')

				if "text" in msg.get('message').keys():
					reply_to_message(msg.get('sender')['id'], msg.get('message')['text'])
				else:
					print "Some Error!!!"

		return HttpResponse("None")


def reply_to_message(user_id, message):
	access_token = 'EAAF8xZAqnxxMBAL41sCiZB7X3NXoZC1UNU8kZAmqNZASVtrHI4X7UkQM9GXJQfXb8R2yQ9KR5uZBZABSklRFyueQEbnttJ9IFcwzYsdEHBwSjZCcXLxlTpghPb4U5NQprcGKoyGTBJXsJpICo3mNfAh5KiIRbg9yIgg1crBDo0htxQZDZD'
	url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token

	resp, attach_link = generate_response(message)
	#send_resp = {"recipient":{"id":user_id}, "message":{"text":resp, "attachment":{"type":"image", "payload":{"url": attach_link}}}}
	send_resp = {"recipient":{"id":user_id}, "message":{"attachment":{"type":"image", "payload":{"url": attach_link}}}}
	response_msg = json.dumps(send_resp)
	status = requests.post(url, headers={"Content-Type": "application/json"},data=response_msg)
	print status.json()

def generate_response(msg):
	if 'search' in msg:
		q = ''.join([ix for ix in msg.split('search', 1)[1]])
	else:
		q = msg
	url_to_send, gif_link = get_gif(q)
	print gif_link
	return url_to_send, gif_link
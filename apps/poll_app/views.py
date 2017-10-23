# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, Poll, Vote
from django.contrib import messages

def index(req):
	return render(req, "poll_app/index.html")

def new_user(req):
	valid = User.userManager.register(
		req.POST['username'],
		req.POST['password'],
		req.POST['confirm'],
	)
	if valid[0]:
		req.session["user"] = {
			"id": valid[1].id,
			"username": valid[1].username
		}
		return redirect('/polls')
	else:
		for error in valid[1]:
			messages.add_message(req, messages.ERROR, error)
	return redirect('/')

def new_session(req):
	valid = User.userManager.login(
		req.POST['username'],
		req.POST['password']
	)
	if valid[0]:
		req.session["user"] = {
			"id": valid[1].id,
			"username": valid[1].username
		}
		return redirect('/polls')
	else:
		for error in valid[1]:
			messages.add_message(req, messages.ERROR, error)
	return redirect('/')

def logout(req):
	req.session.clear()
	return redirect('/')

def polls(req):
	if 'user' not in req.session:
		return redirect('/')
	if req.method == 'GET':
		context = {
			"polls": Poll.objects.all(),
			"votes": Vote.voteManager.filter(voter_id=req.session["user"]["id"])
		}
		return render(req, "poll_app/polls.html", context)
	elif req.method == 'POST':
		Poll.objects.create(
			question=req.POST["question"],
			option1=req.POST["option1"],
			option2=req.POST["option2"],
			option3=req.POST["option3"],
			creator_id=req.session["user"]["id"]
		)
		return redirect('/polls')

def new_poll(req):
	if 'user' not in req.session:
		return redirect('/')
	return render(req, "poll_app/new_poll.html")

def vote(req, id):
	if 'user' not in req.session:
		return redirect('/')
	if req.method == 'GET':
		poll = Poll.objects.get(id=id)
		results = {
			poll.option1: 0,
			poll.option2: 0,
			poll.option3: 0,
		}

		voted = False
		for vote in Vote.voteManager.filter(voter_id=req.session["user"]["id"]):
			if vote.selection == 1:
				results[poll.option1] += 1
			elif vote.selection == 2:
				results[poll.option2] += 1
			elif vote.selection == 3:
				results[poll.option3] += 1
				
			if vote.poll.id == int(id):
				voted = True

		return render(req, "poll_app/vote.html", {"poll": poll, "voted": voted, "results": results})
	elif req.method == 'POST':
		Vote.voteManager.vote(
			int(req.POST["selection"]),
			req.session["user"]["id"],
			int(id)
		)
		return redirect("/polls")

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt
	
class UserManager(models.Manager):
	def register(self, username, password, confirm):

		errors = []

		if len(username) < 2:
			errors.append("Username must be 2 characters or longer!")
		elif len(User.userManager.filter(username=username)) > 0:
			errors.append("Username already exists!")
		if len(password) < 8:
			errors.append("Password must be 8 characters or longer!")
		if not password == confirm:
			errors.append("Password must match Confirm Password!")

		if len(errors) > 0:
			return (False, errors)
		else:
			pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			user = User.userManager.create(username=username, pw_hash=pw_hash)
			return (True, user)

	def login(self, username, password):

		errors = []

		if len(username) < 2:
			errors.append("Username must be 2 characters or longer!")
		if len(password) < 8:
			errors.append("Password must be 8 characters or longer!")

		user = User.userManager.filter(username=username)

		if len(user) == 0:
			errors.append("Username not found!")

		if len(errors) > 0:
			return (False, errors)
		else:
			if bcrypt.checkpw(password.encode(), user[0].pw_hash.encode()):
				return (True, user[0])
			else:
				return (False, ["Incorrect Password!"])

class User(models.Model):
	username = models.CharField(max_length = 255)
	pw_hash = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	userManager = UserManager()

	def __repr__(self):
		return "<User: {} {} {}>".format(
			self.username,
			self.created_at,
			self.updated_at
		)

class Poll(models.Model):
	question = models.CharField(max_length = 255)
	option1 = models.CharField(max_length = 255)
	option2 = models.CharField(max_length = 255)
	option3 = models.CharField(max_length = 255)
	creator = models.ForeignKey(User, related_name="polls")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __repr__(self):
		return "<Poll: {} {} {}>".format(
			self.question,
			self.created_at,
			self.updated_at
		)

class VoteManager(models.Manager):
	def vote(self, selection, voter, poll):
		if len(Vote.voteManager.filter(voter_id=voter).filter(poll_id=poll)) == 0:
			Vote.voteManager.create(selection=selection, voter_id=voter, poll_id=poll)
			return True
		else:
			return False

class Vote(models.Model):
	selection = models.IntegerField()
	voter = models.ForeignKey(User, related_name="voters")
	poll = models.ForeignKey(Poll, related_name="votes")

	voteManager = VoteManager()

import os
import base64
import sqlite3

if not os.path.exists('files/'):
	os.mkdir('files/')

class Database:
	def __init__(self):
		if not os.path.exists('files/credentials.db'):
			self.conn = sqlite3.connect('files/credentials.db')
			self.conn.execute('''CREATE TABLE credentials (
					username text NOT NULL,
					email text NOT NULL,
					password text NOT NULL)
			''')
			print('database created successfully')
		else:
			self.conn = sqlite3.connect('files/credentials.db')

		self.cursor = self.conn.cursor()

	def show_table(self):
		self.cursor.execute('''SELECT name from sqlite_master where type="table"''')
		print(self.cursor.fetchall())

	def insert_credential(self, values):
		query = "INSERT INTO credentials VALUES (?,?,?)"
		try:
			self.cursor.execute(query, values)
			self.conn.commit()
			return 'success'
		except:
			return 'error'

	def fetch_credential(self, email):
		query = "SELECT * FROM credentials WHERE email=?"
		try:
			self.cursor.execute(query, (email,))
			data = self.cursor.fetchone()
			return data
		except:
			return 'error'

	def fetch_all_creds(self):
		query = "SELECT * FROM credentials"
		try:
			self.cursor.execute(query)
			data = self.cursor.fetchall()
			return data
		except:
			return 'error'

def encode_password(password):
	return base64.b64encode(password.encode('utf-8'))

def decode_password(password):
	return base64.b64decode(password).decode("utf-8")
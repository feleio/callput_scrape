import MySQLdb
from datetime import datetime

import socket

agent = MySQLdb.connect(	host='127.0.0.1',
							port=33060,
							user='homestead',
							passwd='secret',
							db='fatlok_callput',
							charset='utf8',
							use_unicode=True )
agent.autocommit(True)
cursor = agent.cursor()

def remove_all_warrants_and_lasts():
	sql = 'DELETE FROM warrants'
	cursor.execute(sql)

	sql = 'DELETE FROM lasts'
	cursor.execute(sql)

def is_warrant_name_exist(warrant_name):
	global cursor
	sql = "SELECT EXISTS( SELECT 1 FROM warrants WHERE name = %s )"
	cursor.execute(sql, [warrant_name])
	return cursor.fetchone()[0]

def add_warrant(name, code, issuer, underlying, call_or_put, warrant_type, maturity, strike, ent):
	global cursor
	values = [ unicode(name), unicode(code), unicode(issuer), unicode(underlying), call_or_put, unicode(warrant_type), unicode(maturity), unicode(strike), unicode(ent) ]
	sql = 	u"INSERT INTO warrants (name,code,issuer,underlying,call_or_put,warrant_type,maturity.strftime('%%Y-%%m-%%d %%H:%%M:%%S'),strike,ent,created_at,updated_at) "\
			"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now())"
	print values
	cursor.execute(sql, values)
	return cursor.lastrowid

def add_price(warrant_id, last_at, premium_percent, eff_gearing_percentm, iv_percent, delta, outstanding, turnover):
	global cursor
	values = [ unicode(name), unicode(link), unicode(img_link), group_id ]
	sql = 	u"INSERT INTO lasts (warrant_id,last_at.strftime('%%Y-%%m-%%d %%H:%%M:%%S'),premium_percent,eff_gearing_percentm,iv_percent,delta,outstanding,turnover,created_at,updated_at) "\
			"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now())"

	cursor.execute(sql, values)
	return cursor.lastrowid


def set_time_zone(time_zone_str):
	global cursor
	agent.time_zone = time_zone_str




def is_group_exist(link):
	global cursor
	sql = "SELECT EXISTS( SELECT 1 FROM groups WHERE link = %s )"
	cursor.execute(sql, [link])
	return cursor.fetchone()[0]

def add_group(name, link):
	global agent
	values = [name, link]
	sql = 	u"INSERT INTO groups (name,link,created_at,updated_at) "\
			"VALUES (%s,%s,now(),now())"

	cursor.execute(sql, values)
	return cursor.lastrowid

def add_weapon(name, link, img_link, group_id):
	global cursor
	values = [ unicode(name), unicode(link), unicode(img_link), group_id ]
	sql = 	u"INSERT INTO weapons (name,link,img_link,group_id,created_at,updated_at) "\
			"VALUES (%s,%s,%s,%s,now(),now())"

	cursor.execute(sql, values)
	return cursor.lastrowid

def get_config():
	global cursor

	sql = "SELECT name, value, type FROM configs"
	cursor.execute(sql)
	results = cursor.fetchall()

	config = {}

	for row in results:
		name = row[0]
		value = row[1]
		datatype = row[2]

		if datatype == 'int':
			converted_value = int(value)
		elif datatype == 'decimal':
			converted_value = float(value)
		elif datatype == 'string':
			converted_value = value
		elif datatype == 'boolean':
			converted_value = bool(int(value))

		config[name] = converted_value

	return config


if __name__ == '__main__':

	#agent.time_zone = "+8:00"
	w=get_weapon(1)
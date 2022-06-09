import playhouse.db_url as db_url
import peewee as pw
import os

database = db_url.connect(os.environ['DB_URL'])


class BaseModel(pw.Model):
	class Meta:
		database = database


class Invite(BaseModel):
	code = pw.CharField()
	guild = pw.CharField()
	uses = pw.BigIntegerField(null=True)
	is_active = pw.BooleanField(default=False)
	is_selected = pw.BooleanField(default=True)
	begins_ts = pw.BigIntegerField(null=True)
	expires_ts = pw.BigIntegerField(null=True)
	class Meta:
		indexes = (
			(('code', 'guild'), True),
		)


class InviteUse(BaseModel):
	invite = pw.ForeignKeyField(Invite, backref='uses')
	user = pw.CharField()
	used_ts = pw.BigIntegerField()


def init():
	database.create_tables((Invite, InviteUse))

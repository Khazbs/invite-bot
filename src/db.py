import playhouse.db_url as db_url
import peewee as pw
import os

database = db_url.connect(os.environ['DB_URL'])


class BaseModel(pw.Model):
	class Meta:
		database = database


class Invite(BaseModel):
	code = pw.CharField(primary_key=True)
	guild = pw.CharField()
	max_uses = pw.BigIntegerField(null=True)
	is_active = pw.BooleanField(default=False)
	valid_from_ts = pw.BigIntegerField(null=True)
	valid_to_ts = pw.BigIntegerField(null=True)


class InviteUse(BaseModel):
	invite = pw.ForeignKeyField(Invite, backref='uses')
	user = pw.CharField()
	used_ts = pw.BigIntegerField()


def init():
	database.create_tables((Invite, InviteUse))

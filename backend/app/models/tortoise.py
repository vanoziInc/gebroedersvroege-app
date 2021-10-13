from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


# Tables that have to do with Users

class Users(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified_at = fields.DatetimeField(auto_now=True)
    email = fields.CharField(null=False, max_length=255)
    hashed_password = fields.CharField(null=False, max_length=255)
    is_active = fields.BooleanField(null=False, default=False)
    confirmation = fields.UUIDField(null=True)
    roles = fields.relational.ManyToManyField(
        model_name="models.Roles", related_name="users", through="user_roles")

    def __str__(self):
        return self.email

class Roles(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified_at = fields.DatetimeField(auto_now=True)
    name = fields.CharField(null=False, max_length=255)
    description = fields.CharField(null=False, max_length=255)

    def __str__(self):
        return self.name

class AllowedUsers(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified_at = fields.DatetimeField(auto_now=True)
    email = fields.CharField(null=False, max_length=255)

    def __str__(self):
        return self.email
    
    class Meta:
        table='allowed_users'

# Tables that have to with cows

class Cow(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified_at = fields.DatetimeField(auto_now=True)
    ear_number = fields.IntField(null=True)
    necklace_number = fields.IntField(null=True)
    necklace_number_mother = fields.IntField(null=True)
    date_of_birth = fields.DateField(null=True)  
    date_discharched = fields.DatetimeField(null=True) 
    reason_discharched = fields.CharField(null=True, max_length=255)
    gender = fields.CharField(null=True, max_length=255)
    breed = fields.CharField(null=True, max_length=255)
    birth = fields.ForeignKeyField('models.Birth', related_name='cow')
    

class Calve(models.Model):
    id = fields.IntField(pk=True)
    mother = fields.ForeignKeyField('models.Cow', related_name='calves', null=True)

class Birth(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified_at = fields.DatetimeField(auto_now=True)

    weight = fields.FloatField(null=True)
    first_milk = fields.CharField(null=True, max_length=255)
    birth_process=fields.CharField(null=True, max_length=255)
    # Bijzonderheden
    twins = fields.BooleanField(default=True)
    reverse = fields.BooleanField(default=True)
    cesarean_section = fields.BooleanField(default=True)
    embryo = fields.BooleanField(default=True)
    # Extra opmerkingen
    remarks = fields.TextField(null=True)

    def __str__(self):
        return self.ear_number


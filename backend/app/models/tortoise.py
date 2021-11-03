from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


# Tables that have to do with Users

class Users(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified_at = fields.DatetimeField(auto_now=True)
    first_name = fields.CharField(null=True, max_length=255)
    last_name = fields.CharField(null=True, max_length=255)
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


class GeneralMaintenance(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.CharField(null=False, max_length=255)
    last_modified_at = fields.DatetimeField(auto_now=True)
    last_modified_by = fields.CharField(null=True, max_length=255)
    description = fields.TextField(null=False)

    def __str__(self):
        return self.description
    
    class Meta:
        table='general_maintenance'

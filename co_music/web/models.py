from django.db import models

class Room(models.Model):
    code = models.IntegerField(unique=True)
    admin = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="room_admins")
    users = models.ManyToManyField("auth.User", related_name="rooms")

    is_deleted = models.BooleanField(default=False)

    @property
    def admin_name(self):
        return self.admin.first_name

    def add_user(self, user):
        self.users.add(user)

    def remove_user(self, user):
        self.users.remove(user)

    def is_user_in_room(self, user):
        return user in self.users.all()

    def __str__(self):
        return str(self.code)

class Music(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    file = models.FileField(upload_to='music/', null=True, blank=True)

    is_queued = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_playing = models.BooleanField(default=False)
    current_position = models.FloatField(default=0.0)
    total_length = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.room)

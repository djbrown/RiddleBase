from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from riddles import util


class RiddleCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField()

    def clean(self):
        if self.parent == self:
            raise ValidationError('You cannot set the parent to the object itself.')

    def __str__(self):
        return self.name


class RiddleType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.ForeignKey(RiddleCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Riddle(models.Model):
    riddle_type = models.ForeignKey(RiddleType, on_delete=models.CASCADE)
    solution = models.CharField(max_length=1000)
    pattern = models.CharField(max_length=1000)
    difficulty = models.PositiveSmallIntegerField(blank=True, null=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(10)])
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def previous_pk(self):
        previous_set = Riddle.objects.filter(pk__lt=self.pk).order_by('-pk')
        return previous_set[0].pk if previous_set else None

    def next_pk(self):
        next_set = Riddle.objects.filter(pk__gt=self.pk).order_by('pk')
        return next_set[0].pk if next_set else None

    def clean(self):
        pat_len = len(self.pattern)
        sol_len = len(self.solution)
        if pat_len != sol_len:
            raise ValidationError('Pattern length does not match solution length.')
        if not util.is_square(pat_len):
            raise ValidationError('Riddle value length is not square.')

    def get_or_create_state(self, user: User) -> str:
        state_values = self.pattern
        if user.is_authenticated():
            try:
                state = self.riddlestate
                state_values = state.values
            except ObjectDoesNotExist:
                state = RiddleState(user=user, riddle=self, values=self.pattern)
                state.save()
                state_values = state.values
        return state_values

    def __str__(self):
        return f"{self.riddle_type.name} {self.pk}"


class RiddleState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    riddle = models.ForeignKey(Riddle, on_delete=models.CASCADE)
    value = models.TextField()
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "riddle")

    def __str__(self) -> str:
        return f"{self.riddle.riddle_type.name} {self.riddle.pk} {self.user.name}"

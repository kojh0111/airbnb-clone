from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.views.generic import DetailView
from users import models as user_models
from . import models

# Create your views here.


def go_conversation(request, a_pk, b_pk):
    user_a = user_models.User.objects.get_or_none(pk=a_pk)
    user_b = user_models.User.objects.get_or_none(pk=b_pk)
    if user_a is not None and user_b is not None:
        try:
            conversation = models.Conversation.objects.get(
                Q(participants=user_a) & Q(participants=user_b)
            )
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_a, user_b)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(DetailView):

    model = models.Conversation

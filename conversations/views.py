from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from users import models as user_models
from . import models, forms

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


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        form = forms.AddCommentForm()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {
                "conversation": conversation,
                # "form": form
            },
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))

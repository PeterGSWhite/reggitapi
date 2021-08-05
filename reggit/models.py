from django.db import transaction, models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Post(models.Model):
    title = models.CharField(max_length=50)
    pattern = models.CharField(max_length=500)
    test_text = models.CharField(max_length=500000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)

    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class Vote(models.Model):
    user = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='votes', on_delete=models.CASCADE)
    # value is +1 for upvote, -1 for downvote
    # or 0 if user cancels their vote
    value = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "post")


# Cache votes every time a vote is saved.
# Could also be done periodically (e.g. once a minute or so) 
# with Celery.
def cache_votes(sender, instance, created, **kwargs):
    with transaction.atomic():
        post = Post.objects.get(pk=instance.post.id)
        post.upvotes = post.votes.filter(value=1).count()
        post.downvotes = post.votes.filter(value=-1).count()
        post.save()
post_save.connect(cache_votes, sender=Vote)
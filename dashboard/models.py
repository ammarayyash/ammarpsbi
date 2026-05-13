from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default="UI/UX Enthusiast. Sedang belajar desain interaktif dan web development.")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    streak_days = models.IntegerField(default=0)
    last_streak_date = models.DateField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    show_in_leaderboard = models.BooleanField(default=True)
    # Teacher account flag (separate from staff/admin)
    is_teacher = models.BooleanField(default=False)

    @property
    def avatar_url(self):
        """Return avatar URL or fallback to pravatar."""
        if self.avatar:
            return self.avatar.url
        return f'https://i.pravatar.cc/150?u={self.user.email}'

    def __str__(self):
        return f"{self.user.username}'s Profile"


class UniqueStreak(models.Model):
    """Record when a user reaches a notable ("angka cantik") streak value."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unique_streaks')
    streak_value = models.IntegerField()
    note = models.CharField(max_length=200, blank=True)
    achieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'streak_value')

    def __str__(self):
        return f"{self.user.username} reached {self.streak_value} days"

# Signal to auto-create UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fa-book', help_text="FontAwesome icon class")
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Mission(models.Model):
    GAMIFICATION_CHOICES = (
        ('level1', 'Level 1: Tebak Vektor/Bitmap'),
        ('level2', 'Level 2: Hitung Anchor Point'),
        ('level3', 'Level 3: Palet & Warna'),
        ('level4', 'Level 4: Rakit Maskot'),
        ('level5', 'Level 5: Drag & Drop File'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='missions', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    xp_reward = models.IntegerField(default=50)
    content = models.TextField(help_text="Materi pembelajaran HTML/Markdown untuk misi ini.")
    order = models.IntegerField(default=0, help_text="Urutan misi")
    video_url = models.URLField(blank=True, null=True, help_text="Link video YouTube untuk materi ini.")
    image = models.ImageField(upload_to='missions/', blank=True, null=True, help_text="Gambar tambahan untuk materi.")
    module_file = models.FileField(upload_to='modules/', blank=True, null=True)
    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True, help_text="Background halaman materi.")
    gamification_mode = models.CharField(max_length=20, choices=GAMIFICATION_CHOICES, blank=True, null=True, help_text="Pilih mode evaluasi gamifikasi jika ada.")

    def __str__(self):
        return self.title

# New model for community token rooms
class CommunityRoom(models.Model):
    CONTENT_MODE_CHOICES = (
        ('material', 'Materi'),
        ('quiz', 'Kuis'),
        ('both', 'Materi + Kuis'),
    )

    name = models.CharField(max_length=100)
    token = models.CharField(max_length=20, unique=True, help_text='Token to access the room')
    description = models.TextField(blank=True, default='')
    content = models.TextField(default='Selamat datang di ruang kelas ini.')
    content_mode = models.CharField(max_length=10, choices=CONTENT_MODE_CHOICES, default='both')
    # If False (default) the room runs in classic mode and will NOT store quiz submissions
    store_scores = models.BooleanField(default=False, help_text='If enabled, quiz submissions will be stored for this room')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    @property
    def has_material_section(self):
        return self.content_mode in ('material', 'both')

    @property
    def has_quiz_section(self):
        return self.content_mode in ('quiz', 'both')

    def __str__(self):
        return self.name


class CommunityRoomMembership(models.Model):
    room = models.ForeignKey(CommunityRoom, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_room_memberships')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'user')
        ordering = ('-joined_at',)

    def __str__(self):
        return f'{self.user.username} in {self.room.name}'


class CommunityMaterial(models.Model):
    room = models.ForeignKey(CommunityRoom, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, default='')
    media_url = models.URLField(blank=True, null=True)
    media_file = models.FileField(upload_to='community_materials/', blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('order', 'id')

    def __str__(self):
        return f'{self.room.name} - {self.title}'


class CommunityQuizQuestion(models.Model):
    OPTION_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    room = models.ForeignKey(CommunityRoom, on_delete=models.CASCADE, related_name='quiz_questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES, default='A')
    explanation = models.TextField(blank=True, default='')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order', 'id')

    def __str__(self):
        return f'Quiz {self.room.name}: {self.question_text[:50]}'


class CommunityQuizSubmission(models.Model):
    room = models.ForeignKey(CommunityRoom, on_delete=models.CASCADE, related_name='quiz_submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_quiz_submissions')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-submitted_at',)

    def __str__(self):
        return f'{self.user.username} - {self.room.name}: {self.score}/{self.total_questions}'


class Question(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Q: {self.text[:50]}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Benar' if self.is_correct else 'Salah'})"

class UserMissionProgress(models.Model):
    STATUS_CHOICES = (
        ('not_started', 'Belum Mulai'),
        ('reading', 'Sedang Membaca'),
        ('quiz', 'Sedang Kuis'),
        ('evaluation', 'Evaluasi'),
        ('completed', 'Selesai'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mission_progress')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'mission')

    def __str__(self):
        return f"{self.user.username} - {self.mission.title} ({self.status})"

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} - {self.question.id} - {'Benar' if self.is_correct else 'Salah'}"

# ==========================================
# MODELS UNTUK KOMUNITAS (FORUM)
# ==========================================

class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='var(--accent)')
    bg_color = models.CharField(max_length=50, default='rgba(129, 140, 248, 0.1)')

    def __str__(self):
        return self.name

class Discussion(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
        
    @property
    def total_votes(self):
        upvotes = self.votes.filter(value=1).count()
        downvotes = self.votes.filter(value=-1).count()
        return upvotes - downvotes

class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.discussion.title}"

class DiscussionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField(choices=((1, 'Upvote'), (-1, 'Downvote')))
    
    class Meta:
        unique_together = ('user', 'discussion')

    def __str__(self):
        return f"{self.user.username} voted {self.value} on {self.discussion.title}"

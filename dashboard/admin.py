from django.contrib import admin
from .models import UserProfile, Mission, Question, Choice, UserMissionProgress, UserAnswer

# Customize admin site branding
admin.site.site_header = "Illustrium Administration"
admin.site.site_title = "Illustrium Admin"
admin.site.index_title = "Panel Administrasi Illustrium"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp', 'streak_days', 'is_public', 'show_in_leaderboard')
    list_filter = ('is_public', 'show_in_leaderboard')
    search_fields = ('user__username', 'user__email', 'user__first_name')
    readonly_fields = ('user',)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    fields = ('text', 'is_correct')


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('text', 'order')
    show_change_link = True


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'xp_reward', 'question_count')
    list_display_links = ('title',)
    ordering = ('order',)
    search_fields = ('title', 'description')
    fields = ('course', 'title', 'description', 'xp_reward', 'content', 'order', 'video_url', 'image', 'background_image')
    inlines = [QuestionInline]

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Jumlah Soal'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'mission', 'order')
    list_filter = ('mission',)
    search_fields = ('text',)
    ordering = ('mission', 'order')
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text',)


@admin.register(UserMissionProgress)
class UserMissionProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'mission', 'status', 'started_at', 'completed_at')
    list_filter = ('status', 'mission')
    search_fields = ('user__username', 'mission__title')
    readonly_fields = ('started_at', 'completed_at')


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'choice', 'is_correct', 'answered_at')
    list_filter = ('is_correct',)
    search_fields = ('user__username',)
    readonly_fields = ('answered_at',)

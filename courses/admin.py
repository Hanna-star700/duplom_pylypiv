from django.contrib import admin
from .models import (
    Course, Lesson, Exercise, UserProgress, AIPracticeAttempt, DailyStudyTime,
    Rating, League, GameProfile, Achievement, UserAchievement, Competition,
    Quiz, Question, QuizAttempt,
)


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'level', 'lesson_count', 'is_published', 'order']
    list_filter = ['language', 'is_published']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]


class ExerciseInline(admin.StackedInline):
    model = Exercise
    extra = 0


class QuizInline(admin.StackedInline):
    model = Quiz
    extra = 0
    fk_name = 'lesson'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_minutes', 'is_published']
    list_filter = ['course', 'is_published']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ExerciseInline, QuizInline]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'order', 'is_published']
    list_filter = ['lesson__course', 'is_published']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'user', 'session_key', 'completed', 'completed_at']
    list_filter = ['completed']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['score', 'course', 'lesson', 'session_key', 'created_at']
    list_filter = ['score']


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_points', 'icon', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GameProfile)
class GameProfileAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'user', 'points', 'streak_days', 'league', 'last_activity_date']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'condition_type', 'points_reward', 'icon', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['achievement', 'user', 'session_key', 'earned_at']


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_at', 'end_at', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'quiz_type', 'lesson', 'course', 'is_practice', 'order', 'is_published']
    list_filter = ['quiz_type', 'is_practice', 'is_published']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text_short', 'quiz', 'question_type', 'order']

    def text_short(self, obj):
        return (obj.text[:50] + '…') if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Питання'


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'session_key', 'user', 'score', 'max_score', 'is_practice', 'completed_at']


@admin.register(AIPracticeAttempt)
class AIPracticeAttemptAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'user', 'score', 'created_at']
    list_filter = ['lesson__course', 'lesson']
    search_fields = ['user__username', 'lesson__title']
    readonly_fields = ['created_at']


@admin.register(DailyStudyTime)
class DailyStudyTimeAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'minutes']
    list_filter = ['date']
    search_fields = ['user__username']

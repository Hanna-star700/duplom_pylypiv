from .models import Course, GameProfile


def courses_list(request):
    return {
        'courses_list': Course.objects.filter(is_published=True).order_by('order')[:5],
    }


def user_profile(request):
    """Вогник днів та бали для шапки (як у ZNO Hub)."""
    if not request.user.is_authenticated:
        return {'user_streak': 0, 'user_points': 0}
    try:
        profile = GameProfile.objects.get(user=request.user)
        return {'user_streak': profile.streak_days, 'user_points': profile.points}
    except GameProfile.DoesNotExist:
        return {'user_streak': 0, 'user_points': 0}

from django.urls import path

from playground.views.playground import index, sessions, auth

app_name = 'playground'

urlpatterns = [
    # In order to perform URL reversing, you’ll need to use named URL patterns.
    # Choose names that are unlikely to clash with other applications’
    # choice of names. (reverse() finds depends on whichever pattern is last
    # in your project’s urlpatterns list.)
    # Putting a prefix on your URL name, decreases the chance of collision.
    path('', index.IndexView.as_view(), name='index'),
    path('sessions/', sessions.IndexView.as_view(), name='sessions'),
    path('sessions/clear/', sessions.ClearView.as_view(), name='sessions-clear'),
    path('sessions/clear-expired/', sessions.ClearExpiredView.as_view(), name='sessions-clear-expired'),
    path('sessions/flush/', sessions.FlushView.as_view(), name='sessions-flush'),
    path('sessions/test-cookie/', sessions.TestCookieView.as_view(), name='sessions-test-cookie'),
    path('sessions/cycle-key/', sessions.CycleKeyView.as_view(), name='sessions-cycle-key'),
    path('sessions/modified/', sessions.ModifiedView.as_view(), name='sessions-modified'),

    path('auth/', auth.IndexView.as_view(), name="auth"),
    path('auth/users/', auth.UsersIndexView.as_view(), name="auth-users"),
    path('auth/users/<int:pk>/', auth.UserView.as_view(), name="auth-user"),
    path('auth/users/<int:pk>/password', auth.UserPasswordView.as_view(), name="auth-user-password"),
    path('auth/users/<int:pk>/confirm-delete/', auth.UserDeleteConfirmView.as_view(), name="auth-user-delete-confirm"),
]

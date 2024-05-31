from django.urls import path, include
from .views import (
    CustomSigninView,
    CustomUserCreationView,
    CustomUserDetailView,
    CustomSignoutView,
    AccessDeinedView,
    UserAutoCompleteView,
    UserUpdateView,
)
from todos.views import (
    HelloView,
    TodosCreateView,
    TodosListView,
    TodoUpdateView,
    TodoDeleteView,
)
from django.contrib.auth.decorators import login_required

app_name = "accounts"

urlpatterns = [
    path("", HelloView.as_view(), name="hello"),
    path("create_todo/", TodosCreateView.as_view(), name="create_todo"),
    path("signup/", CustomUserCreationView.as_view(), name="signup"),
    path("signin/", CustomSigninView.as_view(), name="signin"),
    path("signout/", CustomSignoutView.as_view(), name="signout"),
    path("user_search/", HelloView.as_view(), name="user_search"),
    path("user_autocomplete/", UserAutoCompleteView.as_view(), name="autocomplete"),
    path("update_user/<uuid:pk>/", UserUpdateView.as_view(), name="update_user"),
    path("update_todo/<uuid:pk>/", TodoUpdateView.as_view(), name="update_todo"),
    path("delete/<uuid:pk>/", TodoDeleteView.as_view(), name="delete_todo"),
    path(
        "<str:username>/",
        CustomUserDetailView.as_view(),
        name="profile",
    ),
    path("<str:username>/todoslist", TodosListView.as_view(), name="todoslist"),
]

from django.urls import path
from django.contrib.auth import views as login_view

from .views import index

from .group_views import (
    groups, group_edit,
    group_delete, new_group
)
from .staff_views import (
    persons, new_person,
    delete_person,person_detail
)

from .cards_views import (
    show_all_cards, create_new_card,
    show_custom_card, delete_card, edit_card
)

from .action_view import (
    show_in_out
)

from .emotial_view import (
    show_all_in_house, passage,
    total_time_in_house
)

urlpatterns = [
    # Login
    path('login/', login_view.LoginView.as_view(), name="login"),
    path('logout/', login_view.LogoutView.as_view(), name="logout"),

    # First page
    path('', index, name='index'),
    
    # Groups
    path('groups/', groups, name='groups'),
    path('group_add/', new_group, name='new_group'),
    path('group/<int:id_>/<new_name>/', group_edit, name='group_edit'),
    path('group/<int:id_>/', group_edit, name='group_edit'),
    path('group/delete/<int:id_>/', group_delete, name='group_delete'),
    
    # Persons
    path('persons/', persons, name='persons'),
    path('person/', new_person, name='new_person'),
    path('person/<int:id_>/', new_person, name='new_person'),
    path('person/detail/<int:id_>/', person_detail, name='person_detail'),
    path('person/delete/<int:id_>/', delete_person, name='delete_person'),
    
    # Cards
    path('cards/', show_all_cards, name='show_all_cards'),
    path('card/', create_new_card, name='create_new_card'),
    path('card/<int:id_>/', show_custom_card, name='show_custom_card'),
    path('card/edit/<int:id_>/', edit_card, name='edit_card'),
    path('card/delete/<int:id_>/', delete_card, name='delete_card'),

    # Action
    path('actions/', show_in_out, name='show_in_out'),

    # Emotial
    path('inhouse/', show_all_in_house, name='inhouse'),
    path('passage/', passage, name='passage'),
    path('total_time/', total_time_in_house, name='total_time'),
]

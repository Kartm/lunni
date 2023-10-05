from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.urls import path

from .views.actions import upload_transactions_csv, toggle_selection, add_selection_to_group, \
    merge_selection_into_new_group, clear_selection_action, create_group_from_selection, ungroup_member, \
    create_rule_action, categorize_selection_action, create_category_action, delete_category_action
from .views.htmx import transactions_table, group_members, selection_bar, group_expand, group_collapse, \
    categorize_panel, categorize_preview, categories_panel
from .views.pages import transactions_page, breakdown_page

app_name = "lunni2"

urlpatterns = [
    path("transactions/", transactions_page, name="transactions"),
    path("breakdown/", breakdown_page, name="breakdown"),
    path("hx/transactions/table/", transactions_table, name="hx_transactions_table"),
    path("actions/transactions/upload/", upload_transactions_csv, name="upload_transactions_csv"),

    path("hx/groups/<uuid:group_id>/members/", group_members, name="hx_group_members"),
    path("hx/groups/<uuid:group_id>/expand/", group_expand, name="hx_group_expand"),
    path("hx/groups/<uuid:group_id>/collapse/", group_collapse, name="hx_group_collapse"),

    # group actions (selection-driven)
    path("actions/groups/create/", create_group_from_selection, name="create_group_from_selection"),
    path("actions/groups/add-selection/", add_selection_to_group, name="add_selection_to_group"),
    path("actions/groups/merge-selection/", merge_selection_into_new_group, name="merge_selection_into_new_group"),
    path("actions/groups/<uuid:group_id>/ungroup/", ungroup_member, name="ungroup_member"),

    # selection mechanics
    path("hx/selection/bar/", selection_bar, name="hx_selection_bar"),
    path("actions/selection/toggle/", toggle_selection, name="toggle_selection"),
    path("actions/selection/clear/", clear_selection_action, name="clear_selection"),

    path("hx/categorize/panel/", categorize_panel, name="hx_categorize_panel"),
    path("hx/categorize/preview/", categorize_preview, name="hx_categorize_preview"),

    # categorization actions
    path("actions/rules/create/", create_rule_action, name="create_rule_action"),
    path("actions/categorize/selection/", categorize_selection_action, name="categorize_selection_action"),

    # categories
    path("hx/categories/panel/", categories_panel, name="hx_categories_panel"),
    path("actions/categories/create/", create_category_action, name="create_category_action"),
    path("actions/categories/delete/<int:category_id>/", delete_category_action, name="delete_category_action"),
]

if not settings.TESTING:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
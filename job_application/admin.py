from django.contrib import admin
from .models import Job, Goal, Note

admin.site.register(Job)


class NoteAdmin(admin.ModelAdmin):
    list_display = ('job', 'date_created')
    list_filter = ('job', 'date_created')
    search_fields = ('job', 'date_created')
    ordering = ('-date_created',)
    date_hierarchy = 'date_created'


admin.site.register(Note, NoteAdmin)
admin.site.register(Goal)

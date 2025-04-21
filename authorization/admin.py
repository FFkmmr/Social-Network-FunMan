from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Chat, Message, MyUser

class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('username', 'email', 'birthdate', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'following')}),
        ('Personal info', {'fields': ('email', 'birthdate')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'birthdate', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('timestamp',)
    fields = ('sender', 'text', 'timestamp', 'is_read')


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'participants_list', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('participants__username',)
    inlines = [MessageInline]
    
    def participants_list(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    participants_list.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'text_short', 'timestamp', 'is_read')
    list_filter = ('timestamp', 'is_read')
    search_fields = ('text', 'sender__username')
    readonly_fields = ('timestamp',)
    
    def text_short(self, obj):
        return f"{obj.text[:50]}..." if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Text'


admin.site.register(MyUser, MyUserAdmin)

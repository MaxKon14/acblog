from django.contrib import admin, messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import SendEmailForm
from .models import Category, Post, Subscribers

admin.site.empty_value_display = "Не задано"


class PostInline(admin.TabularInline):
    model = Category.posts.through
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
        "slug",
        "created_at",
    )
    list_editable = ("is_published",)
    search_fields = ("name",)
    list_display_links = ("name",)
    inlines = [
        PostInline,
    ]


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "id",
        "is_published",
        "pub_date",
        "author",
    )
    list_editable = ("is_published",)
    search_fields = ("title",)
    list_display_links = ("title",)
    list_filter = ("category",)
    filter_horizontal = ("category",)


class SubscribersAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "id",
        "is_active",
        "subscribed_at",
    )
    list_editable = ("is_active",)
    search_fields = ("email",)
    list_display_links = ("email",)
    actions = ["send_email"]

    def send_email(self, request, queryset):
        if request.method == "POST" and "apply" in request.POST:
            form = SendEmailForm(request.POST)
            print(form)

            if form.is_valid():
                # Берём выбранных подписчиков из стандартного механизма Django admin
                selected_ids = request.POST.getlist("_selected_action")
                selected_subscribers = self.model.objects.filter(pk__in=selected_ids)

                count = selected_subscribers.count()
                if count == 0:
                    messages.error(
                        request, "Не удалось определить выбранных подписчиков."
                    )
                    return render(
                        request,
                        "admin/send_email.html",
                        {
                            **self.admin_site.each_context(request),
                            "form": form,
                            "queryset": queryset,
                            "opts": self.model._meta,
                            "title": "Отправить email выбранным подписчикам",
                        },
                    )

                sent_count = 0
                print(selected_subscribers)
                for sub in selected_subscribers:
                    try:
                        send_mail(
                            subject=form.cleaned_data["subject"],
                            message=form.cleaned_data["message"],
                            from_email=None,  # ← использует DEFAULT_FROM_EMAIL
                            recipient_list=[sub.email],
                            html_message=form.cleaned_data["message"],
                            fail_silently=False,
                        )
                        sent_count += 1
                    except Exception as e:
                        messages.error(
                            request, f"Ошибка отправки на {sub.email}: {str(e)}"
                        )

                if sent_count > 0:
                    messages.success(
                        request, f"Успешно отправлено {sent_count} из {count} писем."
                    )
                else:
                    messages.warning(request, "Ни одно письмо не было отправлено.")

                return redirect("admin:posts_subscribers_changelist")

            else:
                messages.error(request, "Форма содержит ошибки. Проверьте поля.")

        else:
            # GET — показываем форму с предзаполненными получателями
            form = SendEmailForm(initial={"subscribers": queryset})

        context = {
            **self.admin_site.each_context(request),
            "form": form,
            "queryset": queryset,
            "opts": self.model._meta,
            "title": "Отправить email выбранным подписчикам",
        }

        return render(request, "admin/send_email.html", context)

    send_email.short_description = "Отправить письмо выбранным пользователям"


admin.site.register(Subscribers, SubscribersAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)

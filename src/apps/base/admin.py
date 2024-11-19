from django.contrib import admin


class CustomAdmin(admin.ModelAdmin):
    """
    A custom admin class that automatically assigns the currently logged-in user as the creator
    of a new object and the last updater of any object.
    """

    def save_model(self, request, obj, form, change) -> None:
        """
        Parameters:
        - request: HttpRequest object representing the current request.
        - obj: The actual model instance being saved.
        - form: ModelForm instance used to submit the data.
        - change: Boolean, True if this is an update to an existing object, False if a new object.

        Returns:
        - None: The method returns None but saves the instance to the database.
        """
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


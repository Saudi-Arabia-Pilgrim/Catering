from rest_framework import generics


class CustomGenericAPIView(generics.GenericAPIView):
    """
    CustomGenericAPIView: Base class for all other generic views.
    Provides the core functionality such as serialization, pagination, and filtering.
    Example: Use as a base for creating a view that needs custom pagination or filtering.
    """
    pass


class CustomListAPIView(generics.ListAPIView):
    """
    CustomListAPIView: Used to create read-only endpoints to represent a collection of model instances.
    Provides a GET method handler.
    Example: Use to display a list of blog posts or user profiles.
    """
    pass


class CustomCreateAPIView(generics.CreateAPIView):
    """
    CustomCreateAPIView: Used to create an endpoint for creating model instances.
    Provides a POST method handler.
    Example: Use to allow users to create new blog entries or register new accounts.
    """
    pass


class CustomRetrieveAPIView(generics.RetrieveAPIView):
    """
    CustomRetrieveAPIView: Used for read-only endpoints to represent a single model instance.
    Provides a GET method handler to retrieve details of a specific instance.
    Example: Use to display details of a specific blog post or user profile.
    """
    pass


class CustomUpdateAPIView(generics.UpdateAPIView):
    """
    CustomUpdateAPIView: Used to create an endpoint for updating an existing model instance.
    Provides PUT and PATCH method handlers to update resources.
    Example: Use to allow users to update their profile information or a blog post.
    """
    pass


class CustomDestroyAPIView(generics.DestroyAPIView):
    """
    CustomDestroyAPIView: Used to create an endpoint for deleting a specific model instance.
    Provides a DELETE method handler.
    Example: Use to allow users to delete their own blog posts or profiles.
    """
    pass


class CustomListCreateAPIView(generics.ListCreateAPIView):
    """
    CustomListCreateAPIView: Combines list and create functionalities.
    Provides a read-write endpoint to list resources and allow new resources to be created via POST.
    Example: Use in a forum application to list threads and allow the creation of new threads.
    """
    pass


class CustomRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    CustomRetrieveUpdateAPIView: Combines retrieve and update functionalities.
    Provides an endpoint to read (GET) or update (PUT/PATCH) a specific instance.
    Example: Use in a settings page where users can view and modify their settings.
    """
    pass


class CustomRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    CustomRetrieveDestroyAPIView: Combines retrieve and destroy functionalities.
    Provides an endpoint to read (GET) or delete (DELETE) a specific instance.
    Example: Use in administrative dashboards where details of a user can be viewed or deleted.
    """
    pass


class CustomRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    CustomRetrieveUpdateDestroyAPIView: A fully featured endpoint that provides methods to retrieve, update,
    or delete a specific instance.
    Provides GET, PUT, PATCH, and DELETE handlers, offering full CRUD functionality for a specific instance.
    Example: Use for a product detail page where you can view, update, or delete a product.
    """
    pass
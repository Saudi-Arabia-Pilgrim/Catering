from drf_spectacular.utils import extend_schema_view, extend_schema

class AutoTaggedAPIView:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        tag = cls.__module__.split('.')[1].capitalize()
        method_decorators = {
            method: extend_schema(tags=[tag])
            for method in ['get', 'post', 'put', 'patch', 'delete']
            if hasattr(cls, method)
        }

        extend_schema_view(**method_decorators)(cls)

class AutoTaggedAPIViewSets:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        tag = cls.__module__.split('.')[1].capitalize()

        viewset_methods = [
            'list', 'create', 'retrieve', 'update', 'partial_update', 'destroy'
        ]

        method_decorators = {
            method: extend_schema(tags=[tag])
            for method in viewset_methods
            if hasattr(cls, method)
        }

        extend_schema_view(**method_decorators)(cls)

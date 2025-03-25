from apps.base.views import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from apps.menus.models import Menu
from apps.menus.serializers import MenuSerializer


class MenuRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuListCreateAPIView(CustomListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
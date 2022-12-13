from rest_framework import viewsets, mixins, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework import status
from core.models import Food, Order
from food import serializers
from core.functions import (
    query_date_major_or_minor,
    read_orders_in_local_time,
    lastest_canceled_and_next_allowed
)


class FoodView(generics.ListAPIView):
    """Food List View"""
    serializer_class = serializers.FoodSerializer
    queryset = Food.objects.all()

    def get_queryset(self):
        return self.queryset

    def list(self, request):
        """Retreive the foods list"""
        data = self.get_queryset().order_by('id')
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FoodAdminViewSet(viewsets.ModelViewSet):
    """Manage admin foods in the database"""
    serializer_class = serializers.FoodSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all().order_by(
                                                                        '-id')
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    def list(self, request):
        """Retreive the foods list"""
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Retrive a detail object"""
        instance = self.get_queryset(pk)
        if instance:
            serializer = self.get_serializer(instance)
            json_data = serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        return Response(
            {'error': 'No se encontró el platillo'},
            status=status.HTTP_404_NOT_FOUND
        )

    def destroy(self, request, pk=None):
        """Delete Food"""
        instance = self.get_queryset(pk)
        if instance:
            instance.delete()
            return Response(
                {'Message': 'Platillo Eliminado correctamente'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'No se encontró el platillo'},
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin):
    """Manage Orders in the database"""
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    canceled_range_days = 4
    discount_range_days = 1
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(
                    user=self.request.user).order_by('-creation_date')
        return self.get_serializer().Meta.model.objects.filter(
                                user=self.request.user, id=pk).first()

    def get_serializer_class(self):
        """Return apporpriate serializer class"""
        if self.action == 'list':
            return serializers.OrderListSerializer
        if self.action == 'retrieve':
            return serializers.OrderDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create new object"""
        serializer.save(user=self.request.user)

    def list(self, request):
        """Retreive the orders list"""
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        for order in serializer.data:
            created = order['creation_date']
            order['creation_date'] = read_orders_in_local_time(created)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Create Orders"""
        """first check canceled:"""
        next_allowed = lastest_canceled_and_next_allowed(
                                self.canceled_range_days, self.get_queryset())
        if next_allowed is not None:
            msg = 'Has cancelado 3 veces en un periodo'
            msg += f'de {self.canceled_range_days} '
            msg += 'días, no podrás volver a ordenar hasta'
            next_allowed = read_orders_in_local_time(next_allowed)
            return Response(
                {'error': f'{msg} {next_allowed}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        """Send information to serializer"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)

            """Check discount and send"""
            minor = query_date_major_or_minor()[0]
            major = query_date_major_or_minor()[1]
            orders_period_discount = self.get_queryset().filter(
                canceled=False,
                creation_date__gte=minor,
                creation_date__lte=major,
            )
            order = self.get_queryset().first()
            order.subtotal = order.food.price
            msg = None
            if len(orders_period_discount) == 3:
                order.discount = order.food.price / 2
                value = 'Felicidades, es tu tercer pedido hoy, ahorraste 50%'
                msg = {'msg': f'{value}'}
            order.total = order.subtotal - order.discount
            order.save()
            data = {}
            data = serializer.data
            data['subtotal'] = order.subtotal
            data['discount'] = order.discount
            data['total'] = order.total
            if msg is None:
                msg = data
            return Response(msg, status=status.HTTP_201_CREATED)
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request, pk=None):
        """Retrive a detail object"""
        instance = self.get_queryset(pk)
        if instance:
            serializer = self.get_serializer(instance)
            json_data = serializer.data
            created = json_data['creation_date']
            json_data['creation_date'] = read_orders_in_local_time(created)
            return Response(json_data, status=status.HTTP_200_OK)
        return Response(
            {'error': 'No se encontro el pedido'},
            status=status.HTTP_404_NOT_FOUND
        )

    def destroy(self, request, pk=None):
        """Cancel Orders"""
        order = self.get_serializer().Meta.model.objects.filter(
                    id=pk, canceled=False, completed=False).first()
        if order:
            order.canceled = True
            order.save()
            next_allowed = lastest_canceled_and_next_allowed(
                self.canceled_range_days,
                self.get_queryset()
            )
            if next_allowed is not None:
                msg = 'Pedido Cancelado exitosamente. '
                msg += 'Ya has cancelado 3 veces en un periodo de '
                msg += f'{self.canceled_range_days} días, '
                msg += 'no podrás volver a ordenar hasta'
                next_allowed = read_orders_in_local_time(next_allowed)
                return Response(
                    {'Advertencia': f'{msg} {next_allowed}'},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'Message': f'Pedido No.{order.id} Cancelado exitosamente'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'No se encontro el pedido.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderAdminViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    """Manage Admin Orders in the database"""
    queryset = Order.objects.all()
    serializer_class = serializers.OrderAdminSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']

    def get_queryset(self, pk=None):
        """Return order list/detail of all orders (pending records)"""
        if pk is None:
            return self.queryset.all().order_by('-creation_date')
        return self.get_serializer().Meta.model.objects.filter(
                    id=pk, canceled=False, completed=False).first()

    def get_serializer_class(self):
        """Return apporpriate serializer class"""
        if self.action == 'retrieve':
            return serializers.OrderAdminDetailSerializer
        return self.serializer_class

    def list(self, request):
        """Retreive the admin orders list"""
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        for order in serializer.data:
            created = order['creation_date']
            order['creation_date'] = read_orders_in_local_time(created)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Retrive a detail Admin Order"""
        order = self.get_queryset().filter(id=pk).first()
        if order:
            serializer = self.get_serializer(order)
            json_data = serializer.data
            created = json_data['creation_date']
            json_data['creation_date'] = read_orders_in_local_time(created)
            return Response(json_data, status=status.HTTP_200_OK)
        return Response(
            {'error': 'No se encontro el pedido'},
            status=status.HTTP_404_NOT_FOUND
        )

    def update(self, request, pk=None):
        """Finish/Completed Admin Orders"""
        order = self.get_queryset().filter(
            id=pk, canceled=False, completed=False).first()
        if order:
            order.completed = True
            order.save()
            return Response(
                {'Message': f'Pedido No.{order.id} Entregado exitosamente'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'No se encontro el pedido.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk=None):
        """Cancel Admin Orders"""
        order = self.get_queryset().filter(
            id=pk, canceled=False, completed=False).first()
        if order:
            order.canceled = True
            order.save()
            message = f'Pedido No.{order.id} Cancelado desde Administrador'
            return Response(
                {'Message': message},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'No se encontro el pedido.'},
            status=status.HTTP_400_BAD_REQUEST
        )

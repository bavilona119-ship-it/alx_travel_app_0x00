from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Listing objects.
    
    Provides CRUD operations:
    - list: GET /api/listings/
    - create: POST /api/listings/
    - retrieve: GET /api/listings/{id}/
    - update: PUT /api/listings/{id}/
    - partial_update: PATCH /api/listings/{id}/
    - destroy: DELETE /api/listings/{id}/
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'price_per_night', 'availability']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price_per_night', 'created_at']
    ordering = ['-created_at']


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Booking objects.
    
    Provides CRUD operations:
    - list: GET /api/bookings/
    - create: POST /api/bookings/
    - retrieve: GET /api/bookings/{id}/
    - update: PUT /api/bookings/{id}/
    - partial_update: PATCH /api/bookings/{id}/
    - destroy: DELETE /api/bookings/{id}/
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['listing', 'user', 'status']
    ordering_fields = ['check_in_date', 'check_out_date', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Optionally filter bookings by user if authenticated.
        """
        queryset = Booking.objects.all()
        user = self.request.user
        
        # If user is authenticated and not staff, show only their bookings
        if user.is_authenticated and not user.is_staff:
            queryset = queryset.filter(user=user)
        
        return queryset

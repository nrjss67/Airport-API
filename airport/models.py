from typing import Any
from django.db import models


from user.models import User


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )

    def __str__(self):
        return f"{self.name} - {self.airplane_type}"

    @property
    def total_seats(self):
        return self.rows * self.seats_in_row


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.closest_big_city}"


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="source_routes"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destination_routes"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"Source: {self.source.name} - Destination: {self.destination.name}"

    @property
    def short_name(self):
        return f"{self.source.closest_big_city} - {self.destination.closest_big_city}"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew)

    def __str__(self):
        return f"Flight {self.id} - {self.route.short_name} - {self.airplane.name}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.create_available_tickets()

    def create_available_tickets(self):
        tickets = []
        for row in range(1, self.airplane.rows + 1):
            for seat in range(1, self.airplane.seats_in_row + 1):
                tickets.append(
                    Ticket(
                        flight=self,
                        row=row,
                        seat=seat,
                        available=True,
                    )
                )
        Ticket.objects.bulk_create(tickets)

    @property
    def available_tickets(self):
        return Ticket.objects.filter(flight=self, available=True)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    available = models.BooleanField(default=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets", blank=True, null=True
    )

    class Meta:
        unique_together = ("flight", "row", "seat")

    def __str__(self):
        return f"Ticket {self.row} {self.seat} - Flight {self.flight.id}"

from django.db import models


class Building(models.Model):
    building_city = models.CharField(max_length=10, default='NYC', null=True)
    state = models.CharField(max_length=10, default='NY', null=True)
    address = models.TextField()
    zipcode = models.CharField(max_length=100)
    block_number = models.PositiveIntegerField()
    lot = models.PositiveIntegerField()
    lot_sq_ft = models.PositiveIntegerField()
    year_built = models.PositiveIntegerField()
    building_class = models.CharField(max_length=100)
    owner = models.CharField(max_length=1000)

    def __str__(self):
        return "{} - {}".format(self.block_number, self.owner)

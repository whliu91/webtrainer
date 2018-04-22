from django.db import models

class NNModel_config(models.Model):
	number_of_layers = models.IntegerField()
	nodes_in_layers = models.CharField(max_length=20)
	activation_function = models.CharField(max_length=10)
	batch_size = models.CharField(max_length=10)
	optimisation_function = models.CharField(max_length=10)
	loss_function = models.CharField(max_length=10)
	epoch = models.IntegerField()
	create_date = models.DateField()
	model_name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name
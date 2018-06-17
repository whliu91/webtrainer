from django.db import models

# NN model db
class NNModelHistory(models.Model):
    OPTIMIZE_FUNC_CHOICES = (
        ('mape', 'mape'),
        ('mse', 'mse'),
        ('mae', 'mae'),
    )
    LOSS_FUNC_CHOICES = (
        ('sgd', 'sgd'),
        ('rmsprop', 'rmsprop'),
        ('adam', 'adam'),
    )
    src_date = models.DateTimeField()
    user_created = models.CharField(max_length=50)
    company_created = models.CharField(max_length=50)
    # model configurations
    input_size = models.IntegerField()
    batch_size = models.IntegerField()
    optim_func = models.CharField(max_length=50, choices=OPTIMIZE_FUNC_CHOICES)
    loss_func = models.CharField(max_length=50, choices=LOSS_FUNC_CHOICES)
    epoch_size = models.IntegerField()
    num_layers = models.IntegerField()
    weights_json = models.CharField(max_length=500)
    min_train_err = models.FloatField()
    data_file = models.FileField(upload_to='uploads/data/')
from django.db import models
from django.conf import settings

# NN model db
class NNModelHistory(models.Model):
    '''
    Database for all models created by users
    '''
    LOSS_FUNC_CHOICES = (
        ('mape', 'mape'),
        ('mse', 'mse'),
        ('mae', 'mae'),
    )
    OPTIMIZE_FUNC_CHOICES = (
        ('sgd', 'sgd'),
        ('rmsprop', 'rmsprop'),
        ('adam', 'adam'),
    )
    src_date = models.DateTimeField()
    user_created = models.CharField(max_length=50)
    company_created = models.CharField(max_length=50)
    # model configurations
    model_name = models.CharField(max_length=50)
    input_size = models.IntegerField()
    batch_size = models.IntegerField()
    optim_func = models.CharField(max_length=50, choices=OPTIMIZE_FUNC_CHOICES)
    loss_func = models.CharField(max_length=50, choices=LOSS_FUNC_CHOICES)
    epoch_size = models.IntegerField()
    num_layers = models.IntegerField()
    num_neurons_layer_str = models.CharField(max_length=100)
    weights_json = models.CharField(max_length=500, default=None, blank=True, null=True)
    min_train_err = models.FloatField(default=None, blank=True, null=True)
    data_file_path = models.FilePathField(path=settings.NN_MODEL_DATA_PATH, default=None, blank=True, null=True)
    data_rows = models.IntegerField(default=0)
    current_data_header = models.CharField(max_length=500, default=None, blank=True, null=True)
    target_col_name = models.CharField(max_length=50, default=None, blank=True, null=True)


class NNJobHistory(models.Model):
    '''
    Database for all jobs created by users
    '''
    JOB_STATUS_CHOICES = (
        ('RUNNING', 'RUNNING'),
        ('FAILED', 'FAILED'),
        ('SUCCEED', 'SUCCEED'),
    )
    job_id = models.CharField(max_length=50)
    job_start_time = models.DateTimeField()
    job_end_time = models.DateTimeField(default=None, blank=True, null=True)
    job_status = models.CharField(max_length=50, choices=JOB_STATUS_CHOICES)
    user_created = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50)
    weights_json = models.CharField(max_length=500, default=None, blank=True, null=True)
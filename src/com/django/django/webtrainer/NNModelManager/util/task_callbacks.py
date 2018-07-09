from NNModelManager.models import NNModelHistory, NNJobHistory

def onTrainingCompeted(job_id, success, weights_json):
    job_obj = NNJobHistory.objects.get(job_id=job_id)
    job_obj.job_status = 'SUCCEED'
    job_obj.weights_json = weights_json
    user_email = job_obj.user_created
    job_obj.save()

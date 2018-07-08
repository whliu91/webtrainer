from NNModelManager.models import NNModelHistory, NNJobHistory

def onTrainingCompeted(job_id, success):
    job_obj = NNJobHistory.objects.get(job_id=job_id)
    job_obj.job_status = 'SUCCEED'
    user_email = job_obj.user_created
    job_obj.save()

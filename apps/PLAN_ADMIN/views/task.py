from apps.BASE.base import AppAPIView
from apps.PLAN_ADMIN.helpers import STATUS
from apps.PLAN_ADMIN.models import PlanTask




class 

class PlanTaskAPIView(AppAPIView):
    def post(self, request, *args, **kwargs):
        uuid = request.data.get("uuid")
        status = request.data.get("status")

        if not uuid or not status:
            return self.send_error_response("Both uuid and status are required")
 
        try:
            # Fetch the PlanTask instance by uuid
            plan_task = PlanTask.objects.get(uuid=uuid)
            
            # Update the status field
            plan_task.status = status
            plan_task.save()  # Save the updated instance
            
            # Return success response
            return self.send_response(
                message="Status updated successfully"
            )
        
        except PlanTask.DoesNotExist:
            return self.send_error_response(f"No PlanTask found with uuid: {uuid}")
        
        except Exception as e:
            return self.send_error_response(f"An error occurred: {str(e)}")

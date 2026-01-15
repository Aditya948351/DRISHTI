from django.core.management.base import BaseCommand
from complaints.models import Complaint
from ai_engine.utils import predict_category, predict_priority

class Command(BaseCommand):
    help = 'Scans all complaints and updates AI predictions (Category & Priority)'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Force update even if already analyzed')

    def handle(self, *args, **options):
        force = options['force']
        complaints = Complaint.objects.all()
        
        updated_count = 0
        total_count = complaints.count()
        
        self.stdout.write(f"Scanning {total_count} complaints...")
        
        for complaint in complaints:
            if not complaint.ai_predicted_category or force:
                self.stdout.write(f"Analyzing Complaint #{complaint.id}: {complaint.title}...")
                
                # Predict Category
                cat, cat_conf = predict_category(complaint.description)
                
                # Predict Priority
                prio, prio_conf = predict_priority(complaint.description, cat)
                
                # Update Complaint
                complaint.ai_predicted_category = cat
                complaint.ai_predicted_priority = prio
                complaint.ai_confidence_score = (cat_conf + prio_conf) / 2 * 100 # Store as percentage
                
                # If category/priority were empty, update them too (optional, but good for consistency)
                if not complaint.category:
                    # Here we would ideally link to a Category object, but for now we rely on the AI text
                    pass 
                
                if complaint.priority == 'medium' or not complaint.priority: # Default
                     complaint.priority = prio

                complaint.save()
                updated_count += 1
                
        self.stdout.write(self.style.SUCCESS(f"Successfully updated {updated_count} complaints."))

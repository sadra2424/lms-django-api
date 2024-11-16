from django.db import models

class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('MOST_BORROWED', 'Most Borrowed Books'),
        ('OVERDUE_BORROWERS', 'Overdue Borrowers'),
        ('CHECKED_OUT_BOOKS', 'Checked Out Books'),
    ]
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.TextField()

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.created_at}"
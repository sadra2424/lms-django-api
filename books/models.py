from django.db import models
from authors.models import Author
from django.db.models import Avg


class Book(models.Model):
    """
    مدل کتاب که شامل اطلاعاتی مانند عنوان، توضیحات، نویسنده، ISBN، دسته‌بندی، تاریخ انتشار،
    و تاریخ‌های ایجاد و به‌روزرسانی می‌باشد.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey('authors.Author' , on_delete=models.CASCADE, related_name='books')
    #models.CASCADE اگر یک نویسنده حذف بشود همه کتاب هاش حذف میشن
    ISBN = models.CharField(max_length=13, unique=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,null=True,related_name='books')
    publication_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    availability = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    borrower_count = models.PositiveIntegerField(default=0)#برای ریپر ها
    

    def average_rating(self):
        """
        محاسبه میانگین امتیازات داده شده به این کتاب
        """
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return self.title

class Category(models.Model):
    """
    مدل دسته‌بندی که نام دسته‌بندی‌ها را ذخیره می‌کند.
    """
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    """
    مدل نقد و بررسی که شامل اطلاعاتی مانند کاربر، کتاب، امتیاز، نظر و تاریخ ایجاد نقد می‌باشد.
    ترکیب فیلدهای borrower و book باید منحصربه‌فرد باشد تا هر کاربر فقط یک نقد برای هر کتاب ثبت کند.
    """
    from borrowers.models import Borrower#برای کار کرد بهتر
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE,related_name="reviews")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=[(i,i) for i in range(1,6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    


    class Meta:
        unique_together = ['borrower' , 'book']
        #این ویژگی یک محدودیت منحصربه‌فرد ترکیبی را ایجاد می‌کند، به این معنی که ترکیب دو یا چند فیلد در جدول باید منحصربه‌فرد باشد.

    def __str__(self):
        return f"Review by {self.borrower.user.username} for {self.book.title}"

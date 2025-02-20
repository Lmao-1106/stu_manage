from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

class Student(models.Model):
    """
    学生基本信息
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile',null=True,blank=True)
    name = models.CharField(max_length=100, verbose_name="姓名")
    age = models.IntegerField(null=True, blank=True, verbose_name="年龄")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="电话")
    email = models.EmailField(null=True, blank=True, verbose_name="邮箱")
    avatar_url = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="头像",default="avatars/default_avatar.jpg")
    # 如果有其他信息，酌情增加

    def __str__(self):
        return self.name

class Course(models.Model):
    """
    课程或报课类别
    """
    name = models.CharField(max_length=100, verbose_name="课程名称")
    description = models.TextField(null=True, blank=True, verbose_name="课程描述")
    total_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="总课时数"
    )
    fixed_deduction = models.DecimalField(
        max_digits=3,  # 允许的数字总位数，比如最多 99.9
        decimal_places=1,  # 小数位精度，保留 1 位小数（可以改成 2）
        default=Decimal('1.0'),
        verbose_name="每次课扣除课时"
    )

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    """
    学生报课信息，用于记录学生与课程的关系、剩余课时等
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生",related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    remaining_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="剩余课时"
    )

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"


class Attendance(models.Model):
    """
    学生出勤记录，用于对出勤情况进行汇总
    """
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, verbose_name="报课记录",related_name="attendances")
    date = models.DateField(verbose_name="上课日期")
    is_present = models.BooleanField(default=True, verbose_name="是否出勤")

    # 也可以加上签到时间、签退时间等字段
    def __str__(self):
        return f"{self.enrollment.student.name} - {self.enrollment.course.name} 出勤: {self.is_present}"


class ClassroomPerformance(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='performances')
    performance_date = models.DateField(auto_now_add=True)
    rating = models.TextField()
    # 新的多维评分字段
    focus = models.IntegerField(default=0)  # 课堂专注
    logical_thinking = models.IntegerField(default=0)  # 思维逻辑
    creativity = models.IntegerField(default=0)  # 创新能力
    expression = models.IntegerField(default=0)  # 自我表达
    #保留评论字段
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.enrollment.student.name} - {self.performance_date} - 课堂评价"


# 信号：每次 Attendance 被保存后，自动创建 ClassroomPerformance
@receiver(post_save, sender=Attendance)
def create_classroom_performance(sender, instance, created, **kwargs):
    if created and instance.is_present:  # 如果出勤记录是新创建并且出勤了
        # 获取 Enrollment 对象
        enrollment = instance.enrollment

        # 创建一个新的 ClassroomPerformance 记录
        ClassroomPerformance.objects.create(
            enrollment=enrollment,
            rating="待评分",  # 默认的课堂评价内容
            notes="待填写"    # 默认备注内容
        )



@receiver(post_save, sender=Attendance)
def deduct_remaining_hours(sender, instance, created, **kwargs):
    if created and instance.is_present:
        enrollment = instance.enrollment
        course = enrollment.course
        # 从 course.fixed_deduction 获取要扣减的课时
        deduction = course.fixed_deduction or 0

        if enrollment.remaining_hours >= deduction:
            enrollment.remaining_hours -= deduction
        else:
            # 若剩余课时不足，则置 0 或做其他业务逻辑
            enrollment.remaining_hours = 0

        enrollment.save()
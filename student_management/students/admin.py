
from .models import ClassroomPerformance
# Register your models here.
from django.contrib import admin
from .models import Student, Course, Enrollment, Attendance
from django.utils.html import format_html

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0  # 不要额外空行
    fields = ['date', 'is_present','performance_link']  # 显示出勤记录的字段
    readonly_fields = ['performance_link']  # 将 performance_link 设置为只读字段

    def performance_link(self, obj):
        """
        为每个出勤记录生成指向课堂表现的链接
        """
        performance = ClassroomPerformance.objects.filter(
            enrollment=obj.enrollment,
            performance_date=obj.date
        ).first()
        if performance:
            # 返回跳转到课堂表现页面的链接
            return format_html('<a href="{}">查看课堂表现</a>',
                               f'/admin/students/classroomperformance/{performance.id}/change/')
        else:
            return "暂无课堂表现"

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0  # 不要额外空行
    inlines = [AttendanceInline]  # 嵌入出勤记录

class ClassroomPerformanceAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'performance_date', 'rating', 'notes')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user','name', 'age')
    inlines = [EnrollmentInline]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_hours')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'remaining_hours')
    inlines = [AttendanceInline]

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'date', 'is_present')
    list_filter = ('is_present', 'date')  # 可以通过出勤情况过滤
    search_fields = ('enrollment__student__name',)  # 支持按学生姓名搜索

    # 可选：为每次保存出勤记录后，自动触发信号
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 这里我们可以直接处理一些特定逻辑
        # 比如通过触发信号自动生成评价（已经通过信号实现）


admin.site.register(ClassroomPerformance, ClassroomPerformanceAdmin)







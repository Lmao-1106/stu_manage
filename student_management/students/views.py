from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Course, Enrollment, Attendance

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    enrollments = Enrollment.objects.filter(student=student)
    return render(request, 'students/student_detail.html', {
        'student': student,
        'enrollments': enrollments
    })

def home_page(request):
    return render(request,'students/index.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, Enrollment

@login_required
def student_home(request):
    user = request.user
    # 假设 Student 模型里对 user 做了一对一关联，related_name='student_profile'
    student = getattr(user, 'student_profile', None)

    # 若账号并未关联学生信息
    if not student:
        # 可以跳转到某个提示页面 or 给出错误提示
        return render(request, 'students/no_student_profile.html')

    # 获取报课信息
    enrollments = request.user.student_profile.enrollments.all()

    context = {
        'student': student,
        'enrollments': enrollments,
    }
    print(f"en:{enrollments}")
    return render(request, 'students/student_home.html', context)



# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ClassroomPerformance, Enrollment

@login_required
def classroom_performance_detail(request, attendance_id):

    # 获取具体的出勤记录
    attendance = get_object_or_404(Attendance, id=attendance_id)
    # 获取该出勤记录对应的课堂表现
    performance = ClassroomPerformance.objects.filter(
        enrollment=attendance.enrollment,
        performance_date=attendance.date
    ).first()

    if request.method == 'POST':
        # 如果没有找到课堂表现记录，则创建一个新的记录
        if not performance:
            performance = ClassroomPerformance.objects.create(
                enrollment=attendance.enrollment,
                performance_date=attendance.date,
                focus=request.POST.get('focus', 0),
                logical_thinking=request.POST.get('logical_thinking', 0),
                creativity=request.POST.get('creativity', 0),
                expression=request.POST.get('expression', 0),
                notes=request.POST.get('notes', '')
            )
        else:
            performance.focus = request.POST.get('focus', 0)
            performance.logical_thinking = request.POST.get('logical_thinking', 0)
            performance.creativity = request.POST.get('creativity', 0)
            performance.expression = request.POST.get('expression', 0)
            performance.notes = request.POST.get('notes', '')
            performance.save()

        # 保存后重定向回当前页面
        return redirect('classroom_performance_detail', attendance_id=attendance.id)
    '''
    if request.method == 'POST':
        performance.rating = request.POST['rating']
        performance.notes = request.POST['notes']
        performance.save()
    '''

    return render(request, 'students/classroom_performance_detail.html', {'performance': performance, 'attendance': attendance})


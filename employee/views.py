from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Employee
from .forms import AddEmployeeForm


@login_required(login_url='authapp:login')
def index(request):
    context = dict()
    context['employees'] = Employee.objects.all().order_by('-joined_date')[:5]
    return render(request, 'employee/index.html', context)


@login_required(login_url='authapp:login')
def view_all(request):
    context = dict()
    search = ''
    try:
        search = request.GET['search']
    except:
        pass
    context['employees'] = Employee.objects.all().order_by('-joined_date')
    if search is not None:
        print(search)
        context['employees'] = Employee.objects.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(department__name__icontains=search) |
            Q(role__name__icontains=search)
        ).order_by('-joined_date')
    return render(request, 'employee/view_all.html', context)


@login_required(login_url='authapp:login')
def view_single_employee(request, id):
    context = dict()
    try:
        employee = Employee.objects.get(pk=id)
    except:
        pass

    context['employee'] = employee

    return render(request, 'employee/employee.html', context)


@login_required(login_url='authapp:login')
def add(request):
    context = dict()
    context['form'] = AddEmployeeForm()
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            messages.info(request, 'Employee added successfully.')
            return redirect('index')
        else:
            return render(request, 'employee/add.html', context)
    else:
        context['form'] = AddEmployeeForm()
    return render(request, 'employee/add.html', context)


@login_required(login_url='authapp:login')
def update(request, id):
    context = dict()
    try:
        employee = Employee.objects.get(pk=id)
    except Employee.DoesNotExist:
        messages.error(request, f'Empoyee does not exist with id {id}')
        return render(request, 'employee/update.html', context)

    form = AddEmployeeForm(instance=employee)
    context['form'] = form

    if request.method == 'POST':
        form = AddEmployeeForm(request.POST, instance=employee)
        context['form'] = form
        if form.is_valid():
            form.save()
            messages.info(request, 'Employee updated successfully.')
            return redirect('employee:view_single_employee', employee.id)
    print(request.resolver_match.url_name)
    return render(request, 'employee/update.html', context)


@login_required(login_url='authapp:login')
def delete(request, id):
    try:
        employee = Employee.objects.get(pk=id)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee does not exist.')
        return redirect('employee:view_all')

    employee.delete()

    messages.info(request, 'Employee deleted successfully.')
    return redirect('employee:view_all')

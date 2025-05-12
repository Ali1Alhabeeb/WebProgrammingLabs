from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from .models import Book,Address,Student, Students, Department, Course, Card
from django.db.models import Q, Count ,Min ,Max ,Sum ,Avg
from .forms import BookForm

def index(request):
    return render(request, "bookmodule/index.html")


def list_books(request):
    
    return render(request, 'bookmodule/list_books.html')


def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')


def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')
                
def linkspage(request):
    return render(request,'html5/links.html')

def formatting(request):
    return render(request,'html5/formatting.html')

def listing(request):
    return render(request,'html5/listing.html')

def tables(request):
    return render(request,'html5/tables.html')

def simple_query(request):
    mybooks=Book.objects.filter(title__icontains='and') # <- multiple objects
    return render(request, 'bookmodule/booklist.html', {'books':mybooks})


def complex_query(request):
    mybooks=books=Book.objects.filter(author__isnull =False).filter(title__icontains='and').filter(edition__gte = 2).exclude(price__lte = 100)[:10]
    if len(mybooks)>=1:
        return render(request, 'bookmodule/booklist.html', {'books':mybooks})
    else:
        return render(request, 'bookmodule/index.html')

def task1(request):
    mybooks=Book.objects.filter(Q(price__lte=80))
    if len(mybooks)>=1:
        return render(request,'bookmodule/booklist.html',{'books':mybooks})
    else:
        return render(request, 'bookmodule/index.html')

def task2(request):
    mybooks=Book.objects.filter(Q(edition__gt=3)& (Q(author__contains='co') | Q(title__contains='co')))
    if len(mybooks)>=1:
        return render(request,'bookmodule/booklist.html',{'books':mybooks})
    else:
        return render(request, 'bookmodule/index.html')
    

def task3(request):
     books=Book.objects.filter(~Q(edition__gt = 2) & (~Q(title__icontains = 'qu') | ~Q(author__icontains = 'qu')))
     return render(request, 'bookmodule/bookList.html', {'books':books})
 
def task4(request):
    books=Book.objects.order_by('title')
    return render(request, 'bookmodule/bookList.html', {'books':books})
    

def task5(request):
     query1 = Book.objects.aggregate(
         count=Count('id'),
         total_price=Sum('price'),
         average_price=Avg('price'),
         min_price=Min('price'),
         max_price=Max('price')
     )
     return render(request, 'bookmodule/task5.html', {'query1': query1})
 
 
def task7(request):
    cities = Address.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/task7.html', {'cities': cities })


#lab 8 
# def task1(request):


def booksearch(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        # now filter
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower():contained = True

            if contained: newBooks.append(item)
        return render(request, 'bookList.html', {'books':newBooks})
    return render(request,'search.html')


def viewbook(request, bookId):
# assume that we have the following books somewhere (e.g. database)
    book1 = {'id':123, 'title':'Continuous Delivery', 'author':'J. Humble and D. Farley'}
    book2 = {'id':456, 'title':'Secrets of Reverse Engineering', 'author':'E. Eilam'}
    targetBook = None
    if book1['id'] == bookId: targetBook = book1
    if book2['id'] == bookId: targetBook = book2
    context = {'book':targetBook} # book is the variable name accessible by the template
    return render(request, 'bookmodule/show.html', context)


def __getBooksList():
 book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
 book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
 book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
 return [book1, book2, book3]


def listbooks(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/listbooks.html', {'books':books})

def addbook(request):
    if request.method =="POST":
        Book.objects.create(
            title= request.POST['title'],
            author= request.POST['author']
            )
        return redirect('list_books')
    return render(request, 'bookmodule/addbook.html')

def editbook(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == "POST":
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.save()
        return redirect('list_books')
    return render(request, 'bookmodule/editbook.html', {'book':book})

def deletebook(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('list_books')


def listbooks2(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/listbooks2.html', {'books':books})

def addbook2(request):
    if request.method =="POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save
            return redirect("list_books2")
    else:
        form = BookForm() 
    return render(request, 'bookmodule/addbook2.html',{'form':form})


def editbook2(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == "POST":
        form = BookForm(request.POST,instance=Book)
        if form.is_valid():
                form.save
                return redirect('list_books2')
    else:
        form = BookForm(instance=Book) 
    return render(request, 'bookmodule/editbook2.html', {'form':form})

def deletebook2(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('list_books2')

def task11(request):
    departments = Department.objects.annotate(student_count=Count('students'))
    return render(request, 'bookmodule/task11.html', {'departments':departments})

def task22(request):
    courses = Course.objects.annotate(student_count=Count('students'))
    return render(request, 'bookmodule/task22.html', {'courses':courses})

def task33(request):
    departments = Department.objects.annotate(oldest_student_id=Min('students__id'))
    
    department_data = []

    for department in departments:
        if department.oldest_student_id is not None:
            oldest_student = department.students_set.get(id=department.oldest_student_id)
            department_data.append(
                {
                    'department_name': department.name,
                    'oldest_student_name': oldest_student.name
                }
            )

    return render(request, 'bookmodule/task33.html', {'department_data': department_data})

def task44(request):
    departments = Department.objects.annotate(student_count=Count('students')).filter(student_count__gt=2).order_by("-student_count")
    return render(request, 'bookmodule/task44.html', {'departments':departments})
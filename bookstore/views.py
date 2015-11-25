from django.shortcuts import render
from .models import Book
import MySQLdb


years = [2010,2011,2012,2013,2014,2015,2016]
prices = [1,2,3,4,5,6,7]

def book_list(request):
	# con = MySQLdb.connect(host = "localhost",user = "root",passwd = "",db = "bookstore")
	# books = "";
	# with con:
	#     cur = con.cursor()
	#     cur.execute("DROP TABLE Book")
	#     # cur.execute("CREATE TABLE Book(ISBN integer primary key, title varchar(100), publisher varchar(100), author varchar(100), keywords varchar(100), subject varchar(100), format varchar(9), year_of_publication integer, price integer, copies integer)")
	#     # for i in range(100):
	#     # 	commd = "INSERT INTO Book VALUES(ISBN = %d,title = 'title%d',publisher = 'publisher%d',author = 'author%d', keywords = 'keywords%d', subject = 'subject%d', format ='hardcover', year_of_publication = 2015, price = %d, copies = %d)" %(101+i+1, i+1, i+1, i+1, i+1, i+1, years[(i+1)%7], prices[(i+1)%7])
	#     # 	cur.execute(commd)
	#     cur.execute("SELECT * FROM book")
	#     if cur.rowcount==0:
	#     	print "Insertion Failed"
	#     else:
	#     	books=cur.fetchone()
	# for i in range(99):
	# 	Book.objects.create(ISBN = i+1,title = 'title'+str(i+1),publisher = 'publisher'+str(i+1),author = 'author'+str(i+1), keywords = 'keywords'+str(i+1), subject = 'subject'+str(i+1), format ='hardcover', year_of_publication = 2015, price = years[(i+1)%7], copies = prices[(i+1)%7])
	return render(request, 'test.html', {'book_list': Book.objects.all()})

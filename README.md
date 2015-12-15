#50.008 Database: B&N Online Bookstore Report
![Imgur](http://i.imgur.com/oBJNyqt.png)
```python
Term 6 2015		
		  
Darren Ng Wei Hong 1000568, 
Anvitha Prashantha 1000459, 
Yijuan Lin 1000440, 
Yunke Zhou 1000434, 
Wen wen Chen 1000594





		    
```
![Imgur](http://i.imgur.com/jWAyfmf.png)

#Contents

[TOC]

```python







```

##1. ER Diagram and Relational Schema

###1.1 ER Diagram

![Imgur](http://i.imgur.com/OgZi4T6.png)

###1.2 Relational Schema

####1.2.1 Books Table

```sql
CREATE TABLE bookstore_book (
ISBN bigint NOT NULL PRIMARY KEY, 
title varchar(100) NOT NULL, 
publisher varchar(100) NOT NULL, 
author varchar(100) NOT NULL, 
keywords varchar(100) NOT NULL, 
subject varchar(100) NOT NULL, 
format varchar(9) NOT NULL, 
year_of_publication integer NOT NULL, 
price integer NOT NULL, 
copies integer NOT NULL,
CHECK (format = 'hardcover' or format = 'softcover'));
```
		
####1.2.2 Customer Table

```sql
CREATE TABLE bookstore_customer (
password varchar(128) NOT NULL, 
last_login datetime(6) NULL, 
is_superuser bool NOT NULL, 
username varchar(100) NOT NULL PRIMARY KEY, 
fullname varchar(100) NOT NULL, 
phone bigint NOT NULL, 
card bigint NOT NULL, 
address varchar(100) NOT NULL, 
is_staff bool NOT NULL, 
is_active bool NOT NULL);
```

####1.2.3 Order Table

```sql
CREATE TABLE bookstore_order(
id integer unsigned AUTO_INCREMENT PRIMARY KEY,
customer_id varchar(100) references bookstore_customer(username),
book_id bigint references bookstore_book(ISBN),
order_date varchar(20) NOT NULL,
order_status varchar(20) NOT NULL,
copies integer NOT NULL
);
```
	
####1.2.4 Rating Table

```sql
CREATE TABLE bookstore_rating(
customer_id varchar(100) references bookstore_customer(username), 
rater_id varchar(100) references bookstore_customer(username),
book_id bigint references bookstore_book(ISBN),
rate integer,
PRIMARY KEY (customer_id, rater_id, book_id),
CHECK (rate <= 2 and rate >=0),
CHECK (customer_id != rater_id));
```
####1.2.5 Feedback Table

```sql
CREATE TABLE bookstore_feedback(
book_id bigint references bookstore_book(ISBN),
customer_id varchar(100) references bookstore_customer(username), 
text varchar(100), 
score integer NOT NULL, 
date varchar(20) NOT NULL,
PRIMARY KEY(customer_id,book_id),
CHECK (score >= 0 and score <= 10)
);
```

##2. Application Implementation

###2.1 System Architecture

The database application project was developed using `Django`, a high-level Python Web framework that allows rapid development and encourages clean and pragmatic design and `MySQL`.

The B&N bookstore project repository can be found at [B&N Online Bookstore](https://github.com/yunkez/database_project.git).

The application was developed and designed in a carefully crafted three step process.

1. Requirement Analysis is first performed. Gathering of system and user requirements and define the objective of the database led to the design of the database relational schema. Next, SQL query statements were made to insert, read, alter the database. To improve performance and to reduce dependencies, most of the database logic are implemented on the MySQL side instead of the front-end. 
2. Next, the Django interface was implemented to interact with the MySQL database developed.
3. Finally, the web page was styled using CSS that is backward compatible to older browsers.

The motivation behind adopting this modularity approach is to separate the Front-end Interface with the logic of the database application. This software development methodology is greatly adopted in the agile development framework like the **Model View Controller** (MVC).

###2.2 User Interface Design Considerations

CSS based design adopted is both backwards compatible with older browsers as well as current newer browser, hence ensuring compatibility with both mobile devices and desktop browsers.

On top of that, the web application is designed for both users and administrative users to complete their intended task with minimal clicks. Visual selection button is used wherever possible instead of requesting users to manually type in serves not only as a pleasant User Interface consideration but also as a first form of check to ensure the necessary integrity constraints.

The included top navigation bar is present throughout the entire web application. Frequently used system functionalities such as information overview, back to homepage for search, order records and logging out can be accessed through the Top Navigation bar.

![Imgur](http://i.imgur.com/hc2Y0I1.png)

Each bookâ€™s details is also designed in a way such that the most important information is the most prominent, such as the price.



##3. System Functionalities
###3.1 Registration

Adopting the conventional User Interface Design, the `Registration` page will be the first page new users will be brought to. 

To register, the user will have to input the following information:

- Username
- Password
- Full Name
- Phone Number
- Address
- Credit Card Number

![Imgur](http://i.imgur.com/8YmVRzO.png)

Checks in the database will then be made to ensure that the fields are not empty and that the username is available. The following code snippet checks for the validity of the user form input:

```python
user_form = CustomerCreationForm(data=request.POST)
        if user_form.is_valid():
	        #perform register new user
		else:
            print user_form.errors #returns the error
```

Furthermore, the user is expected to type out the password twice, so as to ensure that the correct intended password has been keyed in properly.

The following SQL is executed to insert a new customer into the `bookstore_customer` table in the database. 

```mySQL
INSERT INTO bookstore_customer VALUES ('password',NULL,'0','%s','%s','%s','%s','%s','1','1');"%(username,fullname,phone,card,address)
```
When we insert customer detail into `bookstore_customer` table,  the password is actually a sudo variable as we do not want the database to store userâ€™s password directly due to security purposes. Instead, after each customer's details are inserted, we call the following method to store a hashed password inside the database.
```python
u.set_password("%s"% password)
            u.save()
```
Once a user has been successfully registered, he will then be able to log in into his account in the future. The `def user_login(request)` function will be executed whenever the user requests to login. 

```python
 user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/bookstore')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("You have entered wrong username or password.")
    else:
        return render_to_response('bookstore/login.html', {'base_template':'base.html'}, context)
```

Authentication is done to check if the user is indeed registered first followed by a check if the username and password matches or are correct. This two levelled check ensures integrity of the system.

Once a user has been successfully registered, he/she can now login to his/her account in the future.

![Imgur](http://i.imgur.com/FUpKVrF.png)

###3.2 Ordering

Once a book to be ordered has been found through the `search` function, the user simply click the order book button to acknowledge purchase.

![Imgur](http://i.imgur.com/ZRLcJET.png)

The user will be brought to a confirmation page where the quantity of the books to be ordered can be selected. The available quantity is indicted below the selection bar.

![Imgur](http://i.imgur.com/yCDoXVx.png)

The SQL statement checks if the current inventory has sufficient amount of books the user is requesting. It adopts a **all-or-nothing** approach. If a user request more books than what the inventory currently holds, a simple message:

```python
info = "Not enough stock"
```
Will be displayed to show the current amount of books available. This check ensures that the user does not order more books than he actually can. The function `def order(request)` handles the ordering function of the system.

The following SQL is executed to insert an order into the `Orders` table in the database:

```sql
INSERT INTO bookstore_order (customer_id,book_id,order_date,order_status,copies)
VALUES ('%s','%s','%s','completed','%s')"%(username,ISBN,date,copies)
```
Once an Order has been placed, it is important to ensure that the tables in the database are updated as well. The following SQL is executed automatically after a successful order is placed: 	

```SQL		
UPDATE bookstore_book SET copies='%d' 
WHERE ISBN='%s'"%(avail-copies,ISBN)
```

###3.3 User Account Information

The user account information provides an overview of the user's essential information and can be easily accessed by clicking on the account button located at the top right of the webpage.

The user account information displays the following:

- Profile
	- Username
	- Full name
	- Phone number
	- Credit card number
	- Address
- Feedback History
	- Books
	- Score
	- Date
- Rating History
	- User Rated
	- Book title
	- Description
	- Rating Score

![Imgur](http://i.imgur.com/OcJcAct.png)

The following SQL statement is used to extract and display the information found in the Customer's account:

```sql		
SELECT username,fullname,phone,card,address FROM bookstore_customer 
WHERE username='%s'"%(username)
```
The following SQL statement is used to retrieve the information on Order History:
```sql
SELECT id,book_id,title,order_date,order_status,bookstore_order.copies 
FROM bookstore_order JOIN bookstore_book 
WHERE bookstore_order.book_id=bookstore_book.ISBN 
AND customer_id='%s' 
AND order_status='completed' 
order by id desc"%(username))
```
The following SQL statement is used to retrieve the information on Feedback History:
```sql
SELECT title,text,score,date FROM bookstore_feedback,bookstore_book
WHERE customer_id='%s' 
AND bookstore_feedback.book_id=bookstore_book.ISBN"%(username)
```
The following SQL statement is used to retrieve the information on Rating History:

```sql
SELECT f.customer_id,f.text,b.title,r.rate FROM bookstore_rating r,bookstore_feedback f,bookstore_book b 
WHERE r.customer_id = '%s' 
AND r.rater_id=f.customer_id 
AND r.book_id=f.book_id
AND r.book_id=b.ISBN;"%(username)
```

Furthermore, the user will be able to edit his account information details by selecting the `edit user profile` button found at the top right corner of the page. 

![Imgur](http://i.imgur.com/gJWwPUP.png)

The following SQL code is executed should if a user wishes to update his account information:

```sql
UPDATE bookstore_customer 
SET fullname='%s', phone='%s', card='%s',address='%s';"%(fullname,phone,card,address)
```


		
###3.4 Feedback

Within the detailed page of any book found in the web application, a user can leave a personal feedback on the book. 
A feedback includes:

- Description of the feedback
- Rating from $0-10$ as indicted by the stars

![Imgur](http://i.imgur.com/eHauAat.png)

One of the User Interface design choice is the implementation of feedback ratings as stars instead of having the user to input the rating manually. This design decision is better as:

1. It provides a visual feedback for users and is easier then to manually type out the rating
2. It provides an additional layer of checking mechanism as users will never rate the book out of the accepted range of $0-10$.

Moreover, the code **will still check** for the correctness of the rating input first.

Once the check passes, the following SQL statement is executed.
```sql
INSERT INTO bookstore_feedback VALUES ('%s','%s','%s','%s','%s')"%(ISBN,username, text,score,date)
```
Once the feedback has been submitted, a pop up message will notify the user that the feedback has been successfully recorded as shown below. This provides a visual feedback for users to confirm that their Feedback is recorded successfully.

![Imgur](http://i.imgur.com/R1ilpuU.png)

On top of that, the system also checks if a particular user has already given his/her feedback. The same user will only be able to submit a feedback rating once.

The following pop-up message will appear if a particular user attempts to feedback more than once.

![Imgur](http://i.imgur.com/pZsrFlL.png)

####3.4.1 Feedback Usefulness

Users may wish to rate the feedback of a book submitted by other users and can do so by simply selecting the one of the options located at the far right of the comment box.

Users can either rate the feedback:

- Very useful
- Useful
- Useless

![Imgur](http://i.imgur.com/q0oqD4M.png)

The selection buttons make the feedback usefulness feature hassle-free and easy to use. On top of that, it is a simple solution to maintain integrity constraints as users can only rate these feedback with those scores ($2$: very useful, $1$: useful, $0$: useless). Instead of typing out the score which will and can lead to errors, the button selection panel ensures that the right rating is submitted at all times.

The following check is done first to ensure that the rating is done by another user and
if successful, the following SQL statement will be executed:
```pytohn
if username != rater:
            try:
                sql = "INSERT INTO bookstore_rating VALUES ('%s','%s','%s','%s')"%(username, rater, isbn, score)
                cur.execute(sql)
                # return redirect("/bookstore/detail/%s"%isbn)
                return redirect(reverse("detail",args=[isbn,0,3]))
```

On top of that, the system also checks if a particular user has already given his/her feedback. The same user will only be able to submit a rating for a feedback by another user once. 

The following pop-up message will appear if a particular user attempts to feedback more than once.

![Imgur](http://i.imgur.com/NpTCLGW.png)

The following pop-up message will appear if a particular user tries to vote his own feedback.

![Imgur](http://i.imgur.com/2hqXd4j.png)

####3.4.2 Top most Useful Feedback

For a given book, a user is able to request for the top $n$ most 'useful' feedbacks. The â€˜usefulnessâ€™ of a feedback is its average â€˜usefulnessâ€™ score.

When the user selects an arbitrary number $n$ to be displayed, the following SQL code is executed to retrieve the feedbacks.

```sql
SELECT AVG(score) FROM bookstore_feedback where book_id='%s';"%(isbn)
```

Instead of simply just returning the ordered list of most useful feedbacks, the function also gives a breakdown of the user submitted scores that contributed to that feedback. 


```sql
SELECT bf.*,temp.rate,temp.numVotes FROM bookstore_feedback bf 
join(select r2.rater_id,r2.book_id,r2.rate ,count(*) as numVotes,priority from bookstore_rating r2 
join(select r.rater_id,r.book_id,avg(r.rate) as priority from bookstore_rating r group by r.book_id,r.rater_id 
having r.book_id='%s') as rank
where r2.book_id='%s' 
and rank.rater_id=r2.rater_id 
group by r2.rate,r2.rater_id,rank.priority) as temp 
where temp.rater_id = bf.customer_id 
and bf.book_id = '%s' 
order by temp.priority desc,rater_id;"%(isbn,isbn,isbn)
```

Instead of requesting the users to manually key in the $n$ number of top feedbacks to view, a drop down menu located at the far right of the feedback table allows users to easily and quickly access and change $n$ if need be. 

![Imgur](http://i.imgur.com/15XmRE9.png)

###3.5 Search and Sort

To ensure that users have fine control over their searches, the web application's homepage has a dedicated search bar that will search through the backend database for any matching book based on the following attributes:

- Title of the book
- Author of the book
- Publisher
- Subject
- Keywords

The following python function is responsible for  a the search request system functionality: `def index(request)`. The above function is also used to search the books sorted by the average feedback rating. 

To handle cases of exceptions where a user inputs an author's incomplete name, the SQL will handle it by parsing and searching through the database for matches based on the user's input. This is very important as most users will not remember the full title of the book or the full name of an author.

The following snippet of the code parses the user's input and the SQL query will search for matches. 
```python
def searchValue(s):
    return "%"+s+"%"
```
By adding the user's input with the `"%"` symbol concatenated to both sides of the input, the user will be able to search partial names of authors, publishers, book titles and even subjects. The main motivation for this implementation is that most users will not be able to remember the full title of a book, author etc. This feature is additional and is shown below:

On top of that, the user will be able to select if he wants the result to be sorted by the year of publication, `year_of_publication` or the average score, `AVG(score)`. This selection is controlled by the `sort` input variable. As shown above in the python function `def book_browsing`.

The following SQL code is executed should if the user requested for a sorting in terms of the year of publication.

```sql
ELECT b.*,average from (SELECT * FROM bookstore_book 
where title LIKE '%s' and author LIKE '%s' and publisher LIKE'%s' and subject LIKE '%s') b, (SELECT book_id, AVG(score) AS average FROM bookstore_feedback 
GROUP BY book_id UNION SELECT ISBN,0 FROM bookstore_book 
WHERE ISBN NOT IN (SELECT book_id FROM bookstore_feedback)) T 
WHERE b.ISBN=T.book_id 
order by %s DESC "%     (searchValue(title),searchValue(author),searchValue(publisher),searchValue(subject),orderby)
```

The `LIKE` checks for strings that matches the input of the user.

The following SQL code is executed if the user requested for a sorting in terms of the average score.

```sql
SELECT b.*,T.average FROM bookstore_book b,(SELECT book_id, AVG(score) AS average \
            FROM bookstore_feedback GROUP BY book_id) T WHERE b.ISBN=T.book_id UNION SELECT b.*,0 AS average \
        FROM bookstore_book b WHERE b.ISBN NOT IN (SELECT book_id FROM bookstore_feedback) ORDER BY average DESC;")
```

###3.6 Book Recommendation

Once a user has done ordering a book, the web application will display to the user a list of recommended titles based on other users who have purchased the book. Ordered by the most popular book (with the highest sale count). 

```sql
SELECT title,author,ISBN from bookstore_book 
where ISBN in (SELECT book_id FROM (SELECT book_id, count(*) as num from bookstore_order 
where customer_id in (SELECT customer_id from bookstore_order 
where book_id = '%s' and customer_id != '%s')
and book_id != '%s'
group by book_id 
order by num desc) T) "%(ISBN,username,ISBN)
```
Book Recommendation will only appear after a successful ordering of books.

```python
if completed:
        username = request.user.username
        # Execute the above SQL code snippet
```

The following is a screenshot of the book recommendation based on popularity after a successful transaction of book ordering by the user.

![Imgur](http://i.imgur.com/WGezdTW.png)

###3.7 Administrative Functions

When an administrative user signs in, he/she will have the following additional system functionalities. On top of that, an additional `monthly statistics` button is added to the top navigation bar. 

![Imgur](http://i.imgur.com/14vW8a0.png)

#### 3.7.1 Add New Book

As an administrative user, one can add to existing books in the inventory or new books by simple selecting on the `Add` function found in the selection bar. 
![Imgur](http://i.imgur.com/KShht0s.png)

The python file `manage.py` handles the creation of a administrative user. The following code used in the terminal to create an administrative account.

![Imgur](http://i.imgur.com/rlHZHps.png)

To add a new book, the admin is required to input all of the following fields:

- ISBN 13
- Title
- Author
- Publisher
- Publication Year
- Stock to be added
- Price
- Format (hardcover/softcover)
- Subject
- Keywords

The function `def addNewBook(request)` handles new book request once the user submits a new book with the above fields filled up.

The following code snippet ensures that the format of the book added maintains the integrity constraint of the fields filled by the user, `book_form.is_valid()`:
```python
if book_form.is_valid():
	#execute SQL request
else:
    print book_form.errors
```

If the book is new,  with the correct fields entered, the following SQL will be executed:
```sql
INSERT INTO bookstore_book VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(ISBN,title,publisher,author,keywords,subject,format,year,price,copies)
```


####3.7.2 Update Existing Book

Administrative user might want to add and restock books already existing in the database. The following code first checks if the book is already in the database and returns an error message should if the book is not found in the database.

```python
 try:
     cur.execute("SELECT copies FROM bookstore_book WHERE ISBN = '%s'"%(ISBN))
     avail = int(cur.fetchone()[0])  
     cur.execute("UPDATE bookstore_book SET copies='%d' WHERE ISBN='%s'"%(avail+copies,ISBN))
     completed = True
            
 except Book.DoesNotExist:
            info = "Please enter a valid ISBN."
```

The following SQL function is executed whenever an admin wishes to add new stock to existing books.

```SQL
UPDATE num_of_copies from Book where ISBN = book_id
```
The `add` button can be found under the price of the book, replacing the `order` button in the user point of view. Once the `add` button has been selected for a particular book, a pop-up screen indicating the number of copies to be added will appear at the top of the screen.

![Imgur](http://i.imgur.com/TPek0Xi.png)

Once the inventory copies of the book has been updated successfully, the administrative user will be brought to a confirmation page.

![Imgur](http://i.imgur.com/12wSAUn.png)

#### 3.7.2 Statistics
Every month, the administrative user can pull statistics of the following form:

-  top $m$ most popular books (in terms of copies sold in that month), the list of the 
Every month, the store manager wants
-  The list of $m$ most popular authors
- The list of $m$ most popular publishers

A search bar will allow the administrative user to select the $m$ most popular books, authors and publishers he/she wishes to see. 

![Imgur](http://i.imgur.com/CCTRoAg.png)

Instead of displaying the options for the top books, authors or publishers separately, all of these information are displayed in a simple table format and the administrative user can view all the necessary monthly statistic information in a neat and clean format.

![Imgur](http://i.imgur.com/EBpzHXd.png)

The information will be displayed in descending order in terms of popularity. The function `def manager_account(request,count)` handles the system functionality `statistics`.

The following SQL is used to retrieve the top $m$ books sold in the current month:
```sql
SELECT ISBN,title,author FROM bookstore_book WHERE ISBN IN (SELECT book_id 
FROM (SELECT book_id, count(*) AS num 
FROM bookstore_order WHERE order_date LIKE '%s'  
GROUP BY book_id ORDER BY num DESC) T);"%(date)
```

The following SQL is used to retrieve the top $m$ authors most popular in the current month:

```sql
SELECT b1.author, count(*) AS num FROM bookstore_book b1, bookstore_order o1 
WHERE b1.ISBN = o1.book_id
AND order_date LIKE '%s'GROUP BY b1.author 
ORDER BY num DESC;"%(date)   
```

The following SQL is used to retrieve the top $m$ publisher found in the current month:

```sql
SELECT b1.publisher, count(*) AS num FROM bookstore_book b1, bookstore_order o1 
WHERE b1.ISBN = o1.book_id\
AND order_date LIKE '%s' 
GROUP BY b1.publisher 
ORDER BY num DESC;"%(date)




```

##4. User Guide and Screenshots
![Imgur](http://i.imgur.com/3yESLD5.png)


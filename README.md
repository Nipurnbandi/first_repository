<h1>Library Management System</h1>

<p><b>Status:</b> In Progress</p>

<h2>🔧 Tech Stack</h2>
<ul>
  <li>Python</li>
  <li>SQLite3</li>
  <li>datetime module</li>
</ul>

<h2>Project Overview</h2>
<p>
A console-based Library Management System built using Python and SQLite.
The system manages students, books, book issuance, and fine calculation
with proper relational database design.
</p>

<h2>Database Tables</h2>
<ul>
  <li><b>student</b> – Stores student details</li>
  <li><b>quantity_books</b> – Stores book-level information</li>
  <li><b>all_books</b> – Tracks individual book copies</li>
  <li><b>published_books</b> – Stores issued book records</li>
</ul>

<h2> Features Implemented</h2>
<ul>
  <li>Student data storage</li>
  <li>Book inventory with multiple copies</li>
  <li>Book issuing system</li>
  <li>Prevents issuing already issued books</li>
  <li>Automatic issue and renew dates (15 days)</li>
  <li>Fine calculation for overdue books</li>
  <li>Foreign key constraints for data integrity</li>
</ul>

<h2>Fine Logic</h2>
<p>
If the current date exceeds the renew date, a fine of ₹10 per day is applied.
</p>

<h2>Pending Work</h2>
<ul>
  <li>Book renewal</li>
  <li>Book submission</li>
  <li>Quantity updates</li>
  <li>Improved menu loop</li>
</ul>

<p><b>Author:</b> Nipurn Bandi</p>

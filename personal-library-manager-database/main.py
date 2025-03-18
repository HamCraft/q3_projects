import sqlite3
import streamlit as st

DB_NAME = "books.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                genre TEXT,
                read INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def add_book(title, author, year, genre, read):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, year, genre, read) VALUES (?, ?, ?, ?, ?)", 
                       (title, author, year, genre, int(read)))
        conn.commit()

def delete_book(title):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE title = ?", (title,))
        conn.commit()

def search_books(query):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ?", 
                       (f"%{query.lower()}%", f"%{query.lower()}%"))
        return cursor.fetchall()

def get_all_books():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        return cursor.fetchall()

def update_book(book_id, title, author, year, genre, read):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE books SET title=?, author=?, year=?, genre=?, read=? WHERE id=?
        """, (title, author, year, genre, int(read), book_id))
        conn.commit()

def get_reading_progress():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM books")
        total_books = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM books WHERE read=1")
        completed_books = cursor.fetchone()[0]
    return total_books, completed_books

# Initialize DB
init_db()

# Streamlit UI
st.title("📚 Book Collection Manager")

menu = ["Add Book", "View Books", "Search Books", "Update Book", "Delete Book", "Reading Progress"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Book":
    st.subheader("📖 Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read = st.checkbox("Read")
    if st.button("Add Book"):
        add_book(title, author, year, genre, read)
        st.success(f"Book '{title}' added successfully!")

elif choice == "View Books":
    st.subheader("📚 Your Book Collection")
    books = get_all_books()
    if books:
        for book in books:
            st.write(f"**{book[1]}** by {book[2]} ({book[3]}) - {book[4]} - {'Read' if book[5] else 'Unread'}")
    else:
        st.info("No books found in your collection.")

elif choice == "Search Books":
    st.subheader("🔍 Search Books")
    query = st.text_input("Enter title or author")
    if st.button("Search"):
        results = search_books(query)
        if results:
            for book in results:
                st.write(f"**{book[1]}** by {book[2]} ({book[3]}) - {book[4]} - {'Read' if book[5] else 'Unread'}")
        else:
            st.warning("No matching books found.")

elif choice == "Update Book":
    st.subheader("✏️ Update Book Details")
    books = get_all_books()
    book_titles = [book[1] for book in books]
    selected_book = st.selectbox("Select Book to Update", book_titles)
    if selected_book:
        book_data = next(book for book in books if book[1] == selected_book)
        new_title = st.text_input("Title", book_data[1])
        new_author = st.text_input("Author", book_data[2])
        new_year = st.number_input("Year", value=book_data[3], min_value=0, max_value=2100, step=1)
        new_genre = st.text_input("Genre", book_data[4])
        new_read = st.checkbox("Read", value=bool(book_data[5]))
        if st.button("Update Book"):
            update_book(book_data[0], new_title, new_author, new_year, new_genre, new_read)
            st.success(f"Book '{new_title}' updated successfully!")

elif choice == "Delete Book":
    st.subheader("🗑️ Delete a Book")
    books = get_all_books()
    book_titles = [book[1] for book in books]
    selected_book = st.selectbox("Select Book to Delete", book_titles)
    if st.button("Delete Book"):
        delete_book(selected_book)
        st.success(f"Book '{selected_book}' deleted successfully!")

elif choice == "Reading Progress":
    st.subheader("📊 Reading Progress")
    total_books, completed_books = get_reading_progress()
    completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0
    st.write(f"Total Books: {total_books}")
    st.write(f"Books Read: {completed_books}")
    st.progress(completion_rate / 100)
